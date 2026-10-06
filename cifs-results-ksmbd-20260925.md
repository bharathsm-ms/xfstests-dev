# ksmbd CIFS Results: 2026-09-25

Historical report. See [cifs-results-20261006.md](cifs-results-20261006.md) for
the cross-server matrix. Configurations, runner scripts and raw evidence named
below remain local-only and are not included with these results pages.

## Run Status

Completed on **2026-09-25**, from **06:42:48 to 08:10:49 UTC**, in three segments.
Setup and authenticated preflight passed. All 269 published tests were reached:

| Result | Count |
| --- | ---: |
| PASS | 209 |
| FAIL | 17 |
| SKIP | 41 |
| TIMEOUT | 2 |
| NOT_RUN | 0 |
| **Total** | **269** |

Samba was restored at **08:12:19 UTC**, and the temporary backing filesystems
were released. Failures include fixture assumptions and test-observation limits;
they are not all established ksmbd defects.

The inventory is the 269 numbered CIFS tests published
at `1ebff9ed567e9347fa28abd8339a2877c14e3a3c`, excluding local-only additions
and uncommitted test repairs.

## Environment

- Client and server kernel: `7.3.0-rc2+`, x86-64, on the same host.
- Server: in-tree ksmbd module, ksmbd-tools `3.5.3-1` from Ubuntu.
- Tools were checksum-verified and privately extracted under
  `/opt/ksmbd-xfstests-3.5.3`; the conflicting distribution package was not
  installed and Samba was not removed.
- Local-only server configuration: `configs/ksmbd-20260925.conf`.
- Local-only client profile: `local.config.ksmbd-20260925`.
- TEST: `//127.0.0.2/xfstest`; SCRATCH: `//127.0.0.2/xfstest_scratch`.
- The ksmbd TCP listener was restricted to loopback port 445. Samba was
  temporarily stopped with explicit approval and restored after testing.
- Each share has a dedicated 2 GiB loop-backed ext4 filesystem under
  `/srv/ksmbd-xfstests-20260925/`. The images reside on a dedicated 4.5 GiB
  tmpfs, avoiding allocation of their contents on the nearly full root disk.
- Authenticated, non-guest access uses a dedicated non-login `ksmbd-xfstest`
  account and a root-owned mode-0600 credentials file. No secrets appear here.
- SMB 3.1.1 profile: `dir_mode=0755,file_mode=0755,serverino,mfsymlinks`.
  Unlike the Azure profile, global `nosharesock` is not set. Server multichannel
  remains disabled for this baseline. DFS and Kerberos fixtures are not enabled.
- The installed ksmbd-tools defaults also leave `smb2 leases = no` and
  `durable handles = no`; share oplocks default to `yes`. These settings were
  not changed during execution. Results are not coverage of an all-features-
  enabled ksmbd configuration.

## Preflight

Both shares passed 4096-byte write, fsync, exact read-back, and owned-file
removal probes. Each reported 1929 MiB available. The original Azure host
mount is preserved; inherited copies are detached only inside private test
mount namespaces. Neither `/etc/fstab` nor the existing Kerberos realms was
changed.

## Execution And Limits

Tests use the clean published worktree and
the local `tools/run_cifs_samba.sh` runner with `CIFS_TEST_ROOT` set.
Each test runs in a private mount namespace. Results are kept private under
`results-runs/cifs-ksmbd-published-20260925.DvgX9r/`; raw logs must not be
published without redaction.

The per-test limit was 900 seconds plus 30 seconds of termination
grace. Execution stops for an audit after a timeout, a monitored-setting or
firewall mismatch, a server failure, a new serious kernel diagnostic, or low
host resources. The bounded fixtures permit the ENOSPC test that was deferred
on Azure, but tests requiring larger backing storage may skip or fail. Such
outcomes must be qualified rather than attributed automatically to ksmbd.

