# CIFS Failure and Skip Report

**Updated:** 2026-10-08 | **Results through:** 2026-10-08

[Results overview](cifs-results_latest.md) | [Complete test matrix](cifs-results-20261006.md#complete-per-test-matrix)

This report explains non-passing results for the same **290 committed test
IDs** as the results matrix. Untracked tests are excluded. Passing tests remain
in the complete matrix and are not repeated here.

Reasons below describe recorded assertions, errors or prerequisite checks,
not necessarily proven server bugs. Skips do not establish that a server lacks
a feature in every configuration. Runs used different source versions and
fixtures; tests `192`, `194`, `225`, `236` and `275` have pending local repairs.
The October 7 validation reran repaired tests `103`, `116`, `157`, `171`,
`216`, `251` and `310` on all four servers. Their observed outcomes are merged
into the matrix, and fresh reasons replace older diagnostics for these tests.
The October 8 ksmbd batch added the 21 previously missing outcomes: one pass,
one failure, and 19 skips. Earlier raw evidence is unchanged.

**Key:** ❌ fail, ⏭️ skip, ⏱️ timeout, ⏸️ deliberately deferred (not run).
Missing results are not skips.

## Summary

| Server | ❌ Fail | ⏭️ Skip | ⏱️ Timeout | ⏸️ Deferred | Listed Results |
| --- | ---: | ---: | ---: | ---: | ---: |
| Samba 4.22.11 | 24 | 27 | 0 | 0 | 51 |
| Azure | 26 | 54 | 3 | 1 | 84 |
| Windows | 22 | 49 | 0 | 1 | 72 |
| ksmbd | 17 | 60 | 2 | 0 | 79 |

All 290 committed IDs now have recorded outcomes on ksmbd. The 19 new skips
are recorded prerequisite or policy outcomes, not converted missing results.

[Test-Issue Review](#test-issue-review) | [Samba](#samba) | [Azure](#azure) | [Windows](#windows) | [ksmbd](#ksmbd) | [Evidence](#evidence)

## Test-Issue Review

The seven repaired test sources and their offline regression checks are included
with these reports. All **15 offline regression checks passed**, followed by the
latest four-server validation: **28 outcomes,
18 PASS, 8 FAIL and 2 SKIP**, with no timeouts. Expected success output was not
changed. The current results replace prior observations, not the archived raw
evidence; they do not establish that every remaining failure is a server defect.

[Per-test live results and limitations](cifs-results-20261006.md#october-7-repair-validation).
ksmbd used a temporary alternate-port fixture and loopback default-port forwarder
without interrupting host Samba. All seven tests now have fresh ksmbd results;
those results remain unchanged. The October 8 batch adds the previously missing
IDs; other ksmbd rows still describe September 25 sources.

| Test | Local Repair | What Still Fails |
| --- | --- | --- |
| [tests/cifs/116](tests/cifs/116) | Correct the quoted filename used to report the punch-hole error. | Azure now skips the explicitly unsupported operation after the follow-up classification fix below; Samba, Windows and ksmbd pass. |
| [tests/cifs/157](tests/cifs/157) | Read the test share's Flush counter instead of the first global counter; require a successful write and `fsync`; use a test-owned mount and the existing cleanup helper. | Write/fsync errors, a disappearing counter or no Flush increment remain failures. Other activity on the same share can still affect its aggregate counter. |
| [tests/cifs/216](tests/cifs/216) | Compare survivor contents as exact bytes; retain bounded hex diagnostics; reject failed fixture writes immediately. | Missing survivors, NULs, truncation, unexpected line endings and other content differences remain failures. |
| [tests/cifs/251](tests/cifs/251) | Stop ignoring creation and stat errors after a successful `idsfromsid` mount. | I/O and permission errors now fail explicitly instead of allowing a misleading success message. |
| [tests/cifs/310](tests/cifs/310) | Replace lossy shell content comparisons with bounded binary reads and exact-byte diagnostics. | Worker errors, missing files and byte mismatches remain failures; no retries or assertion relaxation were added. |

Subsequent source review found three further test-side issues. All three
follow-up changes were included in the latest four-server runs above.

| Test | Confirmed Test Issue | Follow-Up Repair |
| --- | --- | --- |
| [tests/cifs/103](tests/cifs/103) | Phase 1 assumes shared sockets even when the profile forces `nosharesock`. This is a fixture mismatch, not evidence of incorrect server behavior. | Guard incompatible global profiles. With only `nosharesock` removed in a dedicated per-test profile, both assertions ran and passed on all four servers. |
| [tests/cifs/116](tests/cifs/116) | The documented unsupported-operation skip policy missed the exact recorded `keep size mode is unsupported` message; it also treated `EINVAL` as proof of missing support. | Recognize the recorded unsupported-mode response in the C locale. Invalid arguments, I/O errors, permission errors and tool errors remain failures. The new live Azure outcome is SKIP, not PASS. |
| [tests/cifs/171](tests/cifs/171) | Recovery paths forced `rc=0`, rename workers shared `$$`-based temporary names, failed child exits were ignored, and zero-match counts became two zeros. | Preserve recovery errors, use worker-specific `BASHPID` names, propagate failed worker exits and keep counts numeric. Stress thresholds and expected output are unchanged; the original filesystem errors are not claimed resolved. |

The regression suite uses local temporary files, synthetic counters and injected
errors, not SMB shares:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B tools/test_cifs_regressions.py -v
```

The offline checks include cases that must fail and exact prerequisite/unsupported
classification. The live runs used namespace isolation and verified source hashes,
xUnit outcomes and cleanup. No counter reset, client-module reload or changes
to existing server configurations were performed. Temporary Samba 4.22.11 and
ksmbd fixtures were started and removed; the ksmbd server module was loaded only
for its owned fixture and then unloaded. Existing repairs to `192`, `194`, `225`,
`236` and `275` were left untouched and were not rerun.

Other dispositions:

- **Remaining test-quality limits:** `171` can leak shell redirection errors into
	expected output even when its RC tolerance permits continuing; this was
	reproduced locally. `310` requires an OplockBreaks increment without proving a
	lease grant or a required break, so its Samba counter-only failure is not
	conclusive server evidence. `251` still has warning-only ACL assertions and
	ignored query errors; its PASS is not full ACL correctness certification.
	These issues were not changed in the archived runs or these focused repairs.
- **Setup issues:** `225`, `232` and `335` already source the required helper
	library in the current tree, and the called helpers exist. Their older Azure
	missing-helper attempts require a correctly packaged runner and a fresh run,
	not a weaker filesystem assertion. `103` now guards its incompatible socket
	fixture; `317` still needs distinct DFS backends. No server configuration was
	changed in the follow-up review.
- **Mixed evidence:** `171` has expected concurrent pathname races, but also
	invalid-argument errors. Its proven worker/error-handling defects were repaired
	as described above. It still fails on Samba; Windows now fails on stale-file-handle
	output, Azure passes, and ksmbd skips with leases disabled. Further isolation
	is needed before attributing those filesystem errors.
- **Unresolved client/server behavior:** notification, locking, cache-coherency,
	xattr, protocol/security and permission failures remain as recorded. These
	logs do not reliably assign every failure to the server rather than the client.
	No expected output was changed to accept those failures.
- **Prerequisites and policy:** missing Kerberos/DFS/snapshot fixtures, unsupported
	features, opt-in safety gates, resource limits and deliberate deferrals were
	not bypassed. Status changes reflect new live outcomes; unsupported Azure
	punch-hole remains explicitly a skip, not a pass.

## Samba

Samba 4.22.11, October 6 full run plus the final supplement, with October 7
repair-validation overrides for `103`, `116`, `157`, `171`, `216`, `251` and `310`.
Only `171` and `310` failed in the latest batch; `103` now passes. The nine earlier
skips that subsequently passed are
not listed. Reasons come from saved per-test output and ledger records.

### Failures

| Test | Result | Recorded Reason |
| --- | --- | --- |
| cifs/123 | ❌ | The expected holder PID/file entry was not found in `/proc/fs/cifs/open_files`. |
| cifs/133 | ❌ | Modification time did not refresh immediately with `actimeo=0`; both timestamps were equal. |
| cifs/148 | ❌ | A new directory entry remained invisible after `acdirmax` expired. |
| cifs/151 | ❌ | File size remained 5 bytes after an append. |
| cifs/166 | ❌ | The lease-break test reported 200 files missing updates. |
| cifs/167 | ❌ | Directory entries did not refresh after remote modifications. |
| cifs/170 | ❌ | Expected two `RH` leases after a second open; observed two `RHW` leases. |
| cifs/171 | ❌ | October 7 latest run: concurrent stress emitted invalid-argument errors, recovery returned errors, and workers exceeded the unchanged RC tolerance (3 errors versus 2 allowed). The repaired test now fails explicitly rather than ending with a misleading OK line. |
| cifs/179 | ❌ | The holder did not expose the expected `open_files` entry. |
| cifs/191 | ❌ | Single-channel workload failed at `fsync` with `ENOSPC` (no space left on device); multichannel performance was not established. |
| cifs/194 | ❌ | `mount.cifs` did not reject an oversized password as expected. This is a client-helper negative-path check. |
| cifs/207 | ❌ | The holder did not expose the expected `open_files` entry. |
| cifs/221 | ❌ | Mode did not persist after remount: expected `755`, observed `1744`. |
| cifs/238 | ❌ | The expected local `IN_CREATE` event was absent. The script attributes this to the client notification path; the log alone does not prove the exact cause. |
| cifs/266 | ❌ | Cross-mount read returned `writt` instead of `written_by_B`. |
| cifs/275 | ❌ | Directory leases did not reduce `QueryDirectories`: 102 with leases versus 102 without. |
| cifs/310 | ❌ | October 7: shared-file chunks, directory contents and cross-mount checksums passed, but `OplockBreaks` stayed 0 before and after the workload. This replaces the older worker-`EAGAIN` diagnostic; the remaining counter assertion failed. |
| cifs/317 | ❌ | Target 1 fixture data was visible on target 2; the test requires distinct DFS backends. |
| cifs/336 | ❌ | The requested mount returned error 95, operation not supported; no filesystem was attached. |
| cifs/354 | ❌ | A held file descriptor returned stale data after replacement through another mount. |
| cifs/358 | ❌ | A competing process acquired a supposedly held lock during the initial conflict check, before disconnect. This does not establish lock loss after reconnect. |
| cifs/376 | ❌ | The SMB 3.0 signing mount returned error 95 after SMB 3.1.1 combinations succeeded. |
| cifs/393 | ❌ | The SMB 3.0 mount returned error 95 after earlier signing/encryption combinations succeeded. |
| cifs/394 | ❌ | The lock-query helper received an unexpected `F_GETLK` lock type and aborted. This is a userspace assertion failure, not a kernel crash. |

### Skips

| Test | Result | Recorded Reason |
| --- | --- | --- |
| cifs/110 | ⏭️ | `prefixpath` appeared unsupported or ignored by the tested client/server pair. |
| cifs/134 | ⏭️ | Reported block size was 1,024 bytes, not the requested 262,144. |
| cifs/163 | ⏭️ | Advisory-lock/open-share-mode mapping was not enforced. |
| cifs/168 | ⏭️ | The test reached its write target without triggering `ENOSPC`. |
| cifs/172 | ⏭️ | No initial leases were observed. |
| cifs/176 | ⏭️ | Mounting with `compress` failed. |
| cifs/181 | ⏭️ | The mount helper accepted oversized options. |
| cifs/183 | ⏭️ | Record locks were not enforced. |
| cifs/185 | ⏭️ | The mount helper accepted unknown options without `sloppy`. |
| cifs/188 | ⏭️ | Record locks were not enforced. |
| cifs/189 | ⏭️ | The server denied anonymous `sec=none` access. |
| cifs/197 | ⏭️ | The server stripped the setuid bit. |
| cifs/220 | ⏭️ | `setfacl` was unsupported on this mount. |
| cifs/222 | ⏭️ | Symlink creation was unsupported on this mount. |
| cifs/224 | ⏭️ | `SEEK_DATA`/`SEEK_HOLE` was unsupported by the tested server/kernel pair. |
| cifs/225 | ⏭️ | The requested WSL reparse node type was unsupported. |
| cifs/229 | ⏭️ | No tested NFS reparse special-file types were supported. |
| cifs/234 | ⏭️ | Snapshot enumeration found no working method in this fixture. |
| cifs/240 | ⏭️ | The running kernel lacked `CONFIG_CIFS_SWAP`. |
| cifs/247 | ⏭️ | Symlink creation was unsupported on this mount. |
| cifs/248 | ⏭️ | SMB3 compression was unavailable in the tested server/kernel configuration. |
| cifs/252 | ⏭️ | No tested `mknod` operations were supported on this mount. |
| cifs/253 | ⏭️ | Symlinks were unsupported on this mount. |
| cifs/281 | ⏭️ | Symlinks were unsupported on this mount. |
| cifs/289 | ⏭️ | `drop_dir_cache` was not writable. |
| cifs/297 | ⏭️ | Symlink creation failed. |
| cifs/315 | ⏭️ | Global DFS cache flushing was not authorized with `CIFS_ALLOW_DFS_CACHE_FLUSH=yes`. |

## Azure

Latest recorded attempts across the main Azure Files endpoint and the October 6
canary/preproduction probes. This is not a single-endpoint full-suite run.
The October 7 main-endpoint repair run supplies fresh failures for `216` and
`310`, and the unsupported-operation skip for `116`; `103`, `157`, `171` and
`251` passed. Preproduction supplies `275` and `355`;
the earlier main ledger supplies the other rows. Failure messages are qualified
by full logs where the final message hides an earlier setup or worker error.

### Failures

| Test | Result | Recorded Reason |
| --- | --- | --- |
| cifs/001 | ❌ | Clone returned operation not supported, producing an expected-output mismatch. |
| cifs/120 | ❌ | The lock holder did not report acquiring its lock; the exact lock errno was not established. |
| cifs/123 | ❌ | The expected holder PID/file entry was absent from `/proc/fs/cifs/open_files`. |
| cifs/126 | ❌ | Modification time did not refresh after the 10-second attribute-cache TTL. |
| cifs/152 | ❌ | Long-path workload returned `TOTAL_ERR 2` (`ENOENT`), outside the accepted results. |
| cifs/164 | ❌ | Creating the first hardlink returned operation not supported. |
| cifs/178 | ❌ | Initial `setfattr` failed, before the clone-range behavior could be validated. |
| cifs/179 | ❌ | The holder did not expose the expected `open_files` entry. |
| cifs/191 | ❌ | Three-channel throughput was 8.82 MB/s versus 9.98 MB/s for one channel, an 11.62% regression in this run. |
| cifs/192 | ❌ | Latest October 5 retry returned `None` instead of the expected 4 MiB recovery read; the worker exited before the next reconnect barrier. |
| cifs/194 | ❌ | `mount.cifs` did not reject the oversized password as expected; a client-helper negative-path failure. |
| cifs/206 | ❌ | Initial `setfattr` failed, before clone behavior could be validated. |
| cifs/207 | ❌ | The holder did not expose the expected `open_files` entry. |
| cifs/216 | ❌ | October 7 latest run: exact comparison of survivor `del_72` failed at byte 1, but the immediate bounded hex reread showed the expected `content_72` plus newline. The comparison and diagnostic read disagree; persistent stored-data corruption and client/server attribution are not established. |
| cifs/225 | ❌ | Required `_cifs_test_*` helpers were not found, followed by a WSL reparse mismatch. This attempt has a setup failure and is not clean evidence of a server reparse defect. |
| cifs/232 | ❌ | Required `_cifs_test_*` helpers were not found; syncing the resulting empty fixture path failed. The intended cache check was not established. |
| cifs/238 | ❌ | The expected local `IN_CREATE` event was absent, although modify, rename and delete events were captured. |
| cifs/310 | ❌ | October 7: all ten mounts, shared-file chunks and 100 directory names passed. Bounded binary reads for sample files from mounts 1-5 returned entirely NUL bytes instead of the written text; five exact-content comparisons failed. No shell NUL-stripping is involved in this attempt. |
| cifs/335 | ❌ | Required `_cifs_test_*` helpers were not found before the numeric SID mapping mismatch. Do not attribute this attempt solely to server SID handling. |
| cifs/341 | ❌ | Creating the binary `user.test_attr` xattr with `XATTR_CREATE` returned `EINVAL`; this is not the Windows ACL-write failure. |
| cifs/351 | ❌ | The extended-attribute lifecycle worker returned `EINVAL`. |
| cifs/356 | ❌ | Multiuser I/O did not create a separate SMB session. The tested older source reused the same server credentials for both UIDs; the distinct-credential repair passed Samba but was not rerun here. |
| cifs/358 | ❌ | The recovery `pwrite` returned `EAGAIN` after the disconnect attempt. The generic lock-recovery failure message does not establish lost locks. |
| cifs/376 | ❌ | SMB 2.1 mount returned permission denied after the SMB 3.1.1 and 3.0 combinations succeeded. |
| cifs/388 | ❌ | Hardlink creation failed; later permission checks were not reached. |
| cifs/393 | ❌ | Hardlink creation on the encrypted mount returned operation not supported. This does not establish an encryption defect. |

### Skips

| Test | Result | Recorded Reason |
| --- | --- | --- |
| cifs/110 | ⏭️ | `prefixpath` appeared unsupported or ignored by this client/server pair. |
| cifs/111 | ⏭️ | Hardlinks were unsupported on this share. |
| cifs/116 | ⏭️ | October 7 latest run: punch-hole returned `keep size mode is unsupported`. The corrected unsupported-operation classification now produces `sparse/zero-data not supported on this server/share`; this is a live skip, not a passing sparse-file check. |
| cifs/134 | ⏭️ | Reported block size was 65,536 bytes, not the requested 262,144. |
| cifs/149 | ⏭️ | The dedicated DNS fixture hook `CIFS149_DNS_HOOK` was not configured. |
| cifs/158 | ⏭️ | `CIFS_USER2` was not configured. |
| cifs/163 | ⏭️ | Advisory-lock/open-share-mode mapping was not enforced. |
| cifs/167 | ⏭️ | No directory-leasing capability was advertised. |
| cifs/172 | ⏭️ | No initial leases were observed. |
| cifs/176 | ⏭️ | Mounting with `compress` failed. |
| cifs/181 | ⏭️ | The mount helper accepted oversized options. |
| cifs/185 | ⏭️ | The mount helper accepted unknown options without `sloppy`. |
| cifs/189 | ⏭️ | The `sec=none` mount returned error 22, invalid argument. |
| cifs/197 | ⏭️ | The server stripped the setuid bit. |
| cifs/203 | ⏭️ | The multiuser mount failed. |
| cifs/220 | ⏭️ | `setfacl` was unsupported on this mount. |
| cifs/224 | ⏭️ | The prerequisite punch-hole operation was unsupported. |
| cifs/226 | ⏭️ | Zero-range allocation was unsupported. |
| cifs/227 | ⏭️ | Punch-hole allocation was unsupported. |
| cifs/229 | ⏭️ | No tested NFS reparse special-file types were supported. |
| cifs/233 | ⏭️ | Neither collapse-range nor insert-range was supported. |
| cifs/234 | ⏭️ | Snapshot enumeration found no working method in this fixture. |
| cifs/240 | ⏭️ | The running kernel lacked `CONFIG_CIFS_SWAP`. |
| cifs/248 | ⏭️ | SMB3 compression was unavailable in this server/kernel configuration. |
| cifs/252 | ⏭️ | No tested `mknod` operations were supported. |
| cifs/254 | ⏭️ | Setting `user.*` xattrs was unsupported on this mount. |
| cifs/255 | ⏭️ | Hardlinks were unsupported on this mount. |
| cifs/289 | ⏭️ | `drop_dir_cache` was not writable. |
| cifs/313 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. |
| cifs/314 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. |
| cifs/315 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. |
| cifs/316 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. |
| cifs/317 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. |
| cifs/319 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. |
| cifs/320 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. |
| cifs/321 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. |
| cifs/322 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. |
| cifs/323 | ⏭️ | Kerberos fixture `CIFS_KRB5_REALM` was not configured. |
| cifs/324 | ⏭️ | Kerberos fixture `CIFS_KRB5_REALM` was not configured. |
| cifs/326 | ⏭️ | Kerberos fixture `CIFS_KRB5_REALM` was not configured. |
| cifs/327 | ⏭️ | Kerberos fixture `CIFS_KRB5_REALM` was not configured. |
| cifs/328 | ⏭️ | Kerberos fixture `CIFS_KRB5_REALM` was not configured. |
| cifs/329 | ⏭️ | Kerberos fixture `CIFS_KRB5_REALM` was not configured. |
| cifs/330 | ⏭️ | Kerberos fixture `CIFS_KRB5_REALM` was not configured. |
| cifs/331 | ⏭️ | Kerberos fixture `CIFS_KRB5_REALM` was not configured. |
| cifs/332 | ⏭️ | Kerberos fixture `CIFS_KRB5_REALM` was not configured. |
| cifs/333 | ⏭️ | Kerberos fixture `CIFS_KRB5_REALM` was not configured. |
| cifs/355 | ⏭️ | Preproduction did not grant reusable directory-enumeration caching; it did exercise lease-invalidation code, so the skip does not prove absent support. |
| cifs/379 | ⏭️ | A snapshot-enabled share with existing snapshots was required. |
| cifs/387 | ⏭️ | Dedicated-server restart was not authorized with `CIFS_ALLOW_SAMBA_RESTART=yes`. |
| cifs/390 | ⏭️ | The server did not support the requested SMB3 POSIX extensions. |
| cifs/396 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. |
| cifs/404 | ⏭️ | Kerberos fixture `CIFS_KRB5_REALM` was not configured. |
| cifs/407 | ⏭️ | File-compression ioctls were unsupported. |

### Timeouts and Deferrals

Timeouts identify the runner deadline, not an established root cause of the
unfinished workload. They remain distinct from test assertion failures.

| Test | Result | Recorded Reason |
| --- | --- | --- |
| cifs/168 | ⏸️ | The ENOSPC workload would fill almost all free share space; separate cost/availability approval was unavailable. It was not executed. |
| cifs/256 | ⏱️ | Main-endpoint run exceeded its bounded deadline; elapsed time including termination was 1,930.4 seconds. Namespace cleanup was audited. |
| cifs/275 | ⏱️ | Preproduction run exceeded the 600-second limit plus termination grace, 630.5 seconds total. This replaces the main endpoint's skip and is not attributed to that endpoint. |
| cifs/311 | ⏱️ | Main-endpoint run exceeded its bounded deadline; elapsed time including termination was 1,930.3 seconds. Namespace cleanup was audited. |

## Windows

Statuses match the current matrix: the later October 1 coverage run with
October 3 review and October 7 repair-validation overrides. The October 7 run
used the published IP-based Windows profile, not the obsolete hostname profile.
The later October 1 coverage run's raw logs were not accessible for this report.
**Earlier October 1 reasons must not be assumed to describe a later run's exact
failure or skip.**

The Evidence column distinguishes:

- **Oct 7:** Fresh repair-validation output; `103`, `116` and `157` passed,
	while `171`, `216`, `251` and `310` have directly verified failure diagnostics.
- **Oct 3:** Directly read review output for the attempt used by the matrix.
- **Earlier Oct 1:** Published functional-run finding for the same test and
	outcome, offered as historical context only; later-run reason unverified.
- **Unavailable:** Current outcome is known, but no matching reason is
	available from the accessible evidence.
- **Run policy:** Deliberate capacity-safety deferral documented in the run report.

### Failures

| Test | Result | Recorded Reason or Evidence Limit | Evidence |
| --- | --- | --- | --- |
| cifs/146 | ❌ | Used-space delta was 66,265,088 bytes for a 33,554,432-byte file, outside the allowed tolerance. Filesystem-wide accounting does not isolate the file. | Earlier Oct 1 |
| cifs/171 | ❌ | Concurrent stress emitted `Stale file handle` during append/recovery on the secondary mount. Worker errors stayed within the configured tolerance and the final OK line appeared, but the extra error output differs from expected output; the harness recorded FAIL. | Oct 7 |
| cifs/191 | ❌ | Multichannel throughput improved 83.94%, below the required 100% gain. Channels were established; this was a performance-threshold failure. | Earlier Oct 1 |
| cifs/192 | ❌ | Metadata worker `chmod` returned `EACCES` before its reconnect barrier; earlier read/directory phases completed. Cleanup also found a nonempty directory. | Earlier Oct 1 |
| cifs/194 | ❌ | Oversized fake-mount password handling printed overflow but returned success rather than the expected rejection. Client-helper negative-path check, not server authentication. | Oct 3 |
| cifs/198 | ❌ | Detailed reason for the coverage-run failure is unavailable. The earlier functional run did not report this failure; no reason is inferred. | Unavailable |
| cifs/216 | ❌ | Exact comparison of survivor `del_2` failed at byte 1; the immediate hex reread showed the expected `content_2` plus newline. Different observations across these reads require further isolation; persistent stored-data corruption is not established. | Oct 7 |
| cifs/221 | ❌ | `chmod 0644` on the `modefromsid` fixture returned permission denied; round-trip checks were not reached. | Earlier Oct 1 |
| cifs/225 | ❌ | The requested WSL reparse node representation did not match expectations. | Oct 3 |
| cifs/238 | ❌ | `IN_CREATE` was absent although modify, rename and delete events appeared. The test's client-path attribution was not independently proven. | Earlier Oct 1 |
| cifs/251 | ❌ | After the `cifsacl,idsfromsid` mount succeeded, creating `idsfromsid_file` returned `EIO`. The repaired test now stops explicitly with `create idsfromsid_file failed` instead of ignoring that error and printing success. | Oct 7 |
| cifs/275 | ❌ | Directory leases did not reduce `QueryDirectories`: 102 versus 102. | Oct 3 |
| cifs/304 | ❌ | Mount stress accumulated 116 failures, including mount `EIO`; only 17 of 100 mounts succeeded in the final phase. No session-count leak was observed there. | Earlier Oct 1 |
| cifs/310 | ❌ | All ten mounts, shared-file chunks and 100 directory names passed. In the latest run, bounded binary reads for samples from all ten mounts returned entirely NUL bytes rather than the written text; all ten exact-content comparisons failed. | Oct 7 |
| cifs/335 | ❌ | Creating the workspace on a `cifsacl,idsfromsid` mount returned `EIO`; numeric SID mapping assertions were not reached. | Earlier Oct 1 |
| cifs/341 | ❌ | Writing back `system.cifs_acl` returned `EACCES`; descriptor comparison and binary user-xattr checks were not reached. | Earlier Oct 1 |
| cifs/348 | ❌ | The directory held the expected 420 names, but one exact byte-content assertion failed. The filename and actual bytes were not logged. | Earlier Oct 1 |
| cifs/351 | ❌ | Removing the just-created `user.probe` xattr returned `ENODATA`; later lifecycle checks were not reached. | Earlier Oct 1 |
| cifs/376 | ❌ | SMB 2.1 mount returned `EACCES` after SMB 3.1.1/3.0 combinations succeeded. Protocol/security policy compatibility was not independently diagnosed. | Earlier Oct 1 |
| cifs/380 | ❌ | `chmod` on the source ACL fixture returned permission denied; file and directory DACL copying were not reached. | Earlier Oct 1 |
| cifs/388 | ❌ | File `chmod` returned permission denied after earlier symlink, rename, hardlink and timestamp checks; final mode comparison was not reached. | Earlier Oct 1 |
| cifs/390 | ❌ | The requested SMB3 POSIX mount failed before the test's intended unsupported-feature skip; no filesystem was attached. | Oct 3 |

### Skips

| Test | Result | Recorded Reason or Evidence Limit | Evidence |
| --- | --- | --- | --- |
| cifs/102 | ⏭️ | Global `nosharesock` was configured in the profile. | Earlier Oct 1 |
| cifs/110 | ⏭️ | `prefixpath` appeared unsupported or ignored. | Earlier Oct 1 |
| cifs/134 | ⏭️ | Reported block size was 4,096 bytes, not the requested 262,144. | Earlier Oct 1 |
| cifs/149 | ⏭️ | Hostname re-resolution required a hostname-based `TEST_DEV`; the fixture used an IP address. | Oct 3 |
| cifs/158 | ⏭️ | `CIFS_USER2` was not configured. | Earlier Oct 1 |
| cifs/163 | ⏭️ | Advisory-lock/open-share-mode mapping was not enforced. | Earlier Oct 1 |
| cifs/176 | ⏭️ | Compression mount failed or compression support was not detected. | Earlier Oct 1 |
| cifs/178 | ⏭️ | Setting the user xattr succeeded, but reading it returned empty data. | Earlier Oct 1 |
| cifs/181 | ⏭️ | The mount helper accepted oversized options. | Earlier Oct 1 |
| cifs/185 | ⏭️ | The mount helper accepted unknown options without `sloppy`. | Earlier Oct 1 |
| cifs/189 | ⏭️ | Anonymous `sec=none` access was denied. | Earlier Oct 1 |
| cifs/197 | ⏭️ | The setuid bit was stripped. | Earlier Oct 1 |
| cifs/203 | ⏭️ | `cifscreds add` failed. | Earlier Oct 1 |
| cifs/206 | ⏭️ | Setting the user xattr succeeded, but reading it returned empty data. | Earlier Oct 1 |
| cifs/220 | ⏭️ | `setfacl` was unsupported on the mount. | Earlier Oct 1 |
| cifs/224 | ⏭️ | `SEEK_DATA`/`SEEK_HOLE` was unavailable. | Earlier Oct 1 |
| cifs/229 | ⏭️ | NFS reparse special-file types were unavailable. | Earlier Oct 1 |
| cifs/234 | ⏭️ | No working snapshot-enumeration method was found. | Earlier Oct 1 |
| cifs/240 | ⏭️ | The running kernel lacked `CONFIG_CIFS_SWAP`. | Earlier Oct 1 |
| cifs/244 | ⏭️ | Linux file leases were disabled through `fs.leases-enable`. | Oct 3 |
| cifs/248 | ⏭️ | Compression mount failed or compression support was not detected. | Earlier Oct 1 |
| cifs/252 | ⏭️ | No tested `mknod` operations were supported. | Earlier Oct 1 |
| cifs/254 | ⏭️ | Setting the user xattr succeeded, but reading it returned empty data. | Earlier Oct 1 |
| cifs/289 | ⏭️ | `drop_dir_cache` was not writable. | Earlier Oct 1 |
| cifs/313 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. | Earlier Oct 1 |
| cifs/314 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. | Earlier Oct 1 |
| cifs/315 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. | Oct 3 |
| cifs/316 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. | Earlier Oct 1 |
| cifs/317 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. | Earlier Oct 1 |
| cifs/319 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. | Earlier Oct 1 |
| cifs/320 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. | Oct 3 |
| cifs/321 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. | Earlier Oct 1 |
| cifs/322 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. | Earlier Oct 1 |
| cifs/323 | ⏭️ | Kerberos fixture `CIFS_KRB5_REALM` was not configured. | Oct 3 |
| cifs/324 | ⏭️ | Kerberos fixture `CIFS_KRB5_REALM` was not configured. | Oct 3 |
| cifs/326 | ⏭️ | Kerberos fixture `CIFS_KRB5_REALM` was not configured. | Oct 3 |
| cifs/327 | ⏭️ | Kerberos fixture `CIFS_KRB5_REALM` was not configured. | Oct 3 |
| cifs/328 | ⏭️ | Kerberos fixture `CIFS_KRB5_REALM` was not configured. | Oct 3 |
| cifs/329 | ⏭️ | Kerberos fixture `CIFS_KRB5_REALM` was not configured. | Oct 3 |
| cifs/330 | ⏭️ | Kerberos fixture `CIFS_KRB5_REALM` was not configured. | Oct 3 |
| cifs/331 | ⏭️ | Kerberos fixture `CIFS_KRB5_REALM` was not configured. | Oct 3 |
| cifs/332 | ⏭️ | Kerberos fixture `CIFS_KRB5_REALM` was not configured. | Oct 3 |
| cifs/333 | ⏭️ | Kerberos fixture `CIFS_KRB5_REALM` was not configured. | Oct 3 |
| cifs/356 | ⏭️ | A dedicated non-root `CIFS_MULTIUSER_UID` was required. | Oct 3 |
| cifs/379 | ⏭️ | A snapshot-enabled share with existing snapshots was required. | Oct 3 |
| cifs/387 | ⏭️ | Dedicated-server restart was not authorized with `CIFS_ALLOW_SAMBA_RESTART=yes`. | Oct 3 |
| cifs/396 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. | Earlier Oct 1 |
| cifs/404 | ⏭️ | Kerberos fixture `CIFS_KRB5_REALM` was not configured. | Oct 3 |
| cifs/406 | ⏭️ | Isolated-client tracing was not authorized with `CIFS_ALLOW_OFFLOAD_TRACE=yes`. | Oct 3 |

### Deferral

| Test | Result | Recorded Reason or Evidence Limit | Evidence |
| --- | --- | --- | --- |
| cifs/168 | ⏸️ | The ENOSPC workload would consume approximately 353 GiB; it was deliberately excluded for capacity safety, not executed and skipped. | Run policy |

## ksmbd

September 25 published suite, overlaid with the final October 7 seven-test
validation: **6 PASS, 1 SKIP**. Test `157` now passes its share-scoped Flush
assertion; `171` still skips for unavailable leasing. The temporary fixture
used loopback port 1445 and a default-port forwarder, without interrupting host
Samba. Its module, daemon, forwarder, mounts and credentials were removed.

The October 8 batch added **1 PASS, 1 FAIL, 19 SKIP** for the 21 previously
unrecorded IDs. Test `407` passed; `390` failed after POSIX negotiation when
`chmod` returned permission denied. Its test-local file removal also failed,
but the disposable fixture storage and all owned mounts were removed afterward.
Global DFS-cache flushing, Samba restart, CIFS-client reload, and offload tracing
remained explicitly disabled. No test assertion or expected output changed.

Server multichannel, SMB2 leases and durable handles remained disabled; DFS and
Kerberos fixtures were not configured. Rows not marked October 7 or 8 use the historical
findings in the [ksmbd report](cifs-results-ksmbd-20260925.md), not newly rerun
tests. The intermediate `157` connection failure was a port-fixture mismatch,
preserved separately and replaced only after the final live PASS.

### Failures

| Test | Result | Recorded Reason |
| --- | --- | --- |
| cifs/106 | ❌ | Channel-count expectations were not met with server multichannel disabled; this does not establish failure under an enabled configuration. |
| cifs/108 | ❌ | Channel-count expectations were not met with server multichannel disabled. |
| cifs/122 | ❌ | Server capabilities did not advertise the DFS support expected by the test; this fixture did not configure DFS. |
| cifs/125 | ❌ | The original deferred-read FID was not found after reopening. Lease support was disabled, so lease-enabled handle reuse was not validated. |
| cifs/192 | ❌ | Final permission-mode assertion failed after the read/directory reconnect phases completed. The actual mode was not logged. |
| cifs/194 | ❌ | `mount.cifs` accepted an oversized password; a client-helper negative-path assertion. |
| cifs/198 | ❌ | The 16 MiB read under 30% packet loss did not complete successfully within its internally bounded workload. Exit status/errno was not logged; write and final checksum phases were not reached. |
| cifs/238 | ❌ | The expected local `IN_CREATE` notification was not observed. |
| cifs/341 | ❌ | Parsed security descriptor differed after writing back `system.cifs_acl`. Control fields and ACE ordering are included; this does not prove changed effective access. |
| cifs/347 | ❌ | The notify worker missed its internal deadline after remote creation; cancellation was not reached. This is a test failure, not a runner timeout. |
| cifs/354 | ❌ | A held descriptor returned data different from replacement data written and fsynced through a second mount. The oplock-counter check was not reached. |
| cifs/358 | ❌ | A competing process acquired a supposedly held range during the initial conflict check, before disconnect. Reconnect lock recovery was not reached. |
| cifs/380 | ❌ | Parsed file DACL comparison failed during copying; directory copying was not reached. Descriptor inequality does not by itself prove changed effective access. |
| cifs/382 | ❌ | Opening for write succeeded after setting and reading back the DOS read-only bit; final data validation was not reached. |
| cifs/388 | ❌ | `chmod 0755` succeeded, but the following mode comparison failed. Actual post-chmod mode was not logged; earlier link/rename/timestamp checks completed. |
| cifs/390 | ❌ | October 8: after successful POSIX negotiation, file `chmod` raised `PermissionError: [Errno 13] Permission denied`; test-file removal also logged permission denial. This is not a confirmed data-corruption or server-only diagnosis. |
| cifs/394 | ❌ | The native helper received an unexpected `F_GETLK` lock type. The actual type and phase were not logged; this was a userspace assertion abort, not a kernel crash. |

### Skips

| Test | Result | Recorded Reason |
| --- | --- | --- |
| cifs/105 | ⏭️ | DebugData did not expose server interfaces. |
| cifs/107 | ⏭️ | DebugData did not expose server interfaces. |
| cifs/110 | ⏭️ | `prefixpath` appeared unsupported or ignored by the tested client/server pair. |
| cifs/134 | ⏭️ | Reported block size was 4,096 bytes, not the requested 262,144. |
| cifs/137 | ⏭️ | Signing was not observed as requested. |
| cifs/149 | ⏭️ | No established SMB connection was detected. |
| cifs/158 | ⏭️ | `CIFS_USER2` was not configured. |
| cifs/163 | ⏭️ | Advisory-lock/open-share-mode mapping was not enforced. |
| cifs/166 | ⏭️ | Leasing was unavailable in this baseline. |
| cifs/167 | ⏭️ | No directory-leasing capability was advertised. |
| cifs/168 | ⏭️ | Reported file size reached the target, so recovery and checksum checks were skipped despite a logged ENOSPC write error. This was not a deliberate deferral. |
| cifs/170 | ⏭️ | Leasing was unavailable in this baseline. |
| cifs/171 | ⏭️ | October 7 final run: `leasing unsupported`; SMB2 leases remain disabled in this fixture. |
| cifs/172 | ⏭️ | Leasing was unavailable in this baseline. |
| cifs/176 | ⏭️ | Compression was unavailable or the compression mount was rejected. |
| cifs/177 | ⏭️ | DebugData did not expose server interfaces. |
| cifs/181 | ⏭️ | The mount helper accepted oversized options. |
| cifs/185 | ⏭️ | The mount helper accepted unknown options without `sloppy`. |
| cifs/189 | ⏭️ | Anonymous `sec=none` access was denied. |
| cifs/191 | ⏭️ | The server did not advertise multichannel. |
| cifs/197 | ⏭️ | The setuid bit was stripped. |
| cifs/203 | ⏭️ | The multiuser mount failed. |
| cifs/220 | ⏭️ | `setfacl` was unsupported on the mount. |
| cifs/224 | ⏭️ | `SEEK_DATA`/`SEEK_HOLE` was unavailable. |
| cifs/225 | ⏭️ | WSL reparse special-file types were unavailable. |
| cifs/229 | ⏭️ | NFS reparse special-file types were unavailable. |
| cifs/232 | ⏭️ | `nohandlecache` behavior could not be observed through `open_dirs` or Stats. |
| cifs/234 | ⏭️ | Snapshot enumeration was unavailable to the test. |
| cifs/240 | ⏭️ | The running kernel lacked `CONFIG_CIFS_SWAP`. |
| cifs/244 | ⏭️ | `F_SETLEASE` was unavailable in this configuration. |
| cifs/248 | ⏭️ | Compression was unavailable or the compression mount was rejected. |
| cifs/252 | ⏭️ | No tested `mknod` operations were supported. |
| cifs/289 | ⏭️ | `drop_dir_cache` was not writable. |
| cifs/313 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. |
| cifs/314 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. |
| cifs/315 | ⏭️ | October 8: `CIFS_DFS_ROOT` was not configured; the DFS-cache test did not reach its feature assertions. |
| cifs/316 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. |
| cifs/317 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. |
| cifs/319 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. |
| cifs/320 | ⏭️ | October 8: `CIFS_DFS_ROOT` was not configured; target failover was not exercised. |
| cifs/321 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. |
| cifs/322 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. |
| cifs/323 | ⏭️ | October 8: `CIFS_KRB5_REALM` was not configured. |
| cifs/324 | ⏭️ | October 8: `CIFS_KRB5_REALM` was not configured. |
| cifs/326 | ⏭️ | October 8: `CIFS_KRB5_REALM` was not configured. |
| cifs/327 | ⏭️ | October 8: `CIFS_KRB5_REALM` was not configured. |
| cifs/328 | ⏭️ | October 8: `CIFS_KRB5_REALM` was not configured. |
| cifs/329 | ⏭️ | October 8: `CIFS_KRB5_REALM` was not configured. |
| cifs/330 | ⏭️ | October 8: `CIFS_KRB5_REALM` was not configured. |
| cifs/331 | ⏭️ | October 8: `CIFS_KRB5_REALM` was not configured. |
| cifs/332 | ⏭️ | October 8: `CIFS_KRB5_REALM` was not configured. |
| cifs/333 | ⏭️ | October 8: `CIFS_KRB5_REALM` was not configured. |
| cifs/355 | ⏭️ | October 8: the target server did not advertise SMB3 directory leasing. |
| cifs/356 | ⏭️ | October 8: `CIFS_CRED_FILE2` for a distinct server account was not configured. |
| cifs/379 | ⏭️ | October 8: a snapshot-enabled share with existing snapshots was required. |
| cifs/387 | ⏭️ | October 8: dedicated Samba restart opt-in was disabled; this is not a ksmbd restart test. |
| cifs/392 | ⏭️ | October 8: the target session had no server-interface information. |
| cifs/396 | ⏭️ | DFS fixture `CIFS_DFS_ROOT` was not configured. |
| cifs/404 | ⏭️ | October 8: `CIFS_KRB5_REALM` was not configured. |
| cifs/406 | ⏭️ | October 8: `CIFS_ALLOW_OFFLOAD_TRACE` was disabled; tracing was not enabled merely to replace a skip. |

### Timeouts

| Test | Result | Recorded Reason |
| --- | --- | --- |
| cifs/147 | ⏱️ | The test exceeded the runner's 900-second limit plus up to 30 seconds of termination grace. The blocking operation is not established in the published findings. |
| cifs/152 | ⏱️ | The test exceeded the runner's 900-second limit plus up to 30 seconds of termination grace. The blocking operation is not established in the published findings. |

## Evidence

- October 8 ksmbd completion: `results-runs/cifs-ksmbd-remaining-20261008`, 437 verified checksummed files, 21 verified xUnit outcomes, 103 matching source hashes, and fixture/host restoration records. No counters were reset; no new coverage percentage is claimed.
- Latest seven-test Samba/Azure/Windows batch: `results-runs/cifs-repaired-seven-20261007`, 627 checksummed files, 21 verified xUnit outcomes.
- Latest seven-test ksmbd batch: `results-runs/cifs-repaired-seven-ksmbd-20261007-final`, 280 checksummed files, seven verified xUnit outcomes, listener/forwarder provenance and restoration audits.
- Preserved ksmbd preparation: `results-runs/cifs-repaired-seven-ksmbd-20261007` (201 checksummed files, no tests; loopback-device listener check stopped setup) and `results-runs/cifs-repaired-seven-ksmbd-20261007-retry` (280 checksummed files, seven tests; `157` could not connect without the default-port forwarder). The first stopped attempt's owned stale daemon lock was verified against its exited PID and removed before retrying.
- October 7 Azure/Windows repair runs: `results-runs/cifs-test-fixes-20261007`, with per-server `suite-status.tsv`, xUnit, raw output and source hashes. The initial Samba setup in this archive ran no tests. All 510 checksummed files verified.
- October 7 completed Samba retry: `results-runs/cifs-test-fixes-samba-20261007`, with all five outcomes, four-channel preflight and cleanup audits. All 259 checksummed files verified. Both new archives retain before/after counters without resetting them; these are mixed-backend cumulative snapshots, not a new coverage claim.

Raw archives are local and uncommitted. Archive paths below identify evidence,
not portable repository links. No raw logs, credentials or coverage archives
are copied into this report.

- Samba base: `results-runs/samba422-fresh-cifs-20261006-retry/suite-status.tsv`, with each test's `.out.bad`, `.full` and `.notrun` files.
- Samba supplement: `results-runs/samba422-supplement-final-20261006/suite-status.tsv`.
- Azure latest main-endpoint ledger: `results-runs/azure-cifs-multiuser-leases-20261006/latest-cifs-status.tsv`. Its `latest_run` and `result_xml` fields identify the actual attempt and per-test logs; not all tests ran on October 6.
- Azure endpoint overrides: `results-runs/azure-canary-directory-leases-20261006/azure-cifs/suite-status.tsv` followed by `results-runs/azure-preprod-directory-leases-20261006/azure-cifs/suite-status.tsv`.
- Windows historical context and deferral policy: [October 1 published report](cifs-results-windows-20261001.md#failure-findings), including its recorded skips. Its functional findings are not relabeled as coverage-run diagnoses.
- Windows current October 3 review: `results-runs/local-tests-review-20261003/matrix.tsv` and `windows/batch-*/tests/` beneath that archive, using each test's `.out.bad`, `.full` or `.notrun` output.
- Windows coverage baseline statuses: [current matrix](cifs-results-20261006.md#complete-per-test-matrix) and the published coverage-run failure list. Raw `results-runs/cifs-windows-coverage-20261001.KJqXtj7R/` was not accessible; reasons needing it remain explicitly unverified or unavailable.
- ksmbd: [September 25 failure findings](cifs-results-ksmbd-20260925.md#failure-findings), [recorded skips](cifs-results-ksmbd-20260925.md#recorded-skips) and the same report's timeout list and execution limits. Raw evidence remains private under `results-runs/cifs-ksmbd-published-20260925.DvgX9r/`.
