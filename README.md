# OligoArk 🧬

**DNA archival storage for large files with exact recovery.**

## Problem statement

DNA can store data for a very long time, but a practical DNA-storage system must do more than
encode small files. It should be able to:

- store large and mixed types of data without using huge amounts of RAM;
- recover the original file exactly even when some DNA strands are lost;
- work with realistic DNA strand lengths;
- measure storage density, speed, memory use and redundancy clearly.

OligoArk is built to test these goals. A run is considered successful only when the recovered
file matches the original file exactly using **SHA-256**.

## Why DNA storage?

DNA storage is not mainly about making a file smaller in digital form. Its advantage is that
very large amounts of information can potentially be stored in an extremely small amount of
physical DNA, kept for long periods with little or no power while at rest, and later sequenced
to recover the original data. OligoArk focuses on making that storage process scalable,
memory-efficient and exactly recoverable.

## Benchmark results

### 1 GiB storage test

OligoArk successfully stored and recovered a **1 GiB heterogeneous dataset** containing mixed
data types.

| Test | Result | Lost strands recovered | Density | Encode speed | Decode speed | Peak memory |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Clean | ✅ PASS | 0 | **1.646 bits/nt** | 9.78 MiB/s | 23.08 MiB/s | 43.85 MiB |
| 1% strand loss | ✅ PASS | **45,338 / 45,338** | **1.646 bits/nt** | 9.77 MiB/s | 17.91 MiB/s | 44.08 MiB |
| 5% strand loss | ✅ PASS | **226,705 / 226,705** | **1.646 bits/nt** | 9.95 MiB/s | 12.12 MiB/s | 43.63 MiB |

**Redundancy:** 12.5%  
**Archive overhead:** 1.234×  
**Total strands:** 5,096,877

OligoArk also passed exact SHA-256 recovery at:

**1 KiB → 64 KiB → 1 MiB → 10 MiB → 100 MiB → 1 GiB**

Memory stayed nearly flat as the data size increased, showing that the storage path is
**bounded-memory** rather than loading the whole archive into RAM.

### Realistic 248-nt strand test

The 248-nt profile uses Reed-Solomon protection to test more DNA-like error conditions.

| Protection | Clean | 1% loss | 5% loss | Substitution errors | Insert/delete errors | Mixed errors |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| None | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| XOR | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Fountain | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Hybrid | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |

The main remaining technical problem is **insertion/deletion errors**. Substitution errors are
recovered in the tested RS-enabled profile, but indel and mixed-error recovery still need
improvement.

### Comparison with other DNA-storage codecs

Matched test: 1 MiB payload, 152-nt strands, 25% redundancy, five trials per condition.

| Method | Density | Clean | 1% loss | 5% loss | Substitution |
| --- | ---: | ---: | ---: | ---: | ---: |
| **OligoArk Fountain** | 0.463 bits/nt | 5/5 | 0/5 | 0/5 | **5/5** |
| **DNA Fountain** | **1.347 bits/nt** | 5/5 | **5/5** | **5/5** | 0/5 |
| **Goldman-style + XOR** | 0.515 bits/nt | 5/5 | 0/5 | 0/5 | 0/5 |

DNA Fountain currently has better density and dropout recovery in this matched 152-nt test.
OligoArk currently performs better in the tested substitution-error condition.

### Other dataset benchmarks

These tests use published physical-read datasets and measure **reference-strand reconstruction**.

| Dataset | Reads per strand | OligoArk | Pinned BBS |
| --- | ---: | ---: | ---: |
| Microsoft CNR (Nanopore) | 5 | **73/96 (76.0%)** | 72–74/96 |
| Microsoft CNR (Nanopore) | 10 | **93/96 (96.9%)** | **93/96 (96.9%)** |
| Grass et al. (Illumina) | 5 | **94/96 (97.9%)** | 90/96 (93.8%) |
| Grass et al. (Illumina) | 10 | **96/96 (100%)** | 95/96 (99.0%) |
| LCRC HFS-11.7K | 5 | **96/96 (100%)** | **96/96 (100%)** |
| LCRC HFS-11.7K | 10 | **96/96 (100%)** | **96/96 (100%)** |
| DNAformer Pilot | 1 | **83/96 (86.5%)** | **83/96 (86.5%)** |
| DNAformer Pilot | 5 | **96/96 (100%)** | **96/96 (100%)** |
| DNAformer Pilot | 10 | **96/96 (100%)** | **96/96 (100%)** |

On these external datasets, OligoArk matches or slightly improves reconstruction accuracy over
the pinned BBS baseline in several settings, while LCRC and DNAformer reach full recovery at
5–10 reads per strand.

> **Important:** The 1 GiB result is a software storage benchmark with controlled strand loss.
> The 248-nt tests are realistic-strand software experiments. External physical-read results
> are reconstruction benchmarks. These results are **not** an end-to-end wet-lab DNA-storage
> experiment.

More details: [scalable storage](docs/scalable-storage.md) · [codec comparison](docs/dna-fountain-baseline.md)
