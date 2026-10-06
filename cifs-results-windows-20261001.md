# Windows CIFS Results: 2026-10-01

Historical report. See [cifs-results-20261006.md](cifs-results-20261006.md) for
the latest-observed overlay. Profiles, runner scripts and raw coverage evidence
named below remain local-only and are not included with these results pages.

## Run Status

Completed on **2026-10-01**, from **13:43:07 to 14:22:45 UTC**. Authenticated
preflight passed on both shares, and all 268 selected tests finished without an
external-runner timeout or safety stop.

| Result | Count |
| --- | ---: |
| PASS | 209 |
| FAIL | 22 |
| SKIP | 37 |
| TIMEOUT | 0 |
| NOT_RUN | 1 |
| **Total** | **269** |

Scope is the 269 published numbered
CIFS tests at `1ebff9ed567e9347fa28abd8339a2877c14e3a3c`, excluding local-only
additions and uncommitted test repairs.

Test `168` is deliberately NOT_RUN with user approval: each share reports about
353 GiB available, and its ENOSPC workload would consume nearly all of that
space. All other tests were reached. A deferral is not a test-reported SKIP.

The failures below include test assumptions, observation/output problems,
permission denials, and client/server behavior requiring further isolation.
They are not all established Windows server defects.

## Environment

- Windows SMB endpoint: `192.168.0.1`; domain/machine name `CPC-bhara-GLUJM`.
  The Windows edition and build have not been independently identified.
- TEST: `//192.168.0.1/smbshare1`; SCRATCH: `//192.168.0.1/smbshare2`.
- Both shares were confirmed dedicated and disposable. The subsequent explicit
  decision to defer `168` supersedes the initial fill-test authorization.
- Linux client kernel: `7.3.0-rc2+`; mount.cifs and the existing built helpers.
- Local-only profile: `local.config.windows-20261001`.
- Baseline options: SMB 3.1.1, `seal,nosharesock,serverino,mfsymlinks`, and
  `dir_mode=0755,file_mode=0755`. Tests that create their own mounts can choose
  different options; this is not an encrypted-only coverage claim.
- Credentials are stored outside the repository in a root-owned mode-0600 file.
  No password or raw key material belongs in this report.
- Existing host mounts at `/mnt/smbshare1` and `/mnt/smbshare2` are preserved.
  The runner uses separate mountpoints and private mount namespaces.
- DFS, Kerberos, secondary identities, and server-side features are not being
  provisioned or reconfigured for this run.

## Preflight And Evidence

Both shares passed encrypted SMB 3.1.1 mount, 4096-byte write, fsync, exact
read-back, owned-file deletion, and unmount probes. TEST reported 361254 MiB
available and SCRATCH 361252 MiB, each on a reported 2096585 MiB filesystem.
Matching capacity figures do not establish independent backing storage or quotas.

Private evidence directory:
`results-runs/cifs-windows-published-20261001.u5cm4kpv/`.
Raw logs may contain sensitive diagnostics and must be redacted before sharing.

Execution uses the local `tools/run_cifs_samba.sh` runner, with
`CIFS_TEST_ROOT` pointing at the clean published worktree. Each test has a
900-second limit plus 30 seconds of termination grace. Execution stops for an
audit after a timeout, unexpected result, settings/firewall mismatch, serious
kernel diagnostic, or low local disk/memory. Completed results are never replaced
by a continuation. Test assertions are not changed to improve pass counts.

## Complete Outcome Lists

The `cifs/` prefix is omitted. Every completed outcome matches a valid xUnit
record; no XML fallback was needed. Every PASS has harness exit status zero.
The 269 unique IDs match the published inventory. PASS is an observed test
outcome, not a blanket correctness certification of its intended coverage.

### PASS (209)

