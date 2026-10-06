# CIFS Test Results: 2026-09-17

Historical report. See [cifs-results-20261006.md](cifs-results-20261006.md) for
newer outcomes and commit selection. Local profiles, review notes, raw results
and held candidate sources referenced below are not included with this report.

## Summary

**Latest observed Samba results, not a fresh full-suite run.** This page covers
all 302 numbered tests present in the reviewed working tree, including 33
untracked additions. Test IDs are sparse; the highest ID is `404`.

For each test, the ledger selects its newest valid xUnit testcase by suite
timestamp from the two September result roots listed below. A PASS records an
observed result, not proof that every assertion or optional path is correct.
Older results may predate repairs. Skips are not passes.

| Latest Recorded Runtime Outcome | Count |
| --- | ---: |
| PASS | 235 |
| FAIL | 9 |
| SKIP | 58 |
| Total | 302 |

Only **12 tests were rerun in the latest follow-up: 1 PASS, 6 FAIL, 5 SKIP**.
The other 290 latest runtime outcomes come from earlier September runs.
Nine Kerberos tests have only static/fixture validation of their repaired code;
their old runtime SKIPs are included above and explicitly identified below.

No fresh Windows Server or Azure Files results are available for this review.
Their March results remain historical in
[cifs-results_latest.md](cifs-results_latest.md) and
[cifs-results.md](cifs-results.md).

## Fresh Follow-Up

These runs used the original checkout at `6628667d` plus its uncommitted repairs,
not the separate upstream-merge worktree. Test `192` exercised all three owned
socket resets and checked read data, directory inventory, modes, and timestamps.

| Test | Result | Detail |
| --- | --- | --- |
| [108](tests/cifs/108) | SKIP | One non-RSS server interface cannot supply the requested channels. |
| [192](tests/cifs/192) | PASS | Read, directory, and metadata reconnect workload passes after removing the false baseline-mode gate. |
| [194](tests/cifs/194) | FAIL | Oversized-password diagnostic is printed, but mount.cifs returns success. |
| [244](tests/cifs/244) | SKIP | Linux file leases are disabled. |
| [320](tests/cifs/320) | SKIP | Cannot isolate exactly one new DFS target socket; no reset was injected. |
| 343 | SKIP | Linux file leases are disabled. |
| 349 | FAIL | Native F_GETLK query reports a conflict with a lock held by the same process. |
| 360 | FAIL | Directory chmod 0755 is reported as 0777 through cifsacl. |
| 385 | SKIP | Server does not advertise SMB3 directory leasing. |
| [390](tests/cifs/390) | FAIL | Negotiated SMB3 POSIX statvfs returns EIO. |
| 395 | FAIL | Requested mode 0755 is reported as 0777 for both source and copied ACL. |
| 401 | FAIL | XATTR_CREATE on an existing attribute succeeds instead of EEXIST. |

Fresh result segments are under `results-runs/cifs-remaining-review-20260917/`:
`remaining-192`, `remaining-320`, and `remaining-contracts`. Outcomes were checked
against xUnit, not inferred from the runner exit code. No test timed out in this
12-test follow-up.

## All Latest Failures

| Test | Latest Evidence | Failure | Disposition |
| --- | --- | --- | --- |
| [191](tests/cifs/191) | 2026-09-16, multichannel rerun | Default 2 GiB workload exhausted the share's backing storage. | Capacity/fixture limitation; do not attribute ENOSPC alone to a CIFS defect. |
| [194](tests/cifs/194) | Fresh follow-up | `Converted password too long!` with a success exit status. | Mount-helper error handling; retain negative-control assertion. |
| [221](tests/cifs/221) | 2026-09-16, failure rerun | Mode 0755 changed to 1766 after remount; expected mode SID missing. | CIFS/Samba ACL mapping investigation required. |
| [238](tests/cifs/238) | 2026-09-16, failure rerun | Plain O_CREAT missed IN_CREATE; O_EXCL control worked. | Creation-notification regression remains; not rerun in the latest follow-up. |
| 349 | Fresh follow-up | Same-process F_GETLK assertion fails with native C ABI. | Exact native helper passes on local ext4. |
| 360 | Fresh follow-up | File chmod transitions pass; directory 0755 reports 0777. | Keep mode-round-trip assertion. |
| [390](tests/cifs/390) | Fresh follow-up | statvfs returns EIO after POSIX metadata/data checks. | Earlier exact local control passes; negotiated support is not a reason to skip a failed operation. |
| 395 | Fresh follow-up | Semantically matching copied DACL reports mode 0777 instead of 0755. | Client/server ACL interpretation needs investigation. |
| 401 | Fresh follow-up | Existing-attribute XATTR_CREATE does not return EEXIST. | Earlier local control passes; retain errno assertion. |

These nine are observed failures, not nine proven kernel bugs. The six failures
in the remaining-test review exclude the older `191`, `221`, and `238` failures.

## Complete Outcome Lists

Every ID below denotes a `cifs/NNN` test. The lists are disjoint and cover the
302-test working-tree inventory exactly.

### PASS: 235

```text
001 100 101 102 103 104 105 109 111 112 113 114 115 116 117 118 119 120 121
122 123 124 125 126 127 128 129 130 131 132 133 135 136 138 139 140 141 142 143
144 145 146 147 148 150 151 152 153 154 155 156 157 159 160 161 162 164 165 166
169 170 171 172 173 174 175 178 179 182 183 184 186 187 188 190 192 193 195 196
198 199 200 201 202 206 207 208 209 210 211 212 213 214 215 216 217 218 219 222
223 226 227 228 230 231 233 235 236 237 239 241 242 243 245 246 247 249 250 251
253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272
273 274 276 277 278 279 280 281 282 283 284 285 286 287 288 290 291 292 293 294
295 296 297 298 299 300 301 302 303 304 305 306 307 308 310 311 312 313 314 316
317 319 321 322 334 335 336 337 338 339 340 341 342 344 346 347 348 350 351 352
353 354 357 358 359 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375
376 380 381 382 383 384 386 388 389 393 394 396 398 399 400 403
```

### FAIL: 9

```text
191 194 221 238 349 360 390 395 401
```

### SKIP: 58

```text
106 107 108 110 134 137 149 158 163 167 168 176 177 181 185 189 197 203 220
224 225 229 232 234 240 244 248 252 275 289 315 318 320 323 324 325 326 327 328
329 330 331 332 333 343 345 355 356 377 378 379 385 387 391 392 397 402 404
```

`289` is recorded as SKIP by the September run. The March report's policy of
counting its exclusion as FAIL is historical and is not applied to this ledger.

## Remaining-Test Coverage

The follow-up reviewed 43 uncommitted tests; 11 received additional repairs.
Current-code validation for that subset is tracked separately from old runtime
records:

| Latest Review Disposition | Count | Tests |
| --- | ---: | --- |
| PASS | 1 | 192 |
| FAIL | 6 | 194, 349, 360, 390, 395, 401 |
| SKIP | 27 | 106, 107, 108, 149, 177, 232, 244, 275, 315, 318, 320, 323, 324, 325, 343, 345, 355, 356, 377, 378, 379, 385, 387, 391, 392, 397, 402 |
| Static/fixture only after repair | 9 | 326, 327, 328, 329, 330, 331, 332, 333, 404 |

The nine static/fixture-only cases have older SKIP records in the complete lists;
their repaired Kerberos paths were not rerun with already-rejected credentials.
Only the 12 tests in the fresh table were rerun in this follow-up. Syntax checks,
fixtures, and builds do not establish a live PASS for the other tests.

The earlier 62 passing candidates were committed and pushed. The newly passing
`192` repair is now committed locally as `4cdea47e`, without the other 42 review
candidates or documentation changes. That commit has not been pushed.

Important remaining prerequisites include multiple usable channels, directory
leasing, native symlinks, snapshot enumeration, NFS reparse nodes, short DFS TTL,
an isolated DNS-switch fixture, dedicated non-root credential UIDs, and working
Kerberos authentication. The observed fixture has one non-RSS interface, Linux
leases disabled, and DFS referral TTL of 600 seconds. A server restart, module
reload, or global DFS cache purge requires explicit dedicated-host opt-in.

## Environment and Provenance

- Client: Linux `7.3.0-rc2+`, x86-64; mount.cifs `7.2`.
- Server: local Samba `4.21.4-Ubuntu-4.21.4+dfsg-1ubuntu3.5`.
- Local-only profile: `local.config.samba`, section `smb3`; dedicated
  test and scratch shares. Credentials and raw debug logs must remain private.
- Earlier source root: `results-runs/cifs-review-20260916/`.
- Latest follow-up root: `results-runs/cifs-remaining-review-20260917/`.
- 468 valid testcase records were considered. Eight older XML files contain
  invalid control characters and were excluded; each affected test has a newer
  valid result. All 302 tests have a valid selected result. File modification
  time breaks ties between identical suite timestamps.
- Local-only review and repair detail: `cifs-review-20260916.md`.
- Upstream merge `19378166` includes kdave/master `a370dcbe` and passed a full
  build plus 327 shell syntax checks in the separate sync worktree. No live CIFS
  run of that merged harness is claimed by this page.
- The latest follow-up left Samba active, Linux leases at 0, the unrelated stale
  host mount intact, and no private CIFS mounts in the host namespace. Its final
  capacity observation was 1442 MiB free; this is insufficient for full stress
  or fill workloads.

Keep historical tables dated. Future updates should distinguish fresh executions
from retained results, preserve failure reproducers, and never treat a skip or
an untested repaired path as a pass.
