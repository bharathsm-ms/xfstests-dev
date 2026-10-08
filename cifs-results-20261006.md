# CIFS Per-Test Results

**Updated:** 2026-10-08 | **Results through:** 2026-10-07

**Scope:** 290 committed test IDs at `bd42fe80`: 269 in the last-known remote
revision `1ebff9ed` and 21 committed locally but not yet pushed. Untracked tests
are excluded.

[Results overview](cifs-results_latest.md)
| [Failure and skip reasons](cifs-results-failures-20261006.md)
| [Test catalogue](README.cifs-tests.md)

## Summary

| Server | Test Dates (2026) | ✅ Pass | ❌ Fail | ⏭️ Skip | ⏱️ Timeout | ⏸️ Deferred | Total |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Samba 4.22.11 | Oct 6-7 | 239 | 24 | 27 | 0 | 0 | 290 |
| Azure | Oct 3-7 | 206 | 26 | 54 | 3 | 1 | 290 |
| Windows | Oct 1-3, 7 | 218 | 22 | 49 | 0 | 1 | 290 |
| ksmbd | Sep 25, Oct 7 | 210 | 16 | 41 | 2 | 0 | 269 |

These are the latest recorded outcomes from dated runs, not a new run of the
committed checkout. The repaired scripts `103`, `116`, `157`, `171`, `216`, `251`
and `310` are included with these reports and match their October 7 live-run
source archives. Some live-run helper and fixture changes remain local, so this
is not an exact committed-tree live rerun. Tests `192`, `194`, `225`, `236` and
`275` still have pending local repairs. Failures are not necessarily server
defects, and these focused repairs do not certify every assertion in each test.

ksmbd has no recorded results for 21 committed tests, shown as `-` rather than
skips. Test `168` was deferred on Azure and Windows for capacity safety.

## October 7 Repair Validation

The latest seven-test validation used unchanged test sources and expected
outputs on Samba 4.22.11, the main Azure Files endpoint, the published Windows
endpoint and a temporary ksmbd fixture. **28 latest outcomes: 18 PASS, 8 FAIL,
2 SKIP, no timeouts.** These results are merged into the complete matrix.

| Test | Samba | Azure | Windows | ksmbd |
| --- | --- | --- | --- | --- |
| cifs/103 | ✅ | ✅ | ✅ | ✅ |
| cifs/116 | ✅ | ⏭️ | ✅ | ✅ |
| cifs/157 | ✅ | ✅ | ✅ | ✅ |
| cifs/171 | ❌ | ✅ | ❌ | ⏭️ |
| cifs/216 | ✅ | ❌ | ❌ | ✅ |
| cifs/251 | ✅ | ✅ | ❌ | ✅ |
| cifs/310 | ❌ | ❌ | ❌ | ✅ |

