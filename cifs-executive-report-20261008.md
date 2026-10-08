# CIFS xfstests: Executive Report

**Prepared:** October 8, 2026

**Functional results through:** October 8, 2026

**Code-coverage measurement:** October 6, 2026

**Repository:** [bharathsm-ms/smb-xfstests-dev](https://github.com/bharathsm-ms/smb-xfstests-dev), branch `cifs-xfstests`

## Executive Summary

The CIFS xfstests repository provides a repeatable regression-testing framework
for the Linux CIFS/SMB client across **Samba, Azure Files, Windows Server, and
ksmbd**. It combines filesystem correctness checks, authentication and security
tests, recovery workloads, and source-code coverage to expose reliability and
interoperability risks before release.

The current results inventory contains **290 committed test IDs**. An isolated
Samba CIFS-only coverage campaign, including targeted follow-up work, exercised
**18,052 client-code lines (57.29%)**, **852 functions (72.26%)**, and
**8,056 branches (35.98%)**. The follow-up added 331 previously unhit lines,
9 functions, and 226 branches without changing the client build or merging
historical coverage.

**Recommendation:** use the repository as a controlled engineering qualification
baseline and develop a reviewed CI subset from it. The retained failures,
configuration-dependent skips, and source-version differences mean it is not
yet a blanket production-readiness or server-compatibility certification.

## Test Scope and Engineering Value

| Test Area | Representative Coverage | Engineering Benefit |
| --- | --- | --- |
| Data integrity and file operations | Read/write, mmap, truncate, sparse files, large-file boundaries, server-side copy, and cross-mount byte comparisons; examples include `cifs/208-217`, `235`, and `310`. | Detects data mismatches, stale reads, and boundary-condition regressions. |
| Authentication and security | Signing, encryption, Kerberos, multiuser credentials, credential-cache selection, and decryption offload; examples include `118-119`, `158`, `203`, `323-324`, `329`, `356`, `404`, and `406`. | Tests identity isolation and negotiated security behavior with positive and negative controls. |
| Metadata and interoperability | Permissions, ACLs, SID mapping, extended attributes, links, Unicode names, and directory enumeration. | Makes differences in client/server filesystem semantics visible and reproducible. |
| Recovery and availability | Interrupted I/O, reconnects, DNS re-resolution, DFS target failover, and controlled server restarts; examples include `149`, `165`, `320`, and `387`. | Exercises recovery behavior beyond basic mount and read/write smoke tests. |
| Caching and concurrency | Attribute and directory caches, locks, lease/oplock breaks, deferred close, credit pressure, and concurrent workloads. | Helps isolate races, coherency problems, and resource-management failures. |
| Advanced SMB features | Multichannel, SMB3 POSIX extensions, snapshots, port-139 transport, and server filesystem compression; examples include `330`, `379`, `390`, `392`, `403`, and `407`. | Supports capability-specific qualification without assuming identical server feature sets. |

These describe test intent and available workloads, not a claim that every
feature passed on every backend. The local development inventory also contains
15 candidate tests outside the 290-test results scope; their presence does not
establish review approval or cross-server validation.

## Cross-Server Results

| Backend | Pass | Fail | Skip | Timeout | Deferred | No Recorded Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Samba 4.22.11 | 239 | 24 | 27 | 0 | 0 | 0 |
| Azure Files | 206 | 26 | 54 | 3 | 1 | 0 |
| Windows Server | 218 | 22 | 49 | 0 | 1 | 0 |
| ksmbd | 211 | 17 | 60 | 2 | 0 | 0 |

Each row accounts for the same 290-ID reporting inventory. A skip, timeout,
deferral, or missing result is not a pass. Failures can arise from test defects,
fixture assumptions, client behavior, or server behavior; they are not all
established server defects.

The October 8 ksmbd batch closed the remaining inventory gap with **1 pass,
1 failure, and 19 skips**. All four backends now have recorded outcomes for all
290 IDs. Test `407` passed its filesystem-compression checks; `390` failed on a
permission-denied `chmod` after POSIX negotiation. Most new skips reflect missing
feature fixtures or disabled opt-ins, not proven lack of server support.

These are the latest observed results assembled from baseline runs and targeted
reruns, not a simultaneous full-suite run of one identical source tree. Azure
combines main, canary, and preproduction endpoint observations. The tested ksmbd
fixture disabled multichannel, SMB2 leases, and durable handles. The Windows
edition/build was not identified, limiting version-specific conclusions.

The October 7 validation of seven repaired tests produced **18 passes, 8 failures,
and 2 skips across 28 test/backend outcomes**. This work improved result fidelity:
it corrected successful socket-sharing and flush cases, recognized an unsupported
Azure operation as a skip, and retained a newly exposed Windows failure.

## Measured Code Coverage

The following measurements cover the **Linux SMB client**, not server code or
the entire Linux kernel. They use the same instrumented build and denominator:
47 C source files, 31,508 executable lines, 1,179 functions, and 22,392 branches.

| Metric | Isolated Baseline | After Targeted Follow-Up | Additional Unique Hits |
| --- | ---: | ---: | ---: |
| Lines | 17,721 / 31,508 (56.24%) | 18,052 / 31,508 (57.29%) | 331 |
| Functions | 843 / 1,179 (71.50%) | 852 / 1,179 (72.26%) | 9 |
| Branches | 7,830 / 22,392 (34.97%) | 8,056 / 22,392 (35.98%) | 226 |

The line-coverage increase is **1.05 percentage points**. Targeted credential,
Kerberos, DNS, socket-sharing, and large-file fixtures exercised additional code
using existing tests, illustrating the value of improving execution conditions
as well as adding test cases.

**Measurement boundaries:**

- The coverage campaign selected all 305 local CIFS tests, including candidates
  excluded from the functional report. Its percentages must not be relabeled as
  coverage attributable solely to the 290 committed IDs.
- Counts include fixture setup, diagnostic attempts, and failed/skipped execution,
  not only passing tests or the final successful follow-up batch. No generic-test
  or historical coverage was merged into this measurement.
- The source filter is `fs/smb/client/*.c`; headers and exception branches are
  excluded. The client was kernel `7.3.0-rc2+`, with Samba 4.22.11 and an unchanged
  CIFS module build during the campaign.
- Execution coverage is not proof of assertion completeness, correctness, or
  feature support. The build does not measure the main SMB Direct or SMB wire
  compression implementations; those require separately matched builds.
- The earlier 60.11% historical Samba aggregate had a broader measurement scope
  and is not interchangeable with this CIFS-only result. Later cross-server runs
  mixed live counters, so no new coverage percentage is claimed for the
  October 7-8 functional runs.

## Benefits and Readiness

**Earlier regression detection.** The suite exercises failure-prone boundaries,
concurrent operations, and recovery paths that basic connectivity checks miss.

**Faster, more defensible triage.** Per-test results, expected-output comparisons,
source hashes, logs, and fixture records help separate test and environment
problems from client/server defects. Preserving failures avoids false confidence.

**Coverage-guided investment.** Measured additional code execution provides a
way to prioritize missing fixtures and reachable untested paths. It is more
informative than test-count growth alone.

**A foundation for repeatable qualification.** The xfstests harness and xUnit
results support automation. Several advanced fixture and orchestration tools
remain local-only and must be reviewed and packaged before others can reproduce
the complete development workflow from a committed checkout.

These are engineering capabilities and expected operational benefits. No measured
reduction in production incidents, validation cost, or test-cycle duration is
claimed, and the cross-server results are not a performance ranking.

## Recommended Next Steps

1. Resolve high-impact data-integrity, reconnect, locking, and directory-cache
   failures, retaining separate attribution for test, fixture, client, and server.
2. Investigate the ksmbd POSIX permission failure and address missing feature
  fixtures where supported; rerun affected cases with pinned test, helper,
  kernel, server, and configuration versions.
3. Review the 15 local candidates and package the required fixture tooling;
   passing one workload is not sufficient approval for publication or CI gating.
4. Establish a reviewed, non-disruptive CI subset and separate extended recovery
   and stress runs on disposable hosts with dedicated shares and explicit opt-ins.
5. Extend coverage through supported, reachable feature paths while preserving
   source/build identity and isolated measurement windows.

## Evidence and References

- [Test catalogue and setup guidance](README.cifs-tests.md)
- [Complete current results](cifs-results_latest.md)
- [Failure and skip explanations](cifs-results-failures-20261006.md)
- [Run provenance and source-version limits](cifs-results-20261006.md)

The following paths identify locally retained coverage evidence, not published
repository content or portable links:

- Isolated baseline report: `coverage/samba-cifs-only-20261006/REPORT.md`.
- Cumulative follow-up report: `results-runs/samba422-supplement-final-20261006/REPORT.md`.
- Machine-readable comparison: `results-runs/samba422-supplement-final-20261006/baseline-gains.json`.

The retained archives include checksums, source identities, raw counters, and
HTML coverage. Raw logs can contain credentials or SMB session keys; share only
reviewed, redacted material alongside this summary.