PASS, FAIL, and SKIP were reconciled against matching xUnit records and harness
status, with the three explicit XML fallbacks below. TIMEOUT is distinct from
FAIL and SKIP. No tests were deliberately deferred, and no assertions or tested
sources were modified. Continuations replaced only NOT_RUN entries, preserving
both timeouts and all completed results. The private `combined-status.tsv`
records the final outcome, exit status, duration, and evidence path for every ID.

## Complete Outcome Lists

The `cifs/` prefix is omitted. PASS is the published test's observed outcome,
not proof that every intended kernel path was exercised.

### PASS (209)

```text
001 100 101 102 103 104 109 111 112 113 114 115 116 117 118 119
120 121 123 124 126 127 128 129 130 131 132 133 135 136 138 139
140 141 142 143 144 145 146 148 150 151 153 154 155 156 159 160
161 162 164 165 169 173 174 175 178 179 182 183 184 186 187 188
190 193 195 196 199 200 201 202 206 207 208 209 210 211 212 213
214 215 216 217 218 219 221 222 223 226 227 228 230 231 233 235
236 237 239 241 242 243 245 246 247 249 250 251 253 254 255 256
257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272
273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288
290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305
306 307 308 310 311 312 334 335 336 337 338 339 340 342 344 346
348 350 351 352 353 357 359 361 362 363 364 365 366 367 368 369
370 371 372 373 374 375 376 381 383 384 386 389 393 398 399 400
403
```

### FAIL (17)

```text
106 108 122 125 157 192 194 198 238 341 347 354 358 380 382 388
394
```

### SKIP (41)

```text
105 107 110 134 137 149 158 163 166 167 168 170 171 172 176 177
181 185 189 191 197 203 220 224 225 229 232 234 240 244 248 252
289 313 314 316 317 319 321 322 396
```

### TIMEOUT (2)

```text
147 152
```

There are no NOT_RUN entries.

## Failure Findings

- `106` and `108` FAIL: channel-count expectations are not met with server
  multichannel disabled. These do not establish a multichannel implementation
  failure under an enabled configuration.
- `122` FAIL: the baseline server capabilities do not advertise DFS as expected
  by the test. This fixture does not configure DFS.
- `125` FAIL: the test did not find the original deferred-read FID after
  reopening the file. Lease support is disabled in this baseline; this is not
  independent evidence of broken handle reuse with leases enabled.
- `192` FAIL: the final permission-mode assertion failed after the reconnect
  workloads. The read and directory phases completed, unlike its earlier Azure
  failure. The actual final mode was not logged; cause remains unproven.
- `157` FAIL: the flush counter did not increase. The script selects the first
  global Flush counter rather than scoping it to the test connection; the Azure
  host connection was retained. This does not prove that ksmbd omitted a flush.
- `194` FAIL: mount.cifs accepted an oversized password. This is a client
  mount-helper negative-path assertion, also observed on Azure.
- `198` FAIL: the 16 MiB read under 30% probabilistic packet loss did not
  complete successfully. The test gives this read a 90-second timeout, but
  does not log its exit status or errno. The write and final checksum phases
  were not reached. Firewall rules matched their baseline after the test.
- `238` FAIL: IN_CREATE was not observed. The same notification assertion
  failed in the Azure and Samba reports.
- `341` FAIL: the parsed security descriptor differed after writing back the
  original `system.cifs_acl` value. This comparison includes descriptor control
  fields and ordered ACE entries; it does not by itself prove an effective-access
  change. The later binary user-xattr checks were not reached.
- `347` FAIL: the notify worker did not complete within the test's internal
  notification deadline after remote file creation. The cancellation phase
  was not reached. This is a test FAIL, not an external-runner TIMEOUT.
- `354` FAIL: a held descriptor returned data different from the replacement
  written and fsynced through a second mount. The oplock-counter check was not
  reached. The client/server coherency failure needs further isolation.
- `358` FAIL: a competing process acquired a range expected to be locked in the
  initial conflict check, before the disconnect. Despite the script's final
  failure message, this run did not reach reconnect or verify lock recovery.
