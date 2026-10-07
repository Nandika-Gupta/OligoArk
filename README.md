# OligoArk 🧬

**Scalable DNA archival-storage and reconstruction research.**

## Problem statement

DNA archival storage is promising for long-term, high-density preservation, but practical
software systems still need to answer three engineering questions:

1. **Can large heterogeneous files be encoded and recovered without memory growing with the
   whole archive?**
2. **Can the original bytes be recovered exactly when DNA strands are lost or reads are
   noisy?**
3. **Can storage density, redundancy, throughput, memory and reconstruction quality be
   measured reproducibly under realistic strand-length constraints and fair baselines?**

OligoArk addresses these questions with bounded-memory streaming archives, configurable
150–250 nt strand profiles, redundancy/error simulation, reconstruction, and **SHA-256 exact
recovery as the final success criterion**.

## Benchmark results

### 100 MiB scalable archive

| Condition | SHA-256 recovery | Density | Encode | Decode | Peak RSS | Redundancy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Clean | ✅ PASS | **1.645832 bits/nt** | 11.78 MiB/s | 43.88 MiB/s | 108.42 MiB | 12.5001% |
| 1% controlled dropout | ✅ PASS | **1.645832 bits/nt** | 12.00 MiB/s | 24.99 MiB/s | 108.42 MiB | 12.5001% |
| 5% controlled dropout | ✅ PASS | **1.645832 bits/nt** | 11.66 MiB/s | 16.25 MiB/s | 108.04 MiB | 12.5001% |

The same deterministic 100 MiB heterogeneous payload was recovered byte-for-byte in all three cases.

**Scaling:** 1 KiB → 64 KiB → 1 MiB → 10 MiB → 100 MiB all passed SHA-256 verification.  
**Memory scaling:** bounded.  
**Runtime scaling:** linear-or-better.

### OligoArk vs DNA Fountain

| Metric | **OligoArk** | **DNA Fountain baseline** |
| --- | ---: | ---: |
| 100 MiB archival test | ✅ PASS | Not evaluated |
| Clean recovery | ✅ PASS | ✅ PASS |
| 5% strand dropout | ✅ PASS at 100 MiB with XOR | ✅ 3/3 at 152 nt |
| Density at 100 MiB scale | **1.645832 bits/nt** | Not measured |
| Density in matched 152-nt test | 0.457756 bits/nt | **1.347368 bits/nt** |
| Memory scaling | **Bounded through 100 MiB** | Small comparison only |
| Runtime scaling | **Linear-or-better through 100 MiB** | Small comparison only |

### External physical-read reconstruction

| Dataset | Reads/strand | **OligoArk** | Pinned BBS |
| --- | ---: | ---: | ---: |
| Microsoft CNR (Nanopore) | 5 | **73/96 (76.0%)** | 72–74/96 |
| Microsoft CNR (Nanopore) | 10 | **93/96 (96.9%)** | **93/96 (96.9%)** |
| Grass et al. (Illumina) | 5 | **94/96 (97.9%)** | 90/96 (93.8%) |
| Grass et al. (Illumina) | 10 | **96/96 (100%)** | 95/96 (99.0%) |
| LCRC HFS-11.7K | 5 | **96/96 (100%)** | **96/96 (100%)** |
| LCRC HFS-11.7K | 10 | **96/96 (100%)** | **96/96 (100%)** |
| DNAformer Pilot | 5 | **96/96 (100%)** | **96/96 (100%)** |
| DNAformer Pilot | 10 | **96/96 (100%)** | **96/96 (100%)** |

> **Claim boundary:** The 100 MiB results are software archive / controlled-channel evidence. External CNR, Grass, LCRC and DNAformer results are reference-strand reconstruction benchmarks, not end-to-end wet-lab OligoArk archive storage.

Details: [100 MiB acceptance evidence](docs/storage-scale-acceptance-2026-10-07.md) · [DNA Fountain comparison](docs/dna-fountain-baseline.md)
