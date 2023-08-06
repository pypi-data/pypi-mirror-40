# This source code is part of the SeqDetect package and is distributed
# under the 3-Clause BSD License. Please see 'LICENSE.rst' for further
# information.

__author__ = "Patrick Kunzmann"
__all__ = ["detect_features"]

import sys
import numpy as np
import biotite
import biotite.sequence as seq
import biotite.sequence.align as align
import biotite.sequence.io.fasta as fasta
import biotite.sequence.io.genbank as gb
import biotite.database.entrez as entrez


def detect_features(query, blast_alignments, threshold_identity=None,
                    expand=0, min_size=0, feature_keys=None):
    # Expand alphabet to be compatible with ambiguous sequences
    result = seq.AnnotatedSequence(
        query.annotation.copy(),
        seq.NucleotideSequence(query.sequence, ambiguous=True)
    )
    
    # Fetch GenBank files for the hit UIDs in the alignments
    uids = [alignment.hit_id for alignment in blast_alignments]
    print("Fetching data from NCBI Entrez...", file=sys.stderr)
    file_name = entrez.fetch_single_file(
        uids, biotite.temp_file("gb"), db_name="nuccore", ret_type="gb"
    )

    # Iterate over all GenBank files
    # and look for features in BLAST hit range
    multi_file = gb.MultiFile("gb")
    multi_file.read(file_name)
    for i, (alignment,gb_file) in enumerate(zip(blast_alignments, multi_file)):
        print(
            f"Analyzing {i+1:3d}/{len(blast_alignments):3d}...",
            end="\r", file=sys.stderr
        )
        query_interval = alignment.query_interval
        # The query should not be reverse complement
        if query_interval[0] > query_interval[1]:
            raise ValueError("Query is reverse complement")
        hit_interval = alignment.hit_interval
        # The hit may be reverse complement
        if hit_interval[0] > hit_interval[1]:
            first, last = hit_interval[1], hit_interval[0]
            hit_interval = (first, last)
            strand = seq.Location.Strand.REVERSE
        else:
            strand = seq.Location.Strand.FORWARD
        
        # Expand the search range by the supplied expand value
        range_first = hit_interval[0] - expand
        range_last  = hit_interval[1] + expand
        # Get the annotation in range of the BLAST hit + expand
        search_annot_seq = gb_file.get_annotated_sequence()
        if range_first < search_annot_seq.sequence_start:
            range_first = search_annot_seq.sequence_start
        if range_last >= search_annot_seq.sequence_start \
                         + len(search_annot_seq.sequence):
                range_last = \
                    search_annot_seq.sequence_start \
                    + len(search_annot_seq.sequence) +1
        # Limit annotated sequence to search range
        # 'range_last+1' due to inclusive stop to exclusive stop
        search_annot_seq = search_annot_seq[range_first : range_last+1]
        if strand == seq.Location.Strand.REVERSE:
            search_annot_seq = search_annot_seq.reverse_complement()

        for feature in search_annot_seq.annotation:
            if feature_keys is not None:
                if feature.key not in feature_keys:
                    # Ignore this feature
                    continue
            # Feature location must be completely in range of hit
            in_range = True
            for loc in feature.locs:
                if loc.defect & seq.Location.Defect.MISS_LEFT or \
                   loc.defect & seq.Location.Defect.MISS_RIGHT:
                        # Part of the feature is truncated
                        # in the subannotation
                        in_range = False
            # Check for minimum feature size condition
            location_range = feature.get_location_range()
            if location_range[1] - location_range[0] < min_size:
                in_range = False

            if in_range:
                # All locations of the feature are in range
                # -> Compare with query sequence
                is_match = True
                locs_on_query = []
                for loc in feature.locs:
                    start = loc.first - search_annot_seq.sequence_start
                    stop = loc.last - search_annot_seq.sequence_start + 1
                    feature_sequence = search_annot_seq.sequence[start : stop]
                    if threshold_identity is None:
                        # Check for exact identity:
                        match = _match_subsequence(
                            result.sequence, feature_sequence
                        )
                    else:
                        # Check for partial identity with query sequence
                        match = _match_align(
                            result.sequence, feature_sequence, threshold_identity
                        )
                    if match is None:
                        is_match = False
                        break
                    else:
                        first = match + result.sequence_start
                        last = first + len(feature_sequence) -1
                        locs_on_query.append(seq.Location(
                            first, last, loc.strand, loc.defect
                        ))
                # Added detected annotation to input annotated sequence
                if is_match:
                    qual = feature.qual
                    # Add reference to origin GenBank file
                    qual["db_xref"] = gb_file.get_accession()
                    result.annotation.add_feature(seq.Feature(
                        feature.key, locs_on_query, qual
                    ))
    print("", file=sys.stderr)
    return result


def _match_subsequence(reference, query):
    matches = seq.find_subsequence(reference, query)
    if len(matches) == 0:
        return None
    return matches[0]


def _match_align(reference, query, thres_identity):
    alph = seq.NucleotideSequence.alphabet_amb
    # Use identity matrix
    matrix = align.SubstitutionMatrix(alph, alph, np.identity(len(alph)))
    alignment = align.align_optimal(
        reference, query, matrix=matrix, gap_penalty=-2,
        max_number=1, terminal_penalty=False
    )[0]
    # Array that stores alignment positions
    # where no gap is in the query sequence
    non_query_gaps = np.where(alignment.trace[:,1] != -1)[0]
    query_start, query_stop = non_query_gaps[0], non_query_gaps[-1]
    alignment = alignment[query_start : query_stop+1]
    if align.get_sequence_identity(alignment, mode="all") >= thres_identity:
        return alignment.trace[0,0]
    else:
        return None