```text
001 100 101 103 105 109 111 112 113 114 115 116 117 118 119 120
121 122 123 124 125 126 129 130 131 132 133 135 136 138 139 140
141 142 143 144 145 147 148 150 151 152 153 154 155 156 157 159
160 161 162 164 165 166 167 169 170 171 172 173 174 175 179 182
183 184 186 187 188 190 193 195 196 198 199 200 201 202 207 208
209 210 211 212 213 214 215 217 218 219 222 223 226 227 228 230
231 233 235 236 237 239 241 242 243 245 246 247 249 250 253 255
256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271
272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287
288 290 291 292 293 294 295 296 297 298 299 300 301 302 303 305
306 307 308 311 312 334 336 337 338 339 340 342 344 346 347 350
352 353 354 357 358 359 361 362 363 364 365 366 367 368 369 370
371 372 373 374 375 381 382 383 384 386 389 393 394 398 399 400
403
```

### FAIL (22)

```text
106 108 127 128 146 191 192 194 216 221 232 238 251 304 310 335
341 348 351 376 380 388
```

### SKIP (37)

```text
102 104 107 110 134 137 149 158 163 176 177 178 181 185 189 197
203 206 220 224 225 229 234 240 244 248 252 254 289 313 314 316
317 319 321 322 396
```

### NOT_RUN (1)

```text
168
```

There are no TIMEOUT entries.

## Failure Findings

| Tests | Observed Failure And Qualification |
| --- | --- |
| 106, 108 | The DebugData-based checks did not observe the required two channels: 106 reported an allocated sum of 1; 108 reported primary/secondary best counts of 0. This does not establish that multichannel is unsupported: 191 later reported five channels. |
| 127, 128 | QueryDirectories did not increment after the initial directory listing. With existing host connections and additional nosharesock mounts to the same share, counter attribution needs verification; this is not proof that no directory request occurred. |
| 146 | The statfs used-space delta was 66265088 bytes for a 33554432-byte file, outside the test's 70-130% tolerance. Filesystem-wide space accounting does not isolate this file or establish the cause of the larger delta. |
| 191 | Five-channel throughput was 60.24 MB/s versus 32.75 MB/s for the baseline, an 83.94% gain. The test requires at least 100% improvement. This is a performance-threshold failure, not a failure to establish multichannel. |
| 192 | The metadata worker's chmod returned EACCES before its reconnect barrier. Earlier read/directory phases completed, but the metadata reconnect phase did not. The cleanup log also reports a nonempty directory; remote cleanup is not certified. |
| 194 | The mount helper reported an overflow for the 512-byte password case; output included `Converted password too long!` and a duplicate-password warning. This is a client/helper negative-path result, not evidence of a Windows authentication defect. |
| 216 | A surviving file, `del_2`, had unexpected content after the directory workload. Bash also reported an ignored NUL byte in command substitution. Exact returned bytes and the responsible client/server operation were not isolated. |
| 221 | chmod 0644 on the modefromsid fixture returned permission denied. The subsequent mode round-trip checks were not reached. |
| 232 | Functional nohandlecache observations succeeded: cached entries were 1 versus 0 with nohandlecache. Two awk escape-sequence warnings appeared in test output, producing a harness output mismatch. Retained as FAIL, not silently converted to PASS. |
| 238 | IN_CREATE was absent from the captured inotify events, although modify, move, and delete events appeared. The script attributes this to the client notification path; this run alone does not prove that attribution. |
| 251 | Creating the idsfromsid file returned EIO. The script ignores that write failure and still logs `idsfromsid OK`; the error also contaminated expected output. This is not a valid successful idsfromsid check. |
| 304 | The nosharesock mount-stress test accumulated 116 failures. Logs include repeated mount EIO failures and only 17 of 100 mounts established in its final phase. That phase reported no session-count leak; the reason for the mount failures remains unproven. |
| 310 | All ten mounts and the shared-file chunk checks passed, but seven directory-file content comparisons failed for mounts 4-10. Logs show empty shell-comparison values and ignored-NUL warnings. Do not infer a server corruption cause without a byte-level reproduction. |
| 335 | Creating the owned workspace on a cifsacl,idsfromsid mount failed with EIO. Numeric SID-to-ID assertions were not reached. |
| 341 | Writing back `system.cifs_acl` returned EACCES. Descriptor round-trip comparison and later binary user-xattr checks were not reached. |
| 348 | The directory contained the expected 420 names after deletion, but a file's exact byte-content assertion failed. The failing name and actual bytes were not logged. This was a content check, not a directory-count mismatch. |
| 351 | Removing the just-created `user.probe` xattr returned ENODATA. The subsequent attribute lifecycle checks were not reached; other xattr tests also observed nonpersistent or empty user attributes. |
| 376 | Earlier SMB 3.1.1/3.0 combinations mounted, but the SMB 2.1 attempt returned EACCES and no filesystem was attached. Protocol/security policy compatibility was not independently diagnosed. |
| 380 | chmod on the source ACL fixture returned permission denied. File and directory DACL copying were not reached. |
| 388 | File chmod returned permission denied after earlier symlink, rename, hardlink, and timestamp checks. The final mode comparison was not reached. |

