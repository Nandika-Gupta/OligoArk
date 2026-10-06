import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

from oligoark.physical import (
    PhysicalDatasetManifest,
    evaluate_physical_reconstruction,
    read_sequences,
)

BENCHMARKS = Path(__file__).resolve().parents[1] / "benchmarks"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "cnr_tiny"


def _load_converter(monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    monkeypatch.syspath_prepend(str(BENCHMARKS))
    spec = importlib.util.spec_from_file_location(
        "convert_cnr_to_physical", BENCHMARKS / "convert_cnr_to_physical.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cnr_manifest_records_public_provenance() -> None:
    manifest = PhysicalDatasetManifest.load("datasets/cnr.json")
    assert manifest.doi == "10.48550/arXiv.2107.06440"
    assert manifest.run_accessions == (
        "microsoft/clustered-nanopore-reads-dataset@6938f44796185902a08381943c2895782886c5c3",
    )
    assert "MIT" in manifest.data_restrictions
    assert "nearest reference" in manifest.reference_mapping_status


def test_cnr_fixture_converts_and_evaluates(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    converter = _load_converter(monkeypatch)
    centers = [
        line.strip()
        for line in (FIXTURE / "Centers.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    clusters = converter.load_clusters(FIXTURE / "Clusters.txt", expected_count=len(centers))
    assert [len(reads) for reads in clusters] == [3, 3, 0, 3]

    reads_out = tmp_path / "reads.fasta"
    references_out = tmp_path / "references.fasta"
    references, reads = converter.write_physical_inputs(
        centers,
        clusters,
        limit=10,
        max_reads_per_cluster=2,
        reads_out=reads_out,
        references_out=references_out,
    )
    assert (references, reads) == (3, 6)
    reference_text = references_out.read_text(encoding="utf-8")
    assert ">cnr_00002\n" not in reference_text
    assert read_sequences(references_out) == [centers[0], centers[1], centers[3]]

    result = evaluate_physical_reconstruction(
        PhysicalDatasetManifest.load("datasets/cnr.json"),
        read_sequences(reads_out),
        read_sequences(references_out),
    )
    assert result.reference_count == 3
    assert result.total_reads == 6
    assert result.assigned_reads + result.unassigned_reads == result.total_reads


def test_cnr_conversion_stops_at_limit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    converter = _load_converter(monkeypatch)
    references, reads = converter.write_physical_inputs(
        ["AAAA", "CCCC", "GGGG"],
        [["AAAA"], [], ["GGGG", "GGGA"]],
        limit=1,
        max_reads_per_cluster=5,
        reads_out=tmp_path / "reads.fasta",
        references_out=tmp_path / "references.fasta",
    )
    assert (references, reads) == (1, 1)
    with pytest.raises(ValueError):
        converter.write_physical_inputs(
            ["AAAA"],
            [],
            limit=1,
            max_reads_per_cluster=1,
            reads_out=tmp_path / "r.fasta",
            references_out=tmp_path / "f.fasta",
        )
