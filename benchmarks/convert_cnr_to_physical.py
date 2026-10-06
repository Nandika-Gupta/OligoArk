"""Convert a CNR subset into reads/references FASTA files for run_physical_dataset.py."""

from __future__ import annotations

import argparse
from pathlib import Path

from run_external_cnr_benchmark import load_centers, load_clusters


def write_physical_inputs(
    centers: list[str],
    clusters: list[list[str]],
    *,
    limit: int,
    max_reads_per_cluster: int,
    reads_out: Path,
    references_out: Path,
) -> tuple[int, int]:
    """Write the first ``limit`` non-empty clusters and return (references, reads)."""
    if len(centers) != len(clusters):
        raise ValueError("centers and clusters must have the same length")
    if limit < 1 or max_reads_per_cluster < 1:
        raise ValueError("limit and max_reads_per_cluster must be positive")
    reference_lines: list[str] = []
    read_lines: list[str] = []
    for index, (center, reads) in enumerate(zip(centers, clusters, strict=True)):
        if not reads:
            continue
        reference_lines.append(f">cnr_{index:05d}\n{center}\n")
        for read_index, read in enumerate(reads[:max_reads_per_cluster]):
            read_lines.append(f">cnr_{index:05d}_r{read_index}\n{read}\n")
        if len(reference_lines) == limit:
            break
    references_out.write_text("".join(reference_lines), encoding="utf-8")
    reads_out.write_text("".join(read_lines), encoding="utf-8")
    return len(reference_lines), len(read_lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--centers", type=Path, required=True)
    parser.add_argument("--clusters", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--max-reads-per-cluster", type=int, default=10)
    parser.add_argument("--reads-out", type=Path, default=Path("cnr-reads.fasta"))
    parser.add_argument("--references-out", type=Path, default=Path("cnr-references.fasta"))
    args = parser.parse_args()

    centers = load_centers(args.centers)
    clusters = load_clusters(args.clusters, expected_count=len(centers))
    references, reads = write_physical_inputs(
        centers,
        clusters,
        limit=args.limit,
        max_reads_per_cluster=args.max_reads_per_cluster,
        reads_out=args.reads_out,
        references_out=args.references_out,
    )
    print(f"wrote {references} references and {reads} reads")


if __name__ == "__main__":
    main()
