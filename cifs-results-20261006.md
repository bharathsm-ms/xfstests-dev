# CIFS Cross-Server Results and Commit Selection: 2026-10-06

## Interpretation

This is a latest-observed ledger of **305 local test IDs**, not a fresh
cross-server run and not a claim that all 305 test sources are committed.
It includes held local candidates so that their failures remain visible.
An outcome applies to the source and fixture used for that attempt. Older
Windows, Azure and ksmbd results do not validate today's repaired sources.
SKIP is not PASS, and FAIL is not automatically a server or kernel defect.

P = PASS; F = FAIL; S = test-reported SKIP; T = external-runner TIMEOUT;
D = deliberately deferred without execution; - = outside that run's inventory.
The matrix normalizes historical NOT_RUN for test 168 to D, not S.

| Server / Evidence Scope | PASS | FAIL | SKIP | TIMEOUT | Deferred | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Samba, Oct 6 full run plus supplement | 240 | 33 | 32 | 0 | 0 | 305 |
| Azure, Oct 3-6 combined latest attempts | 207 | 33 | 61 | 3 | 1 | 305 |
| Windows, Oct 1 coverage run plus Oct 3 review | 219 | 30 | 55 | 0 | 1 | 305 |
| ksmbd, Sep 25 published suite | 209 | 17 | 41 | 2 | 0 | 269 |

Samba uses only the latest tested server, **4.22.11**, with the Oct 6 results.
Older Samba results remain historical and are not combined into this column.
The original Samba 4.22.11 full run was **231 PASS, 33 FAIL, 41 SKIP**.
Its ten-test supplement was **9 PASS, 0 FAIL, 1 SKIP**: PASS for
`102 137 149 158 203 215 329 356 404`, SKIP for `318`. The nine passes
replace nine earlier skips in the derived ledger, not in the saved original.

Windows uses the later Oct 1 coverage run (211 PASS, 21 FAIL, 36 SKIP,
1 deferred), then the 48 Oct 3 candidate outcomes. The earlier functional
run (209 PASS, 22 FAIL, 37 SKIP, 1 deferred) remains separately documented in
[cifs-results-windows-20261001.md](cifs-results-windows-20261001.md).
The Windows edition/build was not identified. Both published Windows runs and
the [ksmbd run](cifs-results-ksmbd-20260925.md) used revision `1ebff9ed`.
ksmbd had multichannel, SMB2 leases and durable handles disabled.

Azure combines the latest observed outcome for each test across the main Azure
Files endpoint and the later canary and preproduction probes. "Azure Primary"
previously meant the main endpoint, not a different server product. Its ledger
contains 321 actual invocations including retries; the two additional endpoints
ran four tests each. This combined column is not a single-endpoint full-suite run.
For IDs not rerun on those endpoints, the main endpoint's result is retained.
Preproduction supplies the latest TIMEOUT for `275` and FAIL for `385`, replacing
the main endpoint's SKIPs. Those failures are not attributed to the main endpoint.
The endpoint-specific observations are preserved below.

Test 168 remains deferred for capacity safety on both Azure and Windows. The
older [Azure published-suite report](cifs-results-azure-20260924.md) and
[September Samba ledger](cifs-results-20260917.md) are retained as history.

## Selected for This Commit

**19 tests: five repairs and fourteen additions.** Every selected script and
its expected output matches the SHA-256 recorded for a passing Oct 6 Samba
attempt. Selection also considers assertions, prerequisite gates, bounded
operations, cleanup and helper dependencies; a PASS alone is insufficient.
This is a conservative local commit selection, not upstream approval or an
all-server compatibility certification.

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

The commit includes the restart/cleanup support in common/cifs_test, each new
expected-output file and only the selected additions to the group registry.
Other pending helper, harness, README and runner changes are not included.
No test assertions were changed during this commit-selection review.

### Fixture Requirements

Credential tests 158/203/356 require a separate same-domain server account in
`CIFS_CRED_FILE2`, not a copy of the primary account. Tests 203/356 additionally
require a dedicated non-root `CIFS_MULTIUSER_UID`. The successful Samba
credential fixture disabled leases because lease-enabled cleanup produced
Samba share-mode errors. That cleanup problem is not claimed fixed.

The Azure F for 356 is an older source using the same server credentials for
both UIDs, for which the separate-session assertion was inappropriate. The
new distinct-credential version passed Samba only; it was not rerun on Azure.
Historical Windows/Azure/ksmbd passes for 215 predate its remount repair.

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
and an isolated client. These opt-ins are not enabled by this commit.