- `380` FAIL: the helper's parsed DACL comparison failed when copying a file's
  ACL. Directory ACL copying was not reached. As with `341`, descriptor equality
  failure alone does not establish a change in effective access.
- `382` FAIL: after setting and reading back the DOS read-only bit, opening the
  file for writing still succeeded. Earlier DOS-attribute and creation-time
  round-trips passed; the final data check was not reached.
- `388` FAIL: chmod to 0755 succeeded, but the following mode comparison did not
  report 755. The actual post-chmod value was not logged. Earlier symlink,
  hardlink, rename, and timestamp checks completed.
- `394` FAIL: the native helper's F_GETLK result had a lock type different from
  the expected type. The actual type and failing phase were not logged, so full
  lock-conflict and release coverage cannot be claimed. The assertion abort is
  a userspace test failure, not a kernel crash.

## Recorded Skips

These are test-reported prerequisite or observation outcomes, not independent
proof of unsupported server features. All 41 SKIP outcomes are covered below.

| Tests | Recorded Reason |
| --- | --- |
| 105, 107, 177 | DebugData did not expose Server interfaces. |
| 110 | prefixpath unsupported or ignored by this client/server pair. |
| 134 | Reported block size 4096 differs from requested bsize 262144. |
| 137 | Signing was not observed as requested. |
| 149 | No established SMB connection detected. |
| 158 | CIFS_USER2 not configured. |
| 163 | Advisory lock/open-sharemode mapping not enforced. |
| 166, 170, 171, 172 | Leasing unsupported in this baseline. |
| 167 | No directory leasing capability. |
| 168 | ENOSPC recovery path was not reached because size reached target. |
| 176, 248 | Compression unavailable or compress mount rejected. |
| 181 | Helper accepted oversized options. |
| 185 | Helper accepted unknown options without sloppy. |
| 189 | Anonymous sec=none access denied. |
| 191 | Server did not advertise multichannel. |
| 197 | Setuid bit stripped. |
| 203 | Multiuser mount failed. |
| 220 | setfacl unsupported. |
| 224 | SEEK_DATA/SEEK_HOLE unavailable. |
| 225 | WSL reparse special-file types unavailable. |
| 229 | NFS reparse special-file types unavailable. |
| 232 | Could not observe nohandlecache through open_dirs or Stats. |
| 234 | Snapshot enumeration unavailable to the test. |
| 240 | Kernel CONFIG_CIFS_SWAP disabled. |
| 244 | F_SETLEASE unavailable in this configuration. |
| 252 | No mknod operations supported. |
| 289 | drop_dir_cache not writable. |
| 313, 314, 316, 317, 319, 321, 322, 396 | CIFS_DFS_ROOT not configured. |

Test `168` did execute on the bounded fixture: its log contains an ENOSPC write
error, but the file's reported size reached the target and the script skipped
before testing recovery or verifying the final checksum. It is not the deliberate
NOT_RUN deferral used in the Azure report.

## Result Integrity

- `105`, `107`, and `177` SKIP records contain malformed xUnit XML with a control byte
  in the skip message. The runner used their matching `.notrun` files as explicit
  fallback evidence. Removing the single control byte in memory corroborated
  each XML SKIP classification; raw XML is retained unchanged.
- Every other PASS, FAIL, and SKIP has a matching parseable xUnit record. Every
  PASS has harness exit status zero; the two TIMEOUT records retain their
  timeout exit status. All 269 unique IDs match the published inventory.
- The published test/helper/harness sources and both configuration hashes
  remained unchanged. Raw results remain root-private.
- Test `150` passed, but its unscoped credit observation and unchecked worker
  wait statuses limit the strength of that result. This run is not a blanket
  correctness review of the published scripts.

## Setup And Diagnostic Notes

