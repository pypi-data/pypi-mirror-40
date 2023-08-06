# This source code is part of the SeqDetect package and is distributed
# under the 3-Clause BSD License. Please see 'LICENSE.rst' for further
# information.

__author__ = "Patrick Kunzmann"
__all__ = ["write_genbank"]

import biotite.sequence as seq


_KEY_START = 5
_QUAL_START = 21
_SYMBOLS_PER_CHUNK = 10
_SEQ_CHUNKS_PER_LINE = 6
_SYMBOLS_PER_LINE = _SYMBOLS_PER_CHUNK * _SEQ_CHUNKS_PER_LINE


def write_genbank(annotat_seq, locus, mol_type):
    lines = []
    lines += _write_locus(annotat_seq.sequence, locus, mol_type)
    lines += _write_feature_table(annotat_seq.annotation)
    lines += _write_sequence(annotat_seq.sequence, annotat_seq.sequence_start)
    lines += [r"\\"]
    return "\n".join(lines)


def _write_locus(sequence, locus, mol_type):
    return [
        f"LOCUS       {locus:12} {str(len(sequence)) + ' bp':10} {mol_type}"
    ]


def _write_feature_table(annotation):
    lines = []
    lines.append("FEATURES             Location/Qualifiers")
    for feature in sorted(list(annotation)):
        line = " " * _KEY_START
        line += feature.key.ljust(_QUAL_START - _KEY_START)
        line += _write_location(feature.locs)
        lines.append(line)
        for key, values in feature.qual.items():
            for val in values.split("\n"):
                line = " " * _QUAL_START
                if val is None:
                    line +=  f"/{key}"
                else:
                    line +=  f'/{key}="{val}"'
                lines.append(line)

    return lines


def _write_sequence(sequence, seqstart):
    lines = []
    lines.append("ORIGIN")
    
    line = "{:>9d}".format(seqstart)
    for i in range(0, len(sequence), _SYMBOLS_PER_CHUNK):
        # New line after 5 sequence chunks
        if i != 0 and i % _SYMBOLS_PER_LINE == 0:
            lines.append(line)
            line = "{:>9d}".format(seqstart + i)
        line += " " + str(sequence[i : i + _SYMBOLS_PER_CHUNK])
    # Append last line
    lines.append(line)

    return lines


def _write_location(locs):
    if len(locs) == 1:
        loc = list(locs)[0]
        if loc.first == loc.last:
            loc_string = str(loc.first)
        elif loc.defect & seq.Location.Defect.UNK_LOC:
            loc_string = str(loc.first) + "." + str(loc.last)
        elif loc.defect & seq.Location.Defect.BETWEEN:
            loc_string = str(loc.first) + "^" + str(loc.last)
        else:
            loc_string = str(loc.first) + ".." + str(loc.last)
        if loc.strand == seq.Location.Strand.REVERSE:
            loc_string = f"complement({loc_string})"
    else:
        loc_string = ",".join(
            [_write_location([loc]) for loc in locs]
        )
        loc_string = f"join({loc_string})"
    return loc_string