### Held Pending Changes

These **20 pending test changes are excluded**, without changing their saved
outcomes or deleting their working-tree files. A held failure can still be a
useful reproducer; attribution and submission readiness are separate questions.

| Tests | Reason to Hold |
| --- | --- |
| 192 | Samba passes, but current Azure reconnect failure and historical Windows/ksmbd failures need attribution. |
| 194 | Oversized-password helper negative control still fails. |
| 225, 378, 402 | Reparse behavior fails on tested Windows paths; no supported cross-server resolution. |
| 236 | PASS on Samba/Azure, but registered cache plus successful reread does not assert actual FS-Cache disk use. |
| 275, 345, 385 | Unresolved directory-cache/lease assertions; preproduction also records timeout/failure. |
| 318 | No positive short-TTL validation; standard Samba symlink referrals return fixed 600 seconds. |
| 325 | Cipher parser returns a name but test expects numeric hexadecimal IDs. |
| 343 | Duplicates basic lease acquisition/release already covered by repaired 244; consolidate before adding. |
| 349 | F_GETLK conflict/type assertion failures need isolation. |
| 360, 395 | ACL/mode round-trip failures unresolved. |
| 377 | Module-reload path unvalidated; installed and instrumented loaded modules differ. |
| 391 | Direct systemctl restart bypasses the private-server controller. |
| 397 | Latest dedicated Samba recovery run fails, despite an earlier pass. |
| 401 | Xattr create/replace assumptions and negative-control failures unresolved. |
| 405 | Samba and Windows pass; Azure open-file worker fails during channel resize. |

Tests already committed before this selection, including 315, 320, 332, 355,
365, 390, 392, 403 and 407, are not new additions in this commit. Their matrix
outcomes remain visible, including historical failures and skips.

## Azure Directory-Lease Probes

These four-test targets ran after the main endpoint's ledger on Oct 6. Their
latest observations are included in the combined Azure column; this table
preserves the endpoint-specific results. Neither probe is a full-suite run.

| Test | Canary | Preproduction |
| --- | --- | --- |
| cifs/275 | S | T |
| cifs/345 | S | S |
| cifs/355 | S | S |
| cifs/385 | S | F |

Canary skipped all four because directory leasing was not advertised.
Preproduction 345/355 skipped because reusable enumeration caching was not
observed; 275 timed out after the 600-second limit plus termination grace
(630.5 seconds); 385 observed no expected lease break. Preproduction did
exercise lease-invalidation code, so its skips are not proof of absent support.

## Coverage Scope

All numbers below measure the Linux CIFS client, not server implementation
coverage: 31,508 lines, 1,179 functions and 22,392 branches across 47 reportable
C sources / 48 GCOV objects. Headers and exception branches are excluded.

| Measurement | Lines | Functions | Branches |
| --- | ---: | ---: | ---: |
| Samba Oct 6 fresh | 17,721 (56.24%) | 843 | 7,830 |
| Samba after no-reset supplement | 18,052 (57.29%) | 852 | 8,056 |
| Azure main endpoint, before additional probes | 15,659 (49.70%) | 753 | 6,900 |
| Azure combined endpoints, cumulative | 16,100 (51.10%) | 769 | 7,107 |
| Windows Oct 1 independent coverage run | 15,918 (50.52%) | 763 | 6,891 |

Samba gained 331 unique lines relative to the preserved fresh baseline,
including fixture/debug/audit and failed/skipped attempts. The original
zero-based capture was preserved; the supplement did not reset counters,
change Samba/kernel/module/dialect or merge historical/generic/other-server
hits. The full suite includes tests with their own mount-option choices;
the unchanged SMB 3.1.1 claim applies to the supplemental fixture.
Azure's 51.10% is cumulative across its three endpoints, not standalone
preproduction coverage. These measurements must not be summed or unioned into
a new reported measurement. No live tests or coverage operations were run
during this documentation/commit review.

## Evidence Provenance

Saved raw evidence is intentionally local-only and is not committed. The
paths below are provenance identifiers, not portable repository links.
Credentials, profiles, raw logs, GCOV archives and build artifacts are excluded.