Attempting to share port 445 with Samba using a separate dummy interface failed
with `EADDRINUSE`. Moving the userspace daemon into a network namespace did not
isolate the listener on this kernel. Both experimental interfaces/namespaces
were removed before the live run. The successful setup uses host loopback with
Samba temporarily stopped by explicit approval.

During `147`, the notify worker was observed waiting in `SMB2_change_notify`
through `cifs_ioctl` and `wait_for_response`. The published script's 15-second
readiness loop is followed by an unbounded `wait`, so its effective bound is
the external runner timeout. Test `147` reached that limit after 900.8 seconds
and is recorded as TIMEOUT. Its worker stack is preserved in the private results.

The first segment ran from 06:42:48 to 07:03:53 UTC. The post-timeout audit
found no matching test workers, only the original Azure CIFS host mount,
unchanged monitored settings and firewall rules, and kernel taint still zero.
Free space was 1213 MiB locally, 1906 MiB on TEST, and 1929 MiB on SCRATCH.
The next segment resumed only the 219 NOT_RUN entries; it did not rerun `147`
or replace any completed result.

The first continuation ran from 07:05:22 to 07:28:32 UTC. Tests `148`, `150`,
and `151` passed; `149` skipped because no established SMB connection was
detected. Test `150` took 466.2 seconds. Test `152` timed out after 901.1 seconds;
its full log contains no completed phase, so the precise stalled operation is
not established. The second audit found no matching workers, unchanged
monitored settings and firewall rules, kernel taint zero, and 1212 MiB free
locally. The remaining 214 tests resumed in a new segment, preserving both
timeouts and all prior results.

The final continuation ran from 07:30:04 to 08:10:49 UTC and recorded 167 PASS,
12 FAIL, and 35 SKIP without another stop. Tests `256`, `275`, and `311`, which
timed out on Azure, passed here in 253.9, 93.8, and 141.5 seconds respectively.
Test `302` passed in 507.3 seconds. These are observations under different
backends and fixtures, not a controlled performance comparison.

## Setup Lifecycle

This is a temporary test service, not a replacement boot-time SMB service.
The private tools under `/opt/ksmbd-xfstests-3.5.3`, server configuration
`/etc/ksmbd-xfstests-20260925.conf`, dedicated account, private user database
under `/var/lib/ksmbd-xfstests-20260925`, and protected credentials can be
retained for future runs. The ext4 images under `/run/ksmbd-xfstests-20260925`
are RAM-backed and do not survive reboot. No systemd service was enabled at boot.

After execution, the audit found no matching test workers and no processes
retaining the test CIFS mounts. The owned ksmbd instance was shut down before
restarting `smbd`; Samba was verified active with its listener back on
`127.0.0.1:445`. The transient ksmbd service is stopped, and its owned stale lock
was removed only after verifying that the recorded daemon PID had exited.

Both ext4 mounts were normally unmounted, their loop devices (`/dev/loop9` and
`/dev/loop16`) released, and the tmpfs unmounted. This discarded the disposable
RAM-backed image contents. No mountpoint was recursively deleted. The retained
configuration is not a running ksmbd service: backing images/filesystems must be
recreated before a future run, with Samba/port-445 coordination repeated.

The private `restoration-audit.json` records the final checks at 08:12:19 UTC:

- Original Azure host mount preserved; no ksmbd CIFS host mounts remained.
- Monitored CIFS settings and file-leases setting matched the baseline.
- Normalized IPv4 and IPv6 firewall rules matched the baseline.
- Kernel taint remained zero; no BUG/Oops/panic/KASAN/OOM/CPU-warning match was
  found in the run interval. This is a scoped diagnostic check, not proof of
  the absence of all kernel issues.
- Available memory was 11696 MiB after releasing the fixture; local disk free
  space was 1199 MiB. Before release, TEST and SCRATCH had 1852 and 1929 MiB free.

Tests can reset counters and caches, so unchanged monitored settings do not
imply that all global runtime state was unchanged. No test repairs, commits,
or pushes were made as part of this ksmbd run.
