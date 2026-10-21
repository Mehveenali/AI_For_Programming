# reverse_complement.py
# Reads a single-line DNA sequence from a FASTA file and prints its
# reverse complement.

COMPLEMENT = {"A": "T", "T": "A", "C": "G", "G": "C"}

def read_fasta_sequence(path):
    """Return the sequence (str) from a single-record FASTA file."""
    sequence = []
    has_header = False

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if has_header:
                    raise ValueError("Expected a single-record FASTA file")
                has_header = True
                continue
            if not has_header:
                raise ValueError("Expected a FASTA header before the sequence")
            sequence.extend(line.split())

    if not has_header:
        raise ValueError("Missing FASTA header")
    return "".join(sequence)

def reverse_complement(seq):
    """Return the reverse complement of a DNA sequence."""
    seq = "".join(seq.split()).upper()
    try:
        return "".join(COMPLEMENT[base] for base in reversed(seq))
    except KeyError as error:
        raise ValueError(
            f"Invalid DNA base {error.args[0]!r}; sequence must contain only A, T, C, or G"
        ) from error

if __name__ == "__main__":
    import sys
    seq = read_fasta_sequence(sys.argv[1])
    print(reverse_complement(seq))