No failed assertion was weakened or repaired during this run. PASS results also
remain subject to the published scripts' limitations; for example, test `150`
uses unscoped credit observations and does not reliably check every worker status.

## Recorded Skips

These are the scripts' recorded prerequisite or observation outcomes, not an
independent determination that the Windows server lacks each feature.

| Tests | Recorded Reason |
| --- | --- |
| 102 | Global nosharesock configured in the profile. |
| 104 | CIFS Stats did not reflect the write for the share. |
| 107, 177 | Required active/allocated multichannel count was not observed. |
| 110 | prefixpath appeared unsupported or ignored. |
| 134 | Reported block size 4096 differed from requested bsize 262144. |
| 137 | Requested signing was not observed. |
| 149 | No established SMB connection detected. |
| 158 | CIFS_USER2 not configured. |
| 163 | Advisory lock/open-sharemode mapping not enforced. |
| 176, 248 | Compression mount failed or compression support was not detected. |
| 178, 206, 254 | setxattr accepted, but getxattr returned empty user-attribute data. |
| 181 | Mount helper accepted oversized options. |
| 185 | Mount helper accepted unknown options without sloppy. |
| 189 | Anonymous sec=none access denied. |
| 197 | Setuid bit stripped. |
| 203 | cifscreds add failed. |
| 220 | setfacl unsupported on the mount. |
| 224 | SEEK_DATA/SEEK_HOLE unavailable. |
| 225 | WSL reparse special-file types unavailable. |
| 229 | NFS reparse special-file types unavailable. |
| 234 | No working snapshot enumeration method found. |
| 240 | Running kernel CONFIG_CIFS_SWAP disabled. |
| 244 | F_SETLEASE unavailable in this configuration. |
| 252 | No mknod operations supported. |
| 289 | drop_dir_cache not writable. |
| 313, 314, 316, 317, 319, 321, 322, 396 | CIFS_DFS_ROOT not configured. |

## Final Audit

The private post-run audit was recorded at **15:15:05 UTC** on 2026-10-01:

- No matching test workers or extra Windows test mounts remained.
- Both original host mounts at `/mnt/smbshare1` and `/mnt/smbshare2` were
  preserved. Snap namespace aliases were verified against the same source,
  filesystem device, and filesystem root and left untouched.
- Samba remained active, matching the pre-run state. No service restoration
  or server-side configuration change was needed for this remote run.
- All monitored CIFS settings/module parameters and the file-leases setting
  matched their baseline; normalized IPv4/IPv6 firewall rules also matched.
- Kernel taint remained zero. No BUG/Oops/panic/KASAN/OOM/CPU-warning match was
  found in the available kernel log since the run began. This scoped check is
  not proof of the absence of every possible kernel issue.
- Available local disk space was 1303 MiB and available memory was 6297 MiB.
- The published test/helper/harness sources and profile were unchanged.
  Credentials remained root-owned mode 0600 outside the repository, and raw
  evidence remained root-private. The pre-existing staged changes were preserved.

The audit is a host cleanup check, not proof that the remote shares are empty.
Test `192` explicitly logged a cleanup failure; other failed tests may also have
left owned files. No broad remote deletion was performed. Tests can reset counters
and caches, so unchanged monitored settings do not imply unchanged global runtime
state. No test repairs, commits, or pushes were made for this Windows run.