- Samba base: `results-runs/samba422-fresh-cifs-20261006-retry/suite-status.tsv`.
- Samba overlay: `results-runs/samba422-supplement-final-20261006/suite-status.tsv`.
- Matching test/output hashes: each Samba root's `source-sha256.json`.
- Azure baseline (main endpoint): `results-runs/azure-cifs-multiuser-leases-20261006/latest-cifs-status.tsv`.
- Windows base: `results-runs/cifs-windows-coverage-20261001.KJqXtj7R/suite-status.tsv`.
- Windows overlay: `results-runs/local-tests-review-20261003/matrix.tsv`.
- ksmbd: reconciled complete lists in [cifs-results-ksmbd-20260925.md](cifs-results-ksmbd-20260925.md).
- Azure probes: `results-runs/azure-canary-directory-leases-20261006` and `results-runs/azure-preprod-directory-leases-20261006`, each with its saved suite status and report.

## Complete Per-Test Matrix

| Test | Samba | Azure | Windows | ksmbd |
| --- | --- | --- | --- | --- |
| cifs/001 | P | F | P | P |
| cifs/100 | P | P | P | P |
| cifs/101 | P | P | P | P |
| cifs/102 | P | P | S | P |
| cifs/103 | F | P | F | P |
| cifs/104 | P | P | P | P |
| cifs/105 | P | P | P | S |
| cifs/106 | P | P | P | F |
| cifs/107 | P | P | P | S |
| cifs/108 | P | P | P | F |
| cifs/109 | P | P | P | P |
| cifs/110 | S | S | S | S |
| cifs/111 | P | S | P | P |
| cifs/112 | P | P | P | P |
| cifs/113 | P | P | P | P |
| cifs/114 | P | P | P | P |
| cifs/115 | P | P | P | P |
| cifs/116 | P | F | P | P |
| cifs/117 | P | P | P | P |
| cifs/118 | P | P | P | P |
| cifs/119 | P | P | P | P |
| cifs/120 | P | F | P | P |
| cifs/121 | P | P | P | P |
| cifs/122 | P | P | P | F |
| cifs/123 | F | F | P | P |
| cifs/124 | P | P | P | P |
| cifs/125 | P | P | P | F |
| cifs/126 | P | F | P | P |
| cifs/127 | P | P | P | P |
| cifs/128 | P | P | P | P |
| cifs/129 | P | P | P | P |
| cifs/130 | P | P | P | P |
| cifs/131 | P | P | P | P |
| cifs/132 | P | P | P | P |
| cifs/133 | F | P | P | P |
| cifs/134 | S | S | S | S |
| cifs/135 | P | P | P | P |
| cifs/136 | P | P | P | P |
| cifs/137 | P | P | P | S |
| cifs/138 | P | P | P | P |
| cifs/139 | P | P | P | P |
| cifs/140 | P | P | P | P |
| cifs/141 | P | P | P | P |
| cifs/142 | P | P | P | P |
| cifs/143 | P | P | P | P |
| cifs/144 | P | P | P | P |
| cifs/145 | P | P | P | P |
| cifs/146 | P | P | F | P |
| cifs/147 | P | P | P | T |
| cifs/148 | F | P | P | P |
| cifs/149 | P | S | S | S |
| cifs/150 | P | P | P | P |
| cifs/151 | F | P | P | P |
| cifs/152 | P | F | P | T |
| cifs/153 | P | P | P | P |
| cifs/154 | P | P | P | P |
| cifs/155 | P | P | P | P |
| cifs/156 | P | P | P | P |
| cifs/157 | P | P | P | F |
| cifs/158 | P | S | S | S |
| cifs/159 | P | P | P | P |
| cifs/160 | P | P | P | P |
| cifs/161 | P | P | P | P |
| cifs/162 | P | P | P | P |
| cifs/163 | S | S | S | S |
| cifs/164 | P | F | P | P |
| cifs/165 | P | P | P | P |
| cifs/166 | F | P | P | S |
| cifs/167 | F | S | P | S |
| cifs/168 | S | D | D | S |
| cifs/169 | P | P | P | P |
| cifs/170 | F | P | P | S |
| cifs/171 | F | P | P | S |
| cifs/172 | S | S | P | S |
| cifs/173 | P | P | P | P |
| cifs/174 | P | P | P | P |
| cifs/175 | P | P | P | P |
| cifs/176 | S | S | S | S |
| cifs/177 | P | P | P | S |
| cifs/178 | P | F | S | P |
| cifs/179 | F | F | P | P |
| cifs/181 | S | S | S | S |
| cifs/182 | P | P | P | P |
| cifs/183 | S | P | P | P |
| cifs/184 | P | P | P | P |
| cifs/185 | S | S | S | S |
| cifs/186 | P | P | P | P |
| cifs/187 | P | P | P | P |
| cifs/188 | S | P | P | P |
| cifs/189 | S | S | S | S |
| cifs/190 | P | P | P | P |
| cifs/191 | F | F | F | S |
| cifs/192 | P | F | F | F |
| cifs/193 | P | P | P | P |
| cifs/194 | F | F | F | F |
| cifs/195 | P | P | P | P |
| cifs/196 | P | P | P | P |
| cifs/197 | S | S | S | S |
| cifs/198 | P | P | F | F |
| cifs/199 | P | P | P | P |
| cifs/200 | P | P | P | P |
| cifs/201 | P | P | P | P |
| cifs/202 | P | P | P | P |
| cifs/203 | P | S | S | S |
| cifs/206 | P | F | S | P |
| cifs/207 | F | F | P | P |
| cifs/208 | P | P | P | P |
| cifs/209 | P | P | P | P |
| cifs/210 | P | P | P | P |
| cifs/211 | P | P | P | P |
| cifs/212 | P | P | P | P |
| cifs/213 | P | P | P | P |
| cifs/214 | P | P | P | P |
| cifs/215 | P | P | P | P |
| cifs/216 | P | F | F | P |
| cifs/217 | P | P | P | P |
| cifs/218 | P | P | P | P |
| cifs/219 | P | P | P | P |
| cifs/220 | S | S | S | S |
| cifs/221 | F | P | F | P |
| cifs/222 | S | P | P | P |
| cifs/223 | P | P | P | P |
| cifs/224 | S | S | S | S |
| cifs/225 | S | F | F | S |
| cifs/226 | P | S | P | P |
| cifs/227 | P | S | P | P |
| cifs/228 | P | P | P | P |
| cifs/229 | S | S | S | S |
| cifs/230 | P | P | P | P |
| cifs/231 | P | P | P | P |
| cifs/232 | P | F | P | S |
| cifs/233 | P | S | P | P |
| cifs/234 | S | S | S | S |
| cifs/235 | P | P | P | P |
| cifs/236 | P | P | P | P |
| cifs/237 | P | P | P | P |
| cifs/238 | F | F | F | F |
| cifs/239 | P | P | P | P |
| cifs/240 | S | S | S | S |
| cifs/241 | P | P | P | P |
| cifs/242 | P | P | P | P |
| cifs/243 | P | P | P | P |
| cifs/244 | P | P | S | S |
| cifs/245 | P | P | P | P |
| cifs/246 | P | P | P | P |
| cifs/247 | S | P | P | P |
| cifs/248 | S | S | S | S |
| cifs/249 | P | P | P | P |
| cifs/250 | P | P | P | P |
| cifs/251 | P | P | F | P |
| cifs/252 | S | S | S | S |
| cifs/253 | S | P | P | P |
| cifs/254 | P | S | S | P |
| cifs/255 | P | S | P | P |
| cifs/256 | P | T | P | P |
| cifs/257 | P | P | P | P |
| cifs/258 | P | P | P | P |
| cifs/259 | P | P | P | P |
| cifs/260 | P | P | P | P |
| cifs/261 | P | P | P | P |
| cifs/262 | P | P | P | P |
| cifs/263 | P | P | P | P |
| cifs/264 | P | P | P | P |
| cifs/265 | P | P | P | P |
| cifs/266 | F | P | P | P |
| cifs/267 | P | P | P | P |
| cifs/268 | P | P | P | P |
| cifs/269 | P | P | P | P |
| cifs/270 | P | P | P | P |
| cifs/271 | P | P | P | P |
| cifs/272 | P | P | P | P |
| cifs/273 | P | P | P | P |
| cifs/274 | P | P | P | P |
| cifs/275 | F | T | F | P |
| cifs/276 | P | P | P | P |
| cifs/277 | P | P | P | P |
| cifs/278 | P | P | P | P |
| cifs/279 | P | P | P | P |
| cifs/280 | P | P | P | P |
| cifs/281 | S | P | P | P |
| cifs/282 | P | P | P | P |
| cifs/283 | P | P | P | P |
| cifs/284 | P | P | P | P |
| cifs/285 | P | P | P | P |
| cifs/286 | P | P | P | P |
| cifs/287 | P | P | P | P |
| cifs/288 | P | P | P | P |
| cifs/289 | S | S | S | S |
| cifs/290 | P | P | P | P |
| cifs/291 | P | P | P | P |
| cifs/292 | P | P | P | P |
| cifs/293 | P | P | P | P |
| cifs/294 | P | P | P | P |
| cifs/295 | P | P | P | P |
| cifs/296 | P | P | P | P |
| cifs/297 | S | P | P | P |
| cifs/298 | P | P | P | P |
| cifs/299 | P | P | P | P |
| cifs/300 | P | P | P | P |
| cifs/301 | P | P | P | P |
| cifs/302 | P | P | P | P |
| cifs/303 | P | P | P | P |
| cifs/304 | P | P | F | P |
| cifs/305 | P | P | P | P |
| cifs/306 | P | P | P | P |
| cifs/307 | P | P | P | P |
| cifs/308 | P | P | P | P |
| cifs/310 | F | F | F | P |
| cifs/311 | P | T | P | P |
| cifs/312 | P | P | P | P |
| cifs/313 | P | S | S | S |
| cifs/314 | P | S | S | S |
| cifs/315 | S | S | S | - |
| cifs/316 | P | S | S | S |
| cifs/317 | F | S | S | S |
| cifs/318 | S | S | S | - |
| cifs/319 | P | S | S | S |
| cifs/320 | P | S | S | - |
| cifs/321 | P | S | S | S |
| cifs/322 | P | S | S | S |
| cifs/323 | P | S | S | - |
| cifs/324 | P | S | S | - |
| cifs/325 | F | S | S | - |
| cifs/326 | P | S | S | - |
| cifs/327 | P | S | S | - |
| cifs/328 | P | S | S | - |
| cifs/329 | P | S | S | - |
| cifs/330 | P | S | S | - |
| cifs/331 | P | S | S | - |
| cifs/332 | P | S | S | - |
| cifs/333 | P | S | S | - |
| cifs/334 | P | P | P | P |
| cifs/335 | P | F | F | P |
| cifs/336 | F | P | P | P |
| cifs/337 | P | P | P | P |
| cifs/338 | P | P | P | P |
| cifs/339 | P | P | P | P |
| cifs/340 | P | P | P | P |
| cifs/341 | P | F | F | F |
| cifs/342 | P | P | P | P |
| cifs/343 | P | P | S | - |
| cifs/344 | P | P | P | P |
| cifs/345 | F | S | F | - |
| cifs/346 | P | P | P | P |
| cifs/347 | P | P | P | F |
| cifs/348 | P | P | F | P |
| cifs/349 | F | F | F | - |
| cifs/350 | P | P | P | P |
| cifs/351 | P | F | F | P |
| cifs/352 | P | P | P | P |
| cifs/353 | P | P | P | P |
| cifs/354 | F | P | P | F |
| cifs/355 | P | S | P | - |
| cifs/356 | P | F | S | - |
| cifs/357 | P | P | P | P |
| cifs/358 | F | F | P | F |
| cifs/359 | P | P | P | P |
| cifs/360 | F | F | F | - |
| cifs/361 | P | P | P | P |
| cifs/362 | P | P | P | P |
| cifs/363 | P | P | P | P |
| cifs/364 | P | P | P | P |
| cifs/365 | P | P | P | P |
| cifs/366 | P | P | P | P |
| cifs/367 | P | P | P | P |
| cifs/368 | P | P | P | P |
| cifs/369 | P | P | P | P |
| cifs/370 | P | P | P | P |
| cifs/371 | P | P | P | P |
| cifs/372 | P | P | P | P |
| cifs/373 | P | P | P | P |
| cifs/374 | P | P | P | P |
| cifs/375 | P | P | P | P |
| cifs/376 | F | F | F | P |
| cifs/377 | S | S | S | - |
| cifs/378 | S | S | F | - |
| cifs/379 | P | S | S | - |
| cifs/380 | P | P | F | F |
| cifs/381 | P | P | P | P |
| cifs/382 | P | P | P | F |
| cifs/383 | P | P | P | P |
| cifs/384 | P | P | P | P |
| cifs/385 | F | F | F | - |
| cifs/386 | P | P | P | P |
| cifs/387 | P | S | S | - |
| cifs/388 | P | F | F | F |
| cifs/389 | P | P | P | P |
| cifs/390 | P | S | F | - |
| cifs/391 | S | S | S | - |
| cifs/392 | P | P | P | - |
| cifs/393 | F | F | P | P |
| cifs/394 | F | P | P | F |
| cifs/395 | F | F | F | - |
| cifs/396 | P | S | S | S |
| cifs/397 | F | S | S | - |
| cifs/398 | P | P | P | P |
| cifs/399 | P | P | P | P |
| cifs/400 | P | P | P | P |
| cifs/401 | F | F | F | - |
| cifs/402 | S | S | F | - |
| cifs/403 | P | P | P | P |
| cifs/404 | P | S | S | - |
| cifs/405 | P | F | P | - |
| cifs/406 | P | P | S | - |
| cifs/407 | P | S | P | - |