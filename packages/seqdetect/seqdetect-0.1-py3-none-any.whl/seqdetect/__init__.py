# This source code is part of the SeqDetect package and is distributed
# under the 3-Clause BSD License. Please see 'LICENSE.rst' for further
# information.

__author__ = "Patrick Kunzmann"
__version__ = "0.1"

import argparse
import pickle
import hashlib
from os.path import splitext, isfile
import sys
import numpy as np
import biotite
import biotite.sequence as seq
import biotite.sequence.io.fasta as fasta
import biotite.sequence.io.genbank as gb
import biotite.application.blast as blast
import biotite.database.entrez as entrez
from .detect import detect_features
from .gbwrite import write_genbank


def main():
    parser = argparse.ArgumentParser(
        description="Automatically detect DNA sequence features "
                    "via a BLAST search."
    )
    parser.add_argument(
        "infile",
        help="Input sequence file (FASTA or GenBank format). "
             "A too long sequence may result in an error."
    )
    parser.add_argument(
        "--version", action="version",
        version=f"seqdetect {__version__}"
    )
    parser.add_argument(
        "--identity", "-i", type=float,
        help="The sequence identity to a matching feature must be at least "
             "this value. By default an exact match is required."
    )
    parser.add_argument(
        "--number", "-n", type=int, default=50,
        help="The number of top BLAST hits to consider."
    )
    parser.add_argument(
        "--minsize", "-m", type=int, default=0,
        help="Set a minimum size of the feature, to be considered."
    )
    parser.add_argument(
        "--database", "-d", default="nr",
        help="The BLAST database to search in."
    )
    parser.add_argument(
        "--species", "-s",
        help="Limit the organism to search in."
    ),
    parser.add_argument(
        "--feature", "-f", action="append",
        help="Look only for a specific feature key (e.g. 'regulatory'). "
             "Parameter can be repeated to search for multiple feature keys."
    )
    parser.add_argument(
        "--expand", "-x", type=int, default=0,
        help="By default the search space for features does only include the "
             "BLAST hit. That means, that means that features outside the hit "
             "range are not considered, although they might also have a high "
             "similarity."
             "By setting this parameter, the search space is "
             "expanded into both directions of the hit by the given amount of "
             "nucleotides."
    )
    parser.add_argument(
        "--outfile", "-o",
        help="Write the resulting feature annotated sequence into a GenBank "
             "file at the given path."
    )
    parser.add_argument(
        "--mail", "-M", type=int, default=0,
        help="Set the mail address for BLAST requests. You can be contacted "
             "by the NCBI via this address if anything goes totally wrong. "
             "It is recommended to set this option."
    )
    args = parser.parse_args()

    
    ### Read the input file ###
    # Only file extension is important
    name, extension = splitext(args.infile)
    if extension in [".gb"]:
        gb_file = gb.GenBankFile()
        gb_file.read(args.infile)
        annot_seq = gb_file.get_annotated_sequence()
    elif extension in [".fasta", ".fa", ".mpfa", ".fna", ".fsa"]:
        fasta_file = fasta.FastaFile()
        fasta_file.read(args.infile)
        sequence = fasta.get_sequence(fasta_file)
        # No feature info in FASTA -> empty annotation
        annotation = seq.Annotation()
        annot_seq = seq.AnnotatedSequence(annotation, sequence)
    else:
        raise ValueError(f"Unknown file extension '{extension}'")
    
    hash_dict = {
        "sequence" : str(annot_seq.sequence),
        "number" : args.number,
        "feature" : args.feature,
        "species" : args.species,
        "database" : args.database,
    }
    ### BLAST the sequence ###
    # Check if the same configuration was already BLASTed
    # in the last SeqDetect run
    hash_file_name = ".seqdetect.md5"
    ali_file_name  = ".seqdetect.blast"
    hash_dict = {
        "sequence" : str(annot_seq.sequence),
        "number" : args.number,
        "feature" : args.feature,
        "species" : args.species,
        "database" : args.database,
    }
    blast_config_hash = hashlib.md5(str(hash_dict).encode("utf-8")).digest()
    if isfile(hash_file_name) and isfile(ali_file_name):
        with open(hash_file_name, "rb") as file:
            previous_hash = file.read()
            blasted = (blast_config_hash == previous_hash)
    else:
        blasted = False
    # If the sequence has not been BLASTed in the last run, then BLAST
    if not blasted:
        app = blast.BlastWebApp(
            "blastn", sequence, database=args.database, mail=args.mail
        )
        app.set_max_results(args.number)
        query = None
        if args.feature is not None:
            for key in args.feature:
                if query is None:
                    query = entrez.SimpleQuery(key, field="Feature Key")
                else:
                    query |= entrez.SimpleQuery(key, field="Feature Key")
        if args.species is not None:
            if query is None:
                query = entrez.SimpleQuery(args.species, field="Organism")
            else:
                query &= entrez.SimpleQuery(args.species, field="Organism")
        app.set_entrez_query(query)
        app.start()
        print("Blasting...", file=sys.stderr)
        app.join()
        alignments = app.get_alignments()
        # Cache the BLAST result
        # and mark the current configuration as blasted
        with open(ali_file_name, "wb") as file:
            pickle.dump(alignments, file)
        with open(hash_file_name, "wb") as file:
            file.write(blast_config_hash)
    else:
        with open(ali_file_name, "rb") as file:
            alignments = pickle.load(file)
    
    ### Detect features ###
    annot_seq = detect_features(
        annot_seq, alignments, args.identity, args.expand,
        args.minsize, args.feature
    )

    
    ### Write results to file ###
    gb_out = write_genbank(annot_seq, "SeqDetect", "DNA")
    if args.outfile is not None:
        with open(args.outfile, "w") as file:
            file.write(gb_out)
    else:
        print(gb_out)