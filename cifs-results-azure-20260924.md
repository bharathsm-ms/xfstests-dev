# Azure Files CIFS Results: 2026-09-24

Historical report. See [cifs-results-20261006.md](cifs-results-20261006.md) for
newer outcomes. Profiles, runner scripts and raw evidence named below remain
local-only and are not included with these results pages.

## Run Status

**Run finished: 201 PASS, 23 FAIL, 41 SKIP, 3 TIMEOUT, 1 NOT_RUN.**
All 269 published test IDs are accounted for. Test `168` was deliberately
deferred; no tests remain unreached after the timeout continuations. These
results describe the numbered CIFS tests published at commit
`1ebff9ed567e9347fa28abd8339a2877c14e3a3c`. It does not include the 33 local-only
test additions or the uncommitted repairs in the main working tree.

The main run and its three continuations ran from 17:20 to 20:38 UTC on
2026-09-24, including audit pauses; three smoke tests ran beforehand. Every
PASS, FAIL, and SKIP classification was checked against its matching xUnit
record. PASS also requires a zero harness exit status. No XML fallback was
needed. Timeout and deliberate-deferral outcomes remain separate from skips.

## Complete Outcome Lists

IDs below have the `cifs/` prefix omitted. Each published ID appears exactly once.

### PASS (201)

```text
100 101 105 106 107 108 109 112 113 114 115 117 118 119 121 122
123 124 125 126 129 130 131 132 135 136 138 139 140 141 142 143
144 145 146 147 148 150 151 153 154 155 156 157 159 160 161 162
165 166 169 170 171 172 173 174 175 179 182 183 184 186 187 188
190 191 193 195 196 198 199 200 201 207 208 209 210 211 212 213
214 215 217 218 219 221 222 223 228 230 231 235 236 237 239 241
242 243 245 246 247 249 250 251 253 257 258 259 260 261 262 263
264 265 266 267 268 269 270 271 272 273 274 276 277 278 279 280
281 282 283 284 285 286 287 288 290 291 292 293 294 295 296 297
298 299 300 301 302 303 304 305 306 307 308 312 334 335 336 337
338 339 340 342 344 346 347 348 350 352 353 354 357 359 361 362
363 364 365 366 367 368 369 370 371 372 373 374 375 380 381 382
383 384 386 389 394 398 399 400 403
```

### FAIL (23)

```text
001 103 116 120 127 128 133 152 164 178 192 194 202 206 216 238
310 341 351 358 376 388 393
```

### SKIP (41)

```text
102 104 110 111 134 137 149 158 163 167 176 177 181 185 189 197
203 220 224 225 226 227 229 232 233 234 240 244 248 252 254 255
289 313 314 316 317 319 321 322 396
```

### TIMEOUT (3)

```text
256 275 311
```

### NOT_RUN (1)

```text
168
```

## Environment

- Client kernel: `7.3.0-rc2+`, x86-64.
- Backend: Azure Files, account `smbpremium1`.
- TEST: `//smbpremium1.file.core.windows.net/testshare1`.
- SCRATCH: `//smbpremium1.file.core.windows.net/testshare2`.
- Local-only profile: `local.config.azure-20260924`.
- Options: SMB 3.1.1, `dir_mode=0755,file_mode=0755,serverino,nosharesock,mfsymlinks,actimeo=30`.
- Authentication uses an existing root-owned mode-0600 credentials file; no key
  is included in this report or profile.
- Both shares were explicitly confirmed disposable. SCRATCH tests may remove
  existing files. Preflight write, fsync, and read-back probes passed on both.
- Preflight free space: approximately 168 GiB on TEST, 200 GiB on SCRATCH,
  and 1262 MiB on the local client filesystem.

## Execution

Tests run from the clean sync worktree at the published revision, using
the local `tools/run_cifs_samba.sh` runner with `CIFS_TEST_ROOT` set.
Dedicated mountpoints and private per-test mount namespaces preserve the user's
existing `/media/testshare1` host mount. `/etc/fstab` is unchanged.

Raw results are private under
`results-runs/cifs-azure-published-20260924.iPlhWR/`. The `smoke` segment contains
tests `100`, `101`, and `192`; `suite/<NNN>/<NNN>/smb3/` contains the other
initial executions. Continuations use `resume`, `resume2`, and `resume3` with the same
per-test layout. The corresponding status TSVs and manifest JSON files retain
execution status and provenance. Continuation rows supersede only earlier
NOT_RUN placeholders; they do not replace failures or timeouts. Raw console and
full logs must not be published without redaction.

The main run used a 900-second per-test timeout plus a 30-second termination
grace. The controller stopped for an audit after a timeout, a firewall/settings mismatch, or
local free space falling below 512 MiB. Smoke tests used a 300-second timeout.
No test assertions are changed to improve the outcome count.

## Smoke Results

| Test | Outcome | Evidence |
| --- | --- | --- |
| 100 | PASS | xUnit, 2 seconds. |
| 101 | PASS | xUnit, 5 seconds. |
| 192 | FAIL | Embedded Python line 21: second-half read differs from expected data after the first owned socket reset. Directory and metadata phases were not reached. |

## Explicit Deferrals

- `168`: would fill approximately 168 GiB to force ENOSPC. Deferred pending a
  small dedicated quota fixture; this is not a backend capability SKIP.

Test `236` was eligible because cachefilesd was already active; it ran and passed.

## Timeout Audits

Test `256` reached its 900-second limit plus 30 seconds of termination grace.
Its full log records successful creation/listing and scandir validation of
10,000 files, but no later completed phase. It remains TIMEOUT, not PASS or SKIP.

The post-timeout audit found no matching test processes, no private CIFS mounts
in the host namespace, unchanged monitored settings and firewall rules, and
1252 MiB free locally. The original Azure mount remains present. Test-owned
remote files may remain after interrupted cleanup; absence of host mounts does
not prove that all remote test data was removed.

The first resume passed tests `257` through `274`, then `275` timed out during
the initial rsync after creating its 1000-file source tree. It did not reach
the lease/no-lease comparison. The second audit found unchanged monitored
settings and firewall rules, no matching test processes or private host mounts,
and 1250 MiB free locally. The remaining 95 tests ran in a second resume segment.

The second resume recorded 32 PASS, one FAIL (`310`), one SKIP (`289`), and
one TIMEOUT (`311`), leaving 60 tests unreached. Test `311` created 5000 files
and started its rapid open/close workload before reaching the 900-second limit
plus termination grace. The third audit found unchanged monitored settings and
firewall rules, no matching test processes, only the original host CIFS mount,
and 1247 MiB free locally. The original ledgers are preserved.

The third resume completed all remaining 60 tests: 46 PASS, six FAIL, and eight
SKIP. It encountered no further timeouts or safety stops.

## Final Host Audit

After the final segment, monitored CIFS settings and the file-lease setting
matched their baseline, and normalized firewall rules were unchanged. No
matching test processes remained. The only host CIFS mount was the original
`/media/testshare1` mount; no private test mounts remained in that namespace.
Local free space was 1243 MiB. The published worktree's tracked test scripts,
common helpers, and harness still matched the tested revision.

These checks do not claim that every global counter or cache was unchanged:
some tests reset CIFS Stats or drop caches. Test-owned remote files may remain
after timeouts; no broad cleanup of either share was performed. Raw results
remain under a root-owned mode-0700 directory. No test fixes, commits, or pushes
were made as part of this Azure run.

## Continuation Findings

These seven failures and nine skips supplement the first-pass findings below.

| Test | Observed Failure | Qualification |
| --- | --- | --- |
| 310 | Six cross-mount checksums differed from mount 1. | Primary-mount chunk validation and shared-directory checks passed; checksum workers succeeded. Client/service cause not established. |
| 341 | Binary user-xattr creation returned EINVAL. | The preceding system.cifs_acl round-trip assertion completed; this is not evidence of an ACL mismatch. |
| 351 | Initial user-xattr probe returned EINVAL. | The test skips only EOPNOTSUPP, so this remains FAIL; later lifecycle checks were not reached. |
| 358 | Post-reset pwrite returned EAGAIN. | Initial locks and pre-reset contention checks completed. The later lock-survival assertion was not reached. |
| 376 | SMB 2.1 mount returned Permission denied. | Earlier SMB 3.1.1 and 3.0 variations completed; this is a dialect/policy compatibility result, not proof of failed SMB3 negotiation. |
| 388 | Hardlink creation returned Operation not supported. | Missing hardlink capability remains a recorded FAIL. |
| 393 | Hardlink creation on the encrypted mount returned Operation not supported. | Does not establish an encryption failure. |

| Tests | Recorded Skip Reason |
| --- | --- |
| 289 | drop_dir_cache not writable. |
| 313, 314, 316, 317, 319, 321, 322, 396 | CIFS_DFS_ROOT not configured; DFS fixture unavailable. |

## First-Pass Failures

These 16 failures include the smoke failure and are retained regardless of later
results. Capability-related failures are not silently changed into skips.

| Test | Observed Failure | Qualification |
| --- | --- | --- |
| 001 | Clone returned Operation not supported; expected output differs. | Unsupported-operation result, not proof of data corruption. |
| 103 | No baseline non-nosharesock connection found. | The requested profile explicitly enables nosharesock. |
| 116 | Punch-hole failed; diagnostic-printing command also failed. | Quoting bug hides the underlying error. |
| 120 | Lock-holder readiness marker absent after 0.2 seconds. | Timing-sensitive test; no lock errno was established. |
| 127 | QueryDirectories did not increase after initial listing. | Share-name-only counter selection can observe another connection. |
| 128 | QueryDirectories did not increase after first nolease listing. | Same counter-selection ambiguity as 127. |
| 133 | mtime unchanged after cross-mount append with actimeo=0. | Cache/coherency assertion; cause not established. |
| 152 | Long-path operation returned TOTAL_ERR 2. | ENOENT differed from the script's accepted result. |
| 164 | Creating the first hardlink returned Operation not supported. | The related 111 and 255 tests skipped for missing hardlink support. |
| 178 | Initial setfattr failed. | Related 254 skipped for unsupported user xattrs. |
| 192 | Second-half read mismatched after the first socket reset. | Directory and metadata phases were not reached. |
| 194 | mount.cifs accepted an oversized password. | Client mount-helper negative-path assertion. |
| 202 | Lock/open worker exceeded its deadline, approximately 5236 ms. | Reported worker 5; latency-sensitive bound. |
| 206 | Initial setfattr failed. | Related 254 skipped for unsupported user xattrs. |
| 216 | A surviving file had unexpected content. | Also emitted a null-byte command-substitution warning; requires investigation. |
| 238 | IN_CREATE notification was not observed. | Creation-notification assertion also failed in the Samba review. |

## First-Pass Skips

The following 32 tests reported SKIP through their own prerequisite checks.
These are separate from the deliberate deferral and tests not reached.

| Tests | Recorded Reason |
| --- | --- |
| 102 | Global nosharesock configured. |
| 104 | CIFS Stats did not reflect the write. |
| 110 | prefixpath unsupported or ignored by this client/server pair. |
| 111, 255 | Hardlinks unsupported. |
| 134 | Reported statfs block size differs from requested bsize. |
| 137 | Test did not observe signing enabled as requested. |
| 149 | Test did not find an established SMB connection. |
| 158 | CIFS_USER2 not configured. |
| 163 | Advisory lock/open-sharemode mapping not enforced. |
| 167 | No directory leasing capability. |
| 176, 248 | Compression unavailable or compress mount rejected. |
| 177 | Test reported only one active channel. |
| 181 | Helper accepted oversized options. |
| 185 | Helper accepted unknown options without sloppy. |
| 189 | sec=none mount returned EINVAL. |
| 197 | Server stripped the setuid bit. |
| 203 | Multiuser mount failed. |
| 220 | setfacl unsupported. |
| 224, 227 | Punch-hole unsupported. |
| 225 | WSL reparse special-file types unavailable. |
| 226 | Zero-range unsupported. |
| 229, 252 | NFS reparse nodes or mknod operations unsupported. |
| 232 | Could not observe nohandlecache through open_dirs or Stats. |
| 233 | Collapse-range and insert-range unavailable. |
| 234 | Snapshot enumeration unavailable to the test. |
| 240 | Kernel CONFIG_CIFS_SWAP disabled. |
| 244 | F_SETLEASE unsupported in this configuration. |
| 254 | user xattrs unsupported. |

Skip reasons above are the tests' observations, not independent proof of backend
capabilities. In particular, `106`, `107`, and `108` passed multichannel checks
while `177` reported one channel; do not infer that Azure lacks multichannel.

## Interpretation

These are Azure results for the published tests, not reruns of the repaired
local-only tests. The September Samba ledger remains separate in
[cifs-results-20260917.md](cifs-results-20260917.md).

Test `103` assumes a baseline without `nosharesock`; the requested profile
includes that option. Its observed FAIL is therefore a test/profile assumption
conflict, not evidence that Azure incorrectly implements `nosharesock`.

The `192` read assertion failed after the first reset. The wrapper message
"worker exited before reconnect barrier" refers to a subsequent barrier and
does not mean that no reset occurred. The cause requires further investigation;
the assertion alone does not establish a client or service defect.

Other completed failures require test-side qualification before assigning blame:

- `116`: the punch-hole operation failed, but escaped quotes in its error-printing
  command prevented the underlying diagnostic from being included in the full
  log. The observed FAIL is retained; the server errno is not established here.
- `120`: the script waits only 0.2 seconds before requiring the background lock
  holder's readiness marker on the remote share. Its readiness failure does not
  by itself establish a byte-range-lock implementation defect.
- `127` and `128`: directory counters did not increment as expected. Their
  share-name-only Stats lookup is ambiguous when another connection to the same
  share exists; the original host mount was deliberately retained.