Five cells changed: `103` FAIL to PASS on Samba and Windows; `157` FAIL to PASS
on ksmbd; `116` FAIL to SKIP on Azure; and `171` PASS to FAIL on Windows.
The latter emitted stale-file-handle diagnostics despite its final OK line.
Skips are not passes. Test `103` used a per-test profile without global
`nosharesock`, allowing both socket assertions to execute; other options were
preserved. The additional repairs are described in the
[test-issue review](cifs-results-failures-20261006.md#test-issue-review).

ksmbd-tools 3.5.3 used a loopback-device-bound listener on port 1445, with a
temporary `127.0.0.2:445` TCP forwarder for `157`'s test-owned mount helper,
which does not inherit the profile's port. Host Samba on `127.0.0.1:445` was
not stopped or changed. Two temporary 512 MiB ext4 shares replaced the older
2 GiB backing fixtures; multichannel, SMB2 leases and durable handles remained
disabled. Test `171` therefore skipped for unavailable leasing. The other
ksmbd matrix cells retain September 25 observations.

Two ksmbd preparation attempts are preserved separately: the first stopped
before tests because its safety check did not recognize `*%lo:1445`; the second
ran seven tests but `157` failed to connect without the default-port forwarder.
The final seven-test attempt supplied all ksmbd results above. Its daemon,
forwarder, module, lock, mounts, loops and temporary credentials were removed.
No test assertion was changed between attempts.

Each test ran in a private mount/PID namespace with a 600-second limit.
Test/helper source hashes and xUnit records were verified. Host settings,
services, firewall, loop devices and feature state matched the initial audit;
owned runtime and mounts were cleaned up. The loaded client build was unchanged.
Counters were captured without reset; they now include mixed-backend activity,
so no new coverage percentage or Samba-only attribution is claimed.

Fresh failure reasons are in the
[failure report](cifs-results-failures-20261006.md#test-issue-review). The latest
sealed sources are `results-runs/cifs-repaired-seven-20261007` (Samba, Azure,
Windows) and `results-runs/cifs-repaired-seven-ksmbd-20261007-final` (ksmbd).
The stopped setup and intermediate ksmbd batch remain in the corresponding
`cifs-repaired-seven-ksmbd-20261007` and `-retry` directories.

The earlier five-test validation (15 executions: 8 PASS, 7 FAIL) remains sealed
in `results-runs/cifs-test-fixes-20261007` and
`results-runs/cifs-test-fixes-samba-20261007`, including its initial unsuccessful
Samba network preflight. No earlier archive was overwritten or relabeled.

<details>
<summary>Run notes and evidence</summary>

### Server Runs

- **Samba 4.22.11:** October 6 full run plus nine supplemental passes:
	`102 137 149 158 203 215 329 356 404`, then the October 7 seven-test repair
	validation above. No older Samba version is included.
- **Azure:** Latest result per test across the main endpoint and later canary
	and preproduction probes, not a single-endpoint suite run. Preproduction
	supplies the timeout for `275`, replacing the main endpoint's skip. The seven
	October 7 repair tests used the main endpoint.
- **Windows:** The later October 1 coverage run plus the October 3 review and
	the October 7 seven-test repair validation.
	The Windows edition/build was not identified.
- **ksmbd:** September 25 published suite at `1ebff9ed`, with multichannel,
	SMB2 leases and durable handles disabled, overlaid with the October 7
	seven-test final attempt described above.

The original Samba run, filtered to committed IDs, was **229 PASS, 25 FAIL,
36 SKIP**. The nine supplemental passes replace nine skips in the latest
results, not in the saved original run.

The Windows coverage run recorded **211 PASS, 21 FAIL, 36 SKIP, 1 deferred**
before the October 3 review. The earlier functional run recorded **209 PASS,
22 FAIL, 37 SKIP, 1 deferred** and remains separately documented in the
[Windows report](cifs-results-windows-20261001.md). Both published Windows runs
used revision `1ebff9ed`.

### Source and Fixture Limits

- Samba credential tests `158`, `203` and `356` passed with leases disabled
	to avoid share-mode cleanup errors. Lease-enabled cleanup is not confirmed fixed.
- Azure's failure for `356` used older, same-credential source. The repaired
	distinct-credential version passed on Samba but has not been rerun on Azure.
- Windows, Azure and ksmbd passes for `215` predate its remount repair.
- Aggregate coverage is omitted: saved counters include excluded tests and
	fixture activity, so they cannot be labeled committed-only coverage.

The five earlier pending repairs remain unresolved and were not rerun on October 7:

| Test | Open Issue |
| --- | --- |
| 192 | Samba passes, but current Azure reconnect failure and historical Windows/ksmbd failures need attribution. |
| 194 | Oversized-password helper negative control still fails. |
| 225 | Reparse behavior fails on tested Windows paths; no supported cross-server resolution. |
| 236 | PASS on Samba/Azure, but registered cache plus successful reread does not assert actual FS-Cache disk use. |
| 275 | Unresolved directory-cache/lease assertions; preproduction also records a timeout. |

### Committed Test Changes

Commit `028c3dc6` contains **19 tests: five repairs and fourteen additions**.
Every selected script and expected output matches the SHA-256 recorded for
a passing October 6 Samba attempt. Selection also considered assertions,
prerequisite gates, bounded operations, cleanup and helper dependencies;
a PASS alone is insufficient. This is not upstream approval or an all-server
compatibility certification.

| Test | Change | Validated Behavior / Limit |
| --- | --- | --- |
| 149 | Repair | Owned-socket reconnect, DNS switch and changed peer address; dedicated DNS hook required. |
| 158 | Repair | Distinct server credentials, POSIX private-file permissions, positive I/O and EACCES control. |
| 203 | Repair | Private secondary-UID cifscreds add/I/O/clear; fresh-mount access denied after clear. |
| 215 | Repair | Sparse >2 GiB/>4 GiB data and size persistence; remount replaces global VM cache drop. |
| 244 | Repair | Read/write file leases, SIGIO break and blocked competing opener; also PASS on Azure. |
| 323 | Add | Kerberos authentication and checked I/O. |
| 324 | Add | Kerberos integrity/signing mount and checked I/O. |
| 326 | Add | Existing Kerberos session remains usable after private ticket removal. |
| 327 | Add | Independently identified Kerberos and NTLMSSP connections and cross-mount data checks. |
| 328 | Add | Owned-socket Kerberos reconnect, authentication and data checks. |
| 329 | Add | Two non-root credential UIDs, checked I/O and distinct Kerberos sessions. |
| 330 | Add | Kerberos with at least two observed channels. |
| 331 | Add | Kerberos nolease mount with checked enumeration and directory-query increments. |
| 333 | Add | upcall_target option reporting, Kerberos I/O and invalid-value rejection. |
| 356 | Add | Distinct server credentials, private cifscreds lifecycle and separate SMB sessions. |
| 379 | Add | Snapshot enumeration size, UTF-16 labels, uniqueness and normal I/O. |
| 387 | Add | Explicitly authorized dedicated Samba restart, preserved files and post-restart I/O. |
| 404 | Add | Positive cruid, ticketless-UID denial and nonexistent-user rejection. |
| 406 | Add | Private tracing verifies decryption offload and disabled/below-threshold controls; also PASS on Azure. |

The commit includes restart/cleanup support in common/cifs_test, each new
expected-output file and only the selected additions to the group registry.
Other pending helper, harness, README and runner changes were not included.
No test assertions were changed during the commit-selection review.

Tests already committed before that selection, including `315`, `320`, `332`,
`355`, `365`, `390`, `392`, `403` and `407`, were not new additions in that commit.
Their matrix outcomes remain visible, including historical failures and skips.

### Fixture Requirements

Credential tests 158/203/356 require a separate same-domain server account in
`CIFS_CRED_FILE2`, not a copy of the primary account. Tests 203/356 additionally
require a dedicated non-root `CIFS_MULTIUSER_UID`. The Azure failure for 356
used the same credentials for both UIDs, for which the separate-session
assertion was inappropriate; it does not validate the repaired source.

Kerberos tests require a working KDC/upcall setup, dedicated credential UIDs
and private discoverable caches. Test 329 needs `CIFS_KRB5_SECOND_UID` and
tickets discoverable for both worker UIDs and the root bootstrap; 404 needs a
separate ticketless `CIFS_KRB5_EMPTY_UID`. No default host tickets should be
destroyed to construct those fixtures. Test 330 also needs multichannel.

Test 149 requires an executable absolute `CIFS149_DNS_HOOK` implementing
`switch HOST ADDRESS` and `restore HOST ADDRESS`, plus `CIFS149_SECOND_IP`.
Use a disposable hostname and scoped resolver; a Linux dns_resolver key
payload needs a trailing NUL byte. Test 244 needs Linux file leases enabled;
379 needs real existing snapshots on `CIFS_SNAPSHOT_DEV` or `TEST_DEV`.
Test 387 requires `CIFS_ALLOW_SAMBA_RESTART=yes` on a dedicated loopback server;
set `CIFS_SAMBA_CONTROL` for an owned controller, otherwise it uses the host
smbd service. Test 406 requires `CIFS_ALLOW_OFFLOAD_TRACE=yes`, function tracing
and an isolated client. These opt-ins were not enabled by the commit.

### Azure Directory-Lease Probes

Only the two committed IDs from the October 6 probes are shown:

| Test | Canary | Preproduction |
| --- | --- | --- |
| cifs/275 | ⏭️ | ⏱️ |
| cifs/355 | ⏭️ | ⏭️ |

Canary did not advertise directory leasing. Preproduction `355` did not
observe reusable enumeration caching; `275` timed out after 630.5 seconds,
including termination grace. Preproduction exercised lease-invalidation code,
so its skip is not proof of absent support.

### Evidence Sources

Raw archives remain local and uncommitted. These paths identify the saved
evidence; they are not portable repository links.

- Samba base: `results-runs/samba422-fresh-cifs-20261006-retry/suite-status.tsv`.
- Samba supplement: `results-runs/samba422-supplement-final-20261006/suite-status.tsv`.
- Test/output hashes: each Samba archive's `source-sha256.json`.
- Azure main: `results-runs/azure-cifs-multiuser-leases-20261006/latest-cifs-status.tsv`.
- Azure probes: `results-runs/azure-canary-directory-leases-20261006` and `results-runs/azure-preprod-directory-leases-20261006`, each with its saved suite status and report.
- Windows base: `results-runs/cifs-windows-coverage-20261001.KJqXtj7R/suite-status.tsv`.
- Windows review: `results-runs/local-tests-review-20261003/matrix.tsv`.
- October 7 repair validation: `results-runs/cifs-test-fixes-20261007/{azure,windows}/suite-status.tsv` and `results-runs/cifs-test-fixes-samba-20261007/samba/suite-status.tsv`. Each archive includes source hashes, raw output, cleanup audits and `SHA256SUMS`.
- ksmbd: complete lists in the [September 25 report](cifs-results-ksmbd-20260925.md).

</details>

**Key:** ✅ pass, ❌ fail, ⏭️ skip, ⏱️ timeout, ⏸️ deferred (not run),
`-` = no recorded result. Skips and deferrals are not passes.

## Complete Per-Test Matrix

| Test | Samba | Azure | Windows | ksmbd |
| --- | --- | --- | --- | --- |
| cifs/001 | ✅ | ❌ | ✅ | ✅ |
| cifs/100 | ✅ | ✅ | ✅ | ✅ |
| cifs/101 | ✅ | ✅ | ✅ | ✅ |
| cifs/102 | ✅ | ✅ | ⏭️ | ✅ |
| cifs/103 | ✅ | ✅ | ✅ | ✅ |
| cifs/104 | ✅ | ✅ | ✅ | ✅ |
| cifs/105 | ✅ | ✅ | ✅ | ⏭️ |
| cifs/106 | ✅ | ✅ | ✅ | ❌ |
| cifs/107 | ✅ | ✅ | ✅ | ⏭️ |
| cifs/108 | ✅ | ✅ | ✅ | ❌ |
| cifs/109 | ✅ | ✅ | ✅ | ✅ |
| cifs/110 | ⏭️ | ⏭️ | ⏭️ | ⏭️ |
| cifs/111 | ✅ | ⏭️ | ✅ | ✅ |
| cifs/112 | ✅ | ✅ | ✅ | ✅ |
| cifs/113 | ✅ | ✅ | ✅ | ✅ |
| cifs/114 | ✅ | ✅ | ✅ | ✅ |
| cifs/115 | ✅ | ✅ | ✅ | ✅ |
| cifs/116 | ✅ | ⏭️ | ✅ | ✅ |
| cifs/117 | ✅ | ✅ | ✅ | ✅ |
| cifs/118 | ✅ | ✅ | ✅ | ✅ |
| cifs/119 | ✅ | ✅ | ✅ | ✅ |
| cifs/120 | ✅ | ❌ | ✅ | ✅ |
| cifs/121 | ✅ | ✅ | ✅ | ✅ |
| cifs/122 | ✅ | ✅ | ✅ | ❌ |
| cifs/123 | ❌ | ❌ | ✅ | ✅ |
| cifs/124 | ✅ | ✅ | ✅ | ✅ |
| cifs/125 | ✅ | ✅ | ✅ | ❌ |
| cifs/126 | ✅ | ❌ | ✅ | ✅ |
| cifs/127 | ✅ | ✅ | ✅ | ✅ |
| cifs/128 | ✅ | ✅ | ✅ | ✅ |
| cifs/129 | ✅ | ✅ | ✅ | ✅ |
| cifs/130 | ✅ | ✅ | ✅ | ✅ |
| cifs/131 | ✅ | ✅ | ✅ | ✅ |
| cifs/132 | ✅ | ✅ | ✅ | ✅ |
| cifs/133 | ❌ | ✅ | ✅ | ✅ |
| cifs/134 | ⏭️ | ⏭️ | ⏭️ | ⏭️ |
| cifs/135 | ✅ | ✅ | ✅ | ✅ |
| cifs/136 | ✅ | ✅ | ✅ | ✅ |
| cifs/137 | ✅ | ✅ | ✅ | ⏭️ |
| cifs/138 | ✅ | ✅ | ✅ | ✅ |
| cifs/139 | ✅ | ✅ | ✅ | ✅ |
| cifs/140 | ✅ | ✅ | ✅ | ✅ |
| cifs/141 | ✅ | ✅ | ✅ | ✅ |
| cifs/142 | ✅ | ✅ | ✅ | ✅ |
| cifs/143 | ✅ | ✅ | ✅ | ✅ |
| cifs/144 | ✅ | ✅ | ✅ | ✅ |
| cifs/145 | ✅ | ✅ | ✅ | ✅ |
| cifs/146 | ✅ | ✅ | ❌ | ✅ |
| cifs/147 | ✅ | ✅ | ✅ | ⏱️ |
| cifs/148 | ❌ | ✅ | ✅ | ✅ |
| cifs/149 | ✅ | ⏭️ | ⏭️ | ⏭️ |
| cifs/150 | ✅ | ✅ | ✅ | ✅ |
| cifs/151 | ❌ | ✅ | ✅ | ✅ |
| cifs/152 | ✅ | ❌ | ✅ | ⏱️ |
| cifs/153 | ✅ | ✅ | ✅ | ✅ |
| cifs/154 | ✅ | ✅ | ✅ | ✅ |
| cifs/155 | ✅ | ✅ | ✅ | ✅ |
| cifs/156 | ✅ | ✅ | ✅ | ✅ |
| cifs/157 | ✅ | ✅ | ✅ | ✅ |
| cifs/158 | ✅ | ⏭️ | ⏭️ | ⏭️ |
| cifs/159 | ✅ | ✅ | ✅ | ✅ |
| cifs/160 | ✅ | ✅ | ✅ | ✅ |
| cifs/161 | ✅ | ✅ | ✅ | ✅ |
| cifs/162 | ✅ | ✅ | ✅ | ✅ |
| cifs/163 | ⏭️ | ⏭️ | ⏭️ | ⏭️ |
| cifs/164 | ✅ | ❌ | ✅ | ✅ |
| cifs/165 | ✅ | ✅ | ✅ | ✅ |
| cifs/166 | ❌ | ✅ | ✅ | ⏭️ |
| cifs/167 | ❌ | ⏭️ | ✅ | ⏭️ |
| cifs/168 | ⏭️ | ⏸️ | ⏸️ | ⏭️ |
| cifs/169 | ✅ | ✅ | ✅ | ✅ |
| cifs/170 | ❌ | ✅ | ✅ | ⏭️ |
| cifs/171 | ❌ | ✅ | ❌ | ⏭️ |
| cifs/172 | ⏭️ | ⏭️ | ✅ | ⏭️ |
| cifs/173 | ✅ | ✅ | ✅ | ✅ |
| cifs/174 | ✅ | ✅ | ✅ | ✅ |
| cifs/175 | ✅ | ✅ | ✅ | ✅ |
| cifs/176 | ⏭️ | ⏭️ | ⏭️ | ⏭️ |
| cifs/177 | ✅ | ✅ | ✅ | ⏭️ |
| cifs/178 | ✅ | ❌ | ⏭️ | ✅ |
| cifs/179 | ❌ | ❌ | ✅ | ✅ |
| cifs/181 | ⏭️ | ⏭️ | ⏭️ | ⏭️ |
| cifs/182 | ✅ | ✅ | ✅ | ✅ |
| cifs/183 | ⏭️ | ✅ | ✅ | ✅ |
| cifs/184 | ✅ | ✅ | ✅ | ✅ |
| cifs/185 | ⏭️ | ⏭️ | ⏭️ | ⏭️ |
| cifs/186 | ✅ | ✅ | ✅ | ✅ |
| cifs/187 | ✅ | ✅ | ✅ | ✅ |
| cifs/188 | ⏭️ | ✅ | ✅ | ✅ |
| cifs/189 | ⏭️ | ⏭️ | ⏭️ | ⏭️ |
| cifs/190 | ✅ | ✅ | ✅ | ✅ |
| cifs/191 | ❌ | ❌ | ❌ | ⏭️ |
| cifs/192 | ✅ | ❌ | ❌ | ❌ |
| cifs/193 | ✅ | ✅ | ✅ | ✅ |
| cifs/194 | ❌ | ❌ | ❌ | ❌ |
| cifs/195 | ✅ | ✅ | ✅ | ✅ |
| cifs/196 | ✅ | ✅ | ✅ | ✅ |
| cifs/197 | ⏭️ | ⏭️ | ⏭️ | ⏭️ |
| cifs/198 | ✅ | ✅ | ❌ | ❌ |
| cifs/199 | ✅ | ✅ | ✅ | ✅ |
| cifs/200 | ✅ | ✅ | ✅ | ✅ |
| cifs/201 | ✅ | ✅ | ✅ | ✅ |
| cifs/202 | ✅ | ✅ | ✅ | ✅ |
| cifs/203 | ✅ | ⏭️ | ⏭️ | ⏭️ |
| cifs/206 | ✅ | ❌ | ⏭️ | ✅ |
| cifs/207 | ❌ | ❌ | ✅ | ✅ |
| cifs/208 | ✅ | ✅ | ✅ | ✅ |
| cifs/209 | ✅ | ✅ | ✅ | ✅ |
| cifs/210 | ✅ | ✅ | ✅ | ✅ |
| cifs/211 | ✅ | ✅ | ✅ | ✅ |
| cifs/212 | ✅ | ✅ | ✅ | ✅ |
| cifs/213 | ✅ | ✅ | ✅ | ✅ |
| cifs/214 | ✅ | ✅ | ✅ | ✅ |
| cifs/215 | ✅ | ✅ | ✅ | ✅ |
| cifs/216 | ✅ | ❌ | ❌ | ✅ |
| cifs/217 | ✅ | ✅ | ✅ | ✅ |
| cifs/218 | ✅ | ✅ | ✅ | ✅ |
| cifs/219 | ✅ | ✅ | ✅ | ✅ |
| cifs/220 | ⏭️ | ⏭️ | ⏭️ | ⏭️ |
| cifs/221 | ❌ | ✅ | ❌ | ✅ |
| cifs/222 | ⏭️ | ✅ | ✅ | ✅ |
| cifs/223 | ✅ | ✅ | ✅ | ✅ |
| cifs/224 | ⏭️ | ⏭️ | ⏭️ | ⏭️ |
| cifs/225 | ⏭️ | ❌ | ❌ | ⏭️ |
| cifs/226 | ✅ | ⏭️ | ✅ | ✅ |
| cifs/227 | ✅ | ⏭️ | ✅ | ✅ |
| cifs/228 | ✅ | ✅ | ✅ | ✅ |
| cifs/229 | ⏭️ | ⏭️ | ⏭️ | ⏭️ |
| cifs/230 | ✅ | ✅ | ✅ | ✅ |
| cifs/231 | ✅ | ✅ | ✅ | ✅ |
| cifs/232 | ✅ | ❌ | ✅ | ⏭️ |
| cifs/233 | ✅ | ⏭️ | ✅ | ✅ |
| cifs/234 | ⏭️ | ⏭️ | ⏭️ | ⏭️ |
| cifs/235 | ✅ | ✅ | ✅ | ✅ |
| cifs/236 | ✅ | ✅ | ✅ | ✅ |
| cifs/237 | ✅ | ✅ | ✅ | ✅ |
| cifs/238 | ❌ | ❌ | ❌ | ❌ |
| cifs/239 | ✅ | ✅ | ✅ | ✅ |
| cifs/240 | ⏭️ | ⏭️ | ⏭️ | ⏭️ |
| cifs/241 | ✅ | ✅ | ✅ | ✅ |
| cifs/242 | ✅ | ✅ | ✅ | ✅ |
| cifs/243 | ✅ | ✅ | ✅ | ✅ |
| cifs/244 | ✅ | ✅ | ⏭️ | ⏭️ |
| cifs/245 | ✅ | ✅ | ✅ | ✅ |
| cifs/246 | ✅ | ✅ | ✅ | ✅ |
| cifs/247 | ⏭️ | ✅ | ✅ | ✅ |
| cifs/248 | ⏭️ | ⏭️ | ⏭️ | ⏭️ |
| cifs/249 | ✅ | ✅ | ✅ | ✅ |
| cifs/250 | ✅ | ✅ | ✅ | ✅ |
| cifs/251 | ✅ | ✅ | ❌ | ✅ |
| cifs/252 | ⏭️ | ⏭️ | ⏭️ | ⏭️ |
| cifs/253 | ⏭️ | ✅ | ✅ | ✅ |
| cifs/254 | ✅ | ⏭️ | ⏭️ | ✅ |
| cifs/255 | ✅ | ⏭️ | ✅ | ✅ |
| cifs/256 | ✅ | ⏱️ | ✅ | ✅ |
| cifs/257 | ✅ | ✅ | ✅ | ✅ |
| cifs/258 | ✅ | ✅ | ✅ | ✅ |
| cifs/259 | ✅ | ✅ | ✅ | ✅ |
| cifs/260 | ✅ | ✅ | ✅ | ✅ |
| cifs/261 | ✅ | ✅ | ✅ | ✅ |
| cifs/262 | ✅ | ✅ | ✅ | ✅ |
| cifs/263 | ✅ | ✅ | ✅ | ✅ |
| cifs/264 | ✅ | ✅ | ✅ | ✅ |
| cifs/265 | ✅ | ✅ | ✅ | ✅ |
| cifs/266 | ❌ | ✅ | ✅ | ✅ |
| cifs/267 | ✅ | ✅ | ✅ | ✅ |
| cifs/268 | ✅ | ✅ | ✅ | ✅ |
| cifs/269 | ✅ | ✅ | ✅ | ✅ |
| cifs/270 | ✅ | ✅ | ✅ | ✅ |
| cifs/271 | ✅ | ✅ | ✅ | ✅ |
| cifs/272 | ✅ | ✅ | ✅ | ✅ |
| cifs/273 | ✅ | ✅ | ✅ | ✅ |
| cifs/274 | ✅ | ✅ | ✅ | ✅ |
| cifs/275 | ❌ | ⏱️ | ❌ | ✅ |
| cifs/276 | ✅ | ✅ | ✅ | ✅ |
| cifs/277 | ✅ | ✅ | ✅ | ✅ |
| cifs/278 | ✅ | ✅ | ✅ | ✅ |
| cifs/279 | ✅ | ✅ | ✅ | ✅ |
| cifs/280 | ✅ | ✅ | ✅ | ✅ |
| cifs/281 | ⏭️ | ✅ | ✅ | ✅ |
| cifs/282 | ✅ | ✅ | ✅ | ✅ |
| cifs/283 | ✅ | ✅ | ✅ | ✅ |
| cifs/284 | ✅ | ✅ | ✅ | ✅ |
| cifs/285 | ✅ | ✅ | ✅ | ✅ |
| cifs/286 | ✅ | ✅ | ✅ | ✅ |
| cifs/287 | ✅ | ✅ | ✅ | ✅ |
| cifs/288 | ✅ | ✅ | ✅ | ✅ |
| cifs/289 | ⏭️ | ⏭️ | ⏭️ | ⏭️ |
| cifs/290 | ✅ | ✅ | ✅ | ✅ |
| cifs/291 | ✅ | ✅ | ✅ | ✅ |
| cifs/292 | ✅ | ✅ | ✅ | ✅ |
| cifs/293 | ✅ | ✅ | ✅ | ✅ |
| cifs/294 | ✅ | ✅ | ✅ | ✅ |
| cifs/295 | ✅ | ✅ | ✅ | ✅ |
| cifs/296 | ✅ | ✅ | ✅ | ✅ |
| cifs/297 | ⏭️ | ✅ | ✅ | ✅ |
| cifs/298 | ✅ | ✅ | ✅ | ✅ |
| cifs/299 | ✅ | ✅ | ✅ | ✅ |
| cifs/300 | ✅ | ✅ | ✅ | ✅ |
| cifs/301 | ✅ | ✅ | ✅ | ✅ |
| cifs/302 | ✅ | ✅ | ✅ | ✅ |
| cifs/303 | ✅ | ✅ | ✅ | ✅ |
| cifs/304 | ✅ | ✅ | ❌ | ✅ |
| cifs/305 | ✅ | ✅ | ✅ | ✅ |
| cifs/306 | ✅ | ✅ | ✅ | ✅ |
| cifs/307 | ✅ | ✅ | ✅ | ✅ |
| cifs/308 | ✅ | ✅ | ✅ | ✅ |
| cifs/310 | ❌ | ❌ | ❌ | ✅ |
| cifs/311 | ✅ | ⏱️ | ✅ | ✅ |
| cifs/312 | ✅ | ✅ | ✅ | ✅ |
| cifs/313 | ✅ | ⏭️ | ⏭️ | ⏭️ |
| cifs/314 | ✅ | ⏭️ | ⏭️ | ⏭️ |
| cifs/315 | ⏭️ | ⏭️ | ⏭️ | - |
| cifs/316 | ✅ | ⏭️ | ⏭️ | ⏭️ |
| cifs/317 | ❌ | ⏭️ | ⏭️ | ⏭️ |
| cifs/319 | ✅ | ⏭️ | ⏭️ | ⏭️ |
| cifs/320 | ✅ | ⏭️ | ⏭️ | - |
| cifs/321 | ✅ | ⏭️ | ⏭️ | ⏭️ |
| cifs/322 | ✅ | ⏭️ | ⏭️ | ⏭️ |
| cifs/323 | ✅ | ⏭️ | ⏭️ | - |
| cifs/324 | ✅ | ⏭️ | ⏭️ | - |
| cifs/326 | ✅ | ⏭️ | ⏭️ | - |
| cifs/327 | ✅ | ⏭️ | ⏭️ | - |
| cifs/328 | ✅ | ⏭️ | ⏭️ | - |
| cifs/329 | ✅ | ⏭️ | ⏭️ | - |
| cifs/330 | ✅ | ⏭️ | ⏭️ | - |
| cifs/331 | ✅ | ⏭️ | ⏭️ | - |
| cifs/332 | ✅ | ⏭️ | ⏭️ | - |
| cifs/333 | ✅ | ⏭️ | ⏭️ | - |
| cifs/334 | ✅ | ✅ | ✅ | ✅ |
| cifs/335 | ✅ | ❌ | ❌ | ✅ |
| cifs/336 | ❌ | ✅ | ✅ | ✅ |
| cifs/337 | ✅ | ✅ | ✅ | ✅ |
| cifs/338 | ✅ | ✅ | ✅ | ✅ |
| cifs/339 | ✅ | ✅ | ✅ | ✅ |
| cifs/340 | ✅ | ✅ | ✅ | ✅ |
| cifs/341 | ✅ | ❌ | ❌ | ❌ |
| cifs/342 | ✅ | ✅ | ✅ | ✅ |
| cifs/344 | ✅ | ✅ | ✅ | ✅ |
| cifs/346 | ✅ | ✅ | ✅ | ✅ |
| cifs/347 | ✅ | ✅ | ✅ | ❌ |
| cifs/348 | ✅ | ✅ | ❌ | ✅ |
| cifs/350 | ✅ | ✅ | ✅ | ✅ |
| cifs/351 | ✅ | ❌ | ❌ | ✅ |
| cifs/352 | ✅ | ✅ | ✅ | ✅ |
| cifs/353 | ✅ | ✅ | ✅ | ✅ |
| cifs/354 | ❌ | ✅ | ✅ | ❌ |
| cifs/355 | ✅ | ⏭️ | ✅ | - |
| cifs/356 | ✅ | ❌ | ⏭️ | - |
| cifs/357 | ✅ | ✅ | ✅ | ✅ |
| cifs/358 | ❌ | ❌ | ✅ | ❌ |
| cifs/359 | ✅ | ✅ | ✅ | ✅ |
| cifs/361 | ✅ | ✅ | ✅ | ✅ |
| cifs/362 | ✅ | ✅ | ✅ | ✅ |
| cifs/363 | ✅ | ✅ | ✅ | ✅ |
| cifs/364 | ✅ | ✅ | ✅ | ✅ |
| cifs/365 | ✅ | ✅ | ✅ | ✅ |
| cifs/366 | ✅ | ✅ | ✅ | ✅ |
| cifs/367 | ✅ | ✅ | ✅ | ✅ |
| cifs/368 | ✅ | ✅ | ✅ | ✅ |
| cifs/369 | ✅ | ✅ | ✅ | ✅ |
| cifs/370 | ✅ | ✅ | ✅ | ✅ |
| cifs/371 | ✅ | ✅ | ✅ | ✅ |
| cifs/372 | ✅ | ✅ | ✅ | ✅ |
| cifs/373 | ✅ | ✅ | ✅ | ✅ |
| cifs/374 | ✅ | ✅ | ✅ | ✅ |
| cifs/375 | ✅ | ✅ | ✅ | ✅ |
| cifs/376 | ❌ | ❌ | ❌ | ✅ |
| cifs/379 | ✅ | ⏭️ | ⏭️ | - |
| cifs/380 | ✅ | ✅ | ❌ | ❌ |
| cifs/381 | ✅ | ✅ | ✅ | ✅ |
| cifs/382 | ✅ | ✅ | ✅ | ❌ |
| cifs/383 | ✅ | ✅ | ✅ | ✅ |
| cifs/384 | ✅ | ✅ | ✅ | ✅ |
| cifs/386 | ✅ | ✅ | ✅ | ✅ |
| cifs/387 | ✅ | ⏭️ | ⏭️ | - |
| cifs/388 | ✅ | ❌ | ❌ | ❌ |
| cifs/389 | ✅ | ✅ | ✅ | ✅ |
| cifs/390 | ✅ | ⏭️ | ❌ | - |
| cifs/392 | ✅ | ✅ | ✅ | - |
| cifs/393 | ❌ | ❌ | ✅ | ✅ |
| cifs/394 | ❌ | ✅ | ✅ | ❌ |
| cifs/396 | ✅ | ⏭️ | ⏭️ | ⏭️ |
| cifs/398 | ✅ | ✅ | ✅ | ✅ |
| cifs/399 | ✅ | ✅ | ✅ | ✅ |
| cifs/400 | ✅ | ✅ | ✅ | ✅ |
| cifs/403 | ✅ | ✅ | ✅ | ✅ |
| cifs/404 | ✅ | ⏭️ | ⏭️ | - |
| cifs/406 | ✅ | ✅ | ⏭️ | - |
| cifs/407 | ✅ | ⏭️ | ✅ | - |