## Coverage Rerun: 2026-10-01

The preserved local coverage archive (`coverage/README.md`) includes readable HTML,
complete outcomes, matching source/build inputs, protected raw evidence, and
checksum/reproduction instructions for future reference.

A separate run against the same Windows shares measured the Linux CIFS client,
not the Windows server implementation. It used the same 269 published test IDs
at `1ebff9ed567e9347fa28abd8339a2877c14e3a3c`, with `168` still deferred.
Tests ran from **17:01:06 to 17:46:16 UTC**; the final audit completed at
**17:46:24 UTC**. All 268 selected tests finished: **211 PASS, 21 FAIL, 36 SKIP,
0 TIMEOUT, 1 NOT_RUN** across the complete inventory. These outcomes are separate
from the earlier 209/22/37 functional run above; neither run replaces the other.

### Coverage Numbers

| Metric | Executed | Instrumented | Coverage |
| --- | ---: | ---: | ---: |
| Lines | 15918 | 31508 | 50.52% |
| Functions | 763 | 1179 | 64.72% |
| Branches | 6891 | 22392 | 30.77% |

Scope: **47 instrumented C files matching `fs/smb/client/*.c`** in the loaded
module. Headers, header-generated trace code, and exception-tagged branches are
excluded. Files not built into this module are not in the denominator. These
are aggregate run numbers, including setup, successful tests, failed tests,
skip prerequisite probes, and cleanup; they are not per-test coverage or proof
of correctness for every executed path.

### Collection And Integrity

- Kernel: `7.3.0-rc2+`; rebuilt CIFS module build ID:
  `a715402c4ed0028239f9ceab7c78121c639bc452`.
- GCC/gcov 14.2 instrumentation, with `CONFIG_GCOV_KERNEL=y` and
  `CONFIG_GCOV_PROFILE_ALL=y`. LCOV 2.3.1 was privately installed; the system
  LCOV installation was not replaced.
- The local `tools/run_cifs_coverage.py` runner preserved the original
  counters and metadata, then reset only the 48 CIFS GCOV objects at
  17:01:06 UTC. It did not use the global kernel coverage reset.
- Tests `100` and `101` passed the smoke gate: counters in `smb2pdu`, `file`,
  and `connect` changed from zero to nonzero. The remaining 266 tests ran
  without another coverage reset, retaining the smoke-test coverage.
- All captured GCOV data/metadata pairs matched. The runner checked the loaded
  module identity, source/metadata hashes, test revision, and profile throughout
  execution and again during final collection.
- Generated trace-header branch metadata conflicted during LCOV merging, so
  the report explicitly limits its denominator to client C implementation
  files. No LCOV merge errors were suppressed in the final capture.
- HTML rendering used `check_data_consistency=0` because optimized GCC output
  can mark a wrapper's declaration line hit while its function entry is zero.
  Recorded counts were retained unchanged; this disables a rendering check,
  not an execution counter or a test assertion.
- Summary totals were independently reconciled against the final LCOV records.
  HTML generation completed successfully.

Private evidence root: `results-runs/cifs-windows-coverage-20261001.KJqXtj7R/`.
It contains preserved pre-reset and zero snapshots, smoke results, the full
test ledger, and the final `suite-coverage/coverage.info`, `summary.json`, raw
GCOV pairs, and `html/index.html`. Raw artifacts remain root-private.

### Rerun Outcomes And Audit

Failed IDs (`cifs/` omitted):

```text
103 106 108 146 191 192 194 198 216 221 238 251 304 310 335 341
348 351 376 380 388
```

The final audit verified unchanged monitored settings and firewall rules,
unchanged kernel taint, no matching test workers or CIFS host mounts, and no
serious kernel-diagnostic match. There were no pre-existing CIFS host mounts
at the start of this coverage run. Available local disk space was 1153 MiB and
available memory was 6629 MiB. As with the earlier run, this is not a guarantee
that all test-owned files were removed from the remote shares.
