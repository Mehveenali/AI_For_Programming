#!/usr/bin/env python3
"""Print GC content percentages for records in a FASTA file."""

import argparse
import sys


def read_fasta_records(path):
    """Yield (header, sequence) pairs from a multi-record FASTA file."""
    header = None
    sequence = []

    with open(path) as fasta_file:
        for line in fasta_file:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    yield header, "".join(sequence)
                header = line[1:]
                sequence = []
            else:
                if header is None:
                    raise ValueError("Expected a FASTA header before the sequence")
                sequence.extend(line.split())

    if header is not None:
        yield header, "".join(sequence)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fasta_path", help="path to the FASTA file")
    parser.add_argument(
        "--min-gc",
        type=float,
        help="print only records with GC content strictly greater than this percentage",
    )
    args = parser.parse_args()

    for header, sequence in read_fasta_records(args.fasta_path):
        if not sequence:
            print(f"Warning: skipping empty sequence for {header!r}", file=sys.stderr)
            continue
        gc_count = sequence.upper().count("G") + sequence.upper().count("C")
        gc_percent = gc_count / len(sequence) * 100
        if args.min_gc is not None and gc_percent <= args.min_gc:
            continue
        print(f">{header}\tGC content: {gc_percent:.2f}%")


if __name__ == "__main__":
    main()
