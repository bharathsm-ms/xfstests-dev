# CIFS xfstests README

This document describes the CIFS/SMB client test suite for xfstests.

For current outcomes, see the [cross-server results](cifs-results_latest.md),
[failure and skip reasons](cifs-results-failures-20261006.md), and
[run details and validation limits](cifs-results-20261006.md).

## Reproducible Samba profiles

These commands require the local fixture toolkit, which is not included in
the committed checkout. Raw evidence links below also refer to local archives;
the dated result reports provide the tracked summaries.

[tools/setup_all_samba.sh](tools/setup_all_samba.sh) is the parent entry point.
With no arguments it lists profiles; it does not modify the host. A run
configures a fresh local Samba fixture, runs the matching tests, and cleans
up before starting the next profile. This is preferable to independent setup
scripts that overwrite each other's global Samba settings. Recovery, oplock,
multichannel and authentication configurations are deliberately separate.

The canonical test selections are in
[configs/samba-profiles.json](configs/samba-profiles.json). The parent uses
[tools/run_samba_profiles.py](tools/run_samba_profiles.py), the existing
[fixture backend](tools/run_samba422_features.py), and the disposable
[Kerberos module](tools/samba_kerberos.py). Profile selections can include local
additions; verify that the selected scripts and helper tools are present in
your checkout before running. Tests are registered in
[tests/cifs/group.list](tests/cifs/group.list). Regenerate the list with
`make -C tests/cifs group.list` when adding numbered tests.

| Profile | Tests | Configuration |
| --- | --- | --- |
| `smoke` | generic/004, cifs/365 | Encrypted SMB3.1.1 I/O and mount validation |
| `directory-leases` | cifs/345, 355, 385 | SMB2 leases and SMB3 directory leases enabled |
| `multichannel` | cifs/405 | RSS-capable loopback interface, live channel resizing |
| `dfs` | cifs/320 | Separate root and two independently controlled target servers |
| `kerberos` | cifs/323, 324, 326, 328, 331, 333 | Disposable MIT realm, dedicated service/user keytabs |
| `recovery` | cifs/387, 397 | Durable handles, POSIX locking disabled, private restart controller |
| `oplocks` | cifs/349, 354, 360, 401 | Leases/multichannel disabled; SMB3 oplocks, locks, ACLs, xattrs |
| `posix` | cifs/390 | SMB3 Unix extensions enabled |
| `snapshots` | cifs/379 | Btrfs read-only snapshots with shadow_copy2 |
| `compression` | cifs/407 | Server filesystem compression, not SMB wire compression |
| `decrypt-offload` | cifs/406 | Encryption and an explicitly permitted private trace instance |
| `reparse` | cifs/225, 378, 402 | WSL/NFS special files and native symlink probes; may skip |
| `netbios` | cifs/403 | SMB3.1.1 on port 139; SMB1 remains disabled |

### Requirements

Use a dedicated Linux test VM with no unrelated CIFS workloads. This is a
local client/server lab runner, not a remote-server installer or an AD domain
provisioner. It does not install packages, create Unix accounts, edit
local.config, change the kernel, reload CIFS, or reset coverage counters.
`REPORT_GCOV` must be unset.

Install/build Samba **4.22 or newer**, including systemd readiness notification
support and the `btrfs`, `shadow_copy2`, and `streams_xattr` VFS modules.
4.22.11 is the validated version. The default prefix is `/opt/samba-4.22.11`;
use `--prefix /usr` for a suitable packaged installation. Packaged Samba 4.21
does not meet this fixture's requirements. Create a dedicated non-root Unix
account such as `xfstest`, or select an existing one with `--account`.

Build xfstests and its native helpers using the repository's normal build
instructions. Required tools include Python 3.10+, util-linux, iproute2,
cifs-utils, btrfs-progs, and xfsprogs. Kerberos additionally needs MIT
`krb5kdc`, `kdb5_util`, `kadmin.local`, `kinit`, `klist`, `kdestroy`, and
keyutils/request-key. `--check` lists missing commands without installing them.
Running fixtures needs root, mount/PID/network namespace privileges, loop
devices and Btrfs kernel support. Each sequential profile creates two sparse
512 MiB backing images beneath `/dev/shm`; allow at least 1 GiB free there.
Workspace, prefix and result paths must not contain whitespace.

### Commands

```bash
bash tools/setup_all_samba.sh --list
bash tools/setup_all_samba.sh --profiles directory-leases multichannel dfs kerberos --plan
bash tools/setup_all_samba.sh --profiles directory-leases multichannel dfs kerberos --check

sudo -n bash tools/setup_all_samba.sh \
  --profiles directory-leases multichannel dfs kerberos \
  --allow-host-network --allow-host-upcall --run

sudo -n bash tools/setup_all_samba.sh --profiles smoke dfs recovery --run
sudo -n bash tools/setup_all_samba.sh --profiles kerberos --tests cifs/323 \
  --allow-host-network --allow-host-upcall --run
sudo -n bash tools/setup_all_samba.sh --profiles decrypt-offload --allow-tracing --run
```

`--tests` accepts only a subset of one selected profile. Results default to a
new timestamped directory under `results-runs`; `--results PATH` selects a
different **new** directory. The parent serializes its own invocations and
refuses existing CIFS mounts or result directories. It keeps per-profile
configuration, preflight evidence, logs, xUnit reports and cleanup audits.
`summary.json` distinguishes PASS, FAIL, SKIP and ERROR. Test failures do not
prevent later profiles; setup errors, timeouts or unverified cleanup stop
the run. Exit 0 means no failures/errors, not that skipped tests passed;
exit 1 indicates test failure, and exit 2 indicates orchestration/prerequisite
or incomplete-result failure. Inspect skip reasons as well as the exit code.

Most fixtures use private network/mount/PID namespaces. Multichannel and
Kerberos use a temporary, previously unused `127.0.0.2/32` host loopback alias
and therefore require `--allow-host-network`. Samba must be able to bind
`127.0.0.2:445`; an existing wildcard SMB listener will conflict. The assigned
alias is removed and the original loopback configuration verified afterward.

Kerberos also requires `--allow-host-upcall`. It creates a random temporary
realm with KDC listeners only on `127.0.0.2:10088`, private database/keytabs and
ticket caches, plus a temporary rule in `/etc/request-key.d` matching only
the fixture's CIFS endpoint. Existing KDC services, databases, keytabs,
`/etc/krb5.conf` and host Samba configuration are not modified. The scoped
rule and KDC are removed/stopped before deleting private authentication data.
No realm passwords or keytabs are retained in the results.

Fixtures are not left running between commands. Generated run configurations
reference disposable paths and are evidence, not reusable post-cleanup mount
profiles. After interruption, inspect cleanup audits before rerunning. A
forced kill/reboot can bypass cleanup; preserve any leftover runtime until
its mounts/processes are investigated. Do not run against production hosts.

The old whole-host installer is available only via `--legacy-host-setup`.
It overwrites host configuration and recreates KDC data; do not use it on an
existing Samba/Kerberos host. Bare invocation no longer runs that installer.

### No-reset CIFS coverage supplement

[tools/run_samba_fresh_coverage.py](tools/run_samba_fresh_coverage.py) also supports
an explicit `--supplement-from` mode. It verifies a sealed zero-based baseline,
the loaded instrumented kernel/module, Samba binary and monotonically increasing
raw counters. It keeps Samba 4.22.11 and SMB 3.1.1 unchanged, with no module reload,
counter reset, generic tests or historical coverage merge. Omitting this option
selects the separate fresh-run workflow, which resets counters.

Monotonic counters alone do not establish Samba-only attribution. The October 7
cross-server runs added mixed-backend activity to the live counters, so those
counters cannot extend the earlier Samba-only baseline. A new isolated baseline
requires explicit approval for any counter reset or module reload. The commands
below apply only when the baseline's isolation requirements still hold.

```bash
python3 -B tools/run_samba_fresh_coverage.py --plan \
  --supplement-from coverage/samba-cifs-only-20261006
sudo -n env PYTHONDONTWRITEBYTECODE=1 python3 -B \
  tools/run_samba_fresh_coverage.py results-runs/new-samba-supplement \
  --supplement-from coverage/samba-cifs-only-20261006 --timeout 240
```

The ten existing tests are 102, 137, 149, 158, 203, 215, 318, 329, 356 and 404.
`--tests cifs/149` can restrict this set. Results must use a new directory.
The same dedicated-host requirements apply; temporary host-loopback aliases and
hostname/endpoint-scoped request-key rules are created and audited during cleanup.
There must be no concurrent CIFS workload. Inspect `suite-status.tsv` and
`complete.json`: successful orchestration alone does not mean every test passed.

For standalone runs, tests 158, 203 and 356 require `CIFS_CRED_FILE2` for a distinct
server account in the mount account's domain. Tests 203/356 also require a dedicated
non-root `CIFS_MULTIUSER_UID`. The supplement supplies namespace-local accounts,
private credential files and session keyrings; it never adds host Unix accounts.
It disables leases for the credential-only fixture because lease-enabled Samba
produced share-mode cleanup errors. Isolation, negative-authentication and distinct
session assertions remain enforced. Kerberos uses separate positive and ticketless
UIDs with private caches and a scoped upcall account namespace.

The capacity fixture uses two sparse 1536 MiB images and checks large-file data
after remount, without a host-wide cache drop. DNS changes are confined to the
private fixture and a unique hostname. Samba 4.22.11's standard DFS symlink-referral
implementation uses a fixed 600-second TTL: an attempted `msdfs:ttl=5` setting did
not change it, so 318 retains its short-TTL skip. No server rebuild or global DFS
cache flush is used. Saved reports include raw per-test boundaries and cumulative
HTML coverage; counts include fixtures and failed/skipped attempts as well as passes.

### Validation on 2026-10-03

The four-profile non-interactive run completed with **8 PASS, 3 FAIL, 0 SKIP**:
355, 405, 320 and all six Kerberos tests ran, together with 345 and 385.
Passing tests were 355, 320, 323, 324, 326, 328, 331 and 333. Tests 345/385
retained their directory-enumeration failures. Test 405's I/O worker exited
during channel resizing; its earlier coverage-run pass is not a guarantee
of repeatability. Mount validation 365 separately passed through the parent.
Assertions were not weakened. The other profiles reuse existing fixtures
and were not all rerun during this orchestration change.

All four cleanup audits passed. Host Samba PID/start identity, Samba/Kerberos
configuration and keytab/database hashes, request-key rules, loopback state
and host CIFS mounts were unchanged. Initial non-interactive startup failures
are retained separately; the runner now detaches stdin and checks the SMB
listener after the readiness notification. See the
[test summary](results-runs/samba-profiles-20261003-features-verified/summary.json)
and [host audit](results-runs/samba-profiles-20261003-features-verified/host-audit.json).
No coverage recapture/merge was performed for this workflow validation.

Run the unprivileged orchestration checks with:

```bash
python3 -B -m unittest discover -s tools -p test_samba_profiles.py -v
```

## Critical-feature additions (2026-10-02)

Tests `405`-`407` add multichannel resizing, decryption-offload checks, and
server filesystem compression checks. The following validation describes the
October 2 implementation checkpoint, not their latest cross-server outcomes.

| Test | Assertions | Requirements |
| --- | --- | --- |
| `cifs/405` | Remount one live session through 4, 2, 1, and 4 channels; retain connection/session identity and an open file; require verified I/O progress after every transition | SMB 3.1.1, a server capable of four channels, live `max_channels` reconfiguration, readable DebugData, Python 3 |
| `cifs/406` | Encrypted `cache=none` reads with `esize=0` and `esize=65536`; verify payloads and require `smb2_decrypt_offload` calls only for concurrent large reads with offload enabled | SMB 3.1.1 encryption, Python 3, tracefs function tracing, `CIFS_ALLOW_OFFLOAD_TRACE=yes` |
| `cifs/407` | Compression flag set/clear with read-only path fallback, writable and borrowed writable handles; data integrity; rejected unsupported flags, unlinked dentries, and `noserverino` fallback | SMB 3.1.1, stable server inode IDs, server-side file compression, compiled `src/cifs_compression` |

All three use private workspaces and credential-file mounts through
`common/cifs_test`; set `CIFS_CRED_FILE` for the target share. Build the native
helper with `make -C src cifs_compression`. The workloads use under 10 MiB of
remote data. They do not restart the server, reload CIFS, reset GCOV, or modify
global CIFS settings.

Test `406` uses its own bounded ftrace instance, but the traced kernel worker
cannot be filtered to a single mount. Enable its opt-in only on an isolated
client with no unrelated CIFS workloads. The disabled and below-threshold
controls must record zero worker calls; enabled large reads must record at
least one. A private trace does not by itself provide session attribution.

Bounded Samba validation on 2026-10-02: `406` passed with 225 offload-worker
calls and zero calls in all three controls; `405` skipped because the current server advertises one non-RSS
interface; `407` skipped because both compression capability probes returned
unsupported. The initial `406` run had a golden-output final-newline mismatch;
the corrected test passed on rerun. Evidence is retained separately in
`results-runs/cifs-critical-features-20261002` and
`results-runs/cifs-critical-features-20261002-retry-406`. Resize control flow and
compression ioctl assertions also passed local simulated-state checks, which
do not substitute for live validation on capable servers. No incremental LCOV
gain was measured during this implementation run.

At that checkpoint, fixture-dependent gaps included real two-target DFS
failover, Witness notification/move lifecycle, and controlled
protocol/allocation fault paths.
These need independent DFS targets, a Witness-capable server/daemon, or a
controlled server/KUnit fixture respectively; they are not covered by these
three additions. Later two-target DFS validation is recorded below.
Wire compression and SMB Direct also require different
kernel build options from that coverage build.

### Minimal recovery follow-up (2026-10-02)

The existing tests `387` and `397` now have an isolated execution mode in
[tools/run_samba422_features.py](tools/run_samba422_features.py). It requires
the separately installed Samba at `/opt/samba-4.22.11`, an existing `xfstest`
Unix account, Btrfs/loop support, `ss`, Python 3, and root namespace privileges.
Use fresh result/runtime names and run with no unrelated CIFS workloads:

```bash
run="samba422-recovery-$(date +%Y%m%d-%H%M%S)"
sudo -n env PYTHONDONTWRITEBYTECODE=1 \
  SAMBA422_HOST_NETNS="$(readlink /proc/self/ns/net)" \
  SAMBA422_HOST_MNTNS="$(readlink /proc/self/ns/mnt)" \
  unshare --net --mount --pid --fork --mount-proc \
    --kill-child=SIGKILL --propagation private \
  python3 -B tools/run_samba422_features.py \
    "$PWD/results-runs/$run" --runtime "/dev/shm/$run" --recovery
```

Recovery mode disables multichannel and sets `posix locking = no`, with
`durable handles = yes`, `kernel oplocks = no`, and `kernel share modes = no`.
The normal feature profile is unchanged. A root-private Unix control socket
routes restart requests only to the runner-owned Samba process group. A
configured but unavailable socket fails closed; without that setting, the
existing explicit restart opt-in still controls the host `smbd` service.

Test `397` keeps a descriptor open across an exact test-owned TCP disconnect,
then verifies I/O progress after three server restarts and checks final data.
TCP recovery cannot reopen an `EBADF` descriptor. Only the full-restart phase
permits an application reopen on `EBADF`; `EAGAIN` is retried on the same
descriptor within bounded waits. This does not assert persistent-handle
survival across a server restart.

Final xUnit result: **2 PASS, 0 FAIL, 0 SKIP**. Two earlier `397` attempts
exposed the need to distinguish restart `EBADF` from transient `EAGAIN`;
their failed results are retained. Host Samba PID/start time, firewall,
CIFS settings and kernel taint were unchanged; private runtime cleanup passed.

The same-build cumulative Samba aggregate increased from **58.55% to 58.70%
lines**, **74.30% to 74.39% functions**, and **36.62% to 36.76% branches**:
**47 new lines, 1 function (`smb2_set_replay`), and 31 branches**. This includes
fixture activity and all three attempts, not passing-tests-only coverage.
No counters were reset. Eight durable-v1 reconnect and file-reopen calls were
observed; the two durable-v2 reconnect helpers remain cold because this kernel
selects them for persistent handles, unsupported by this Samba backend.

Evidence: [final results](results-runs/samba422-recovery-20261002-verified),
[coverage gains](results-runs/samba422-recovery-20261002-gcov/coverage-gains.json),
and [function calls](results-runs/samba422-recovery-20261002-gcov/recovery-function-calls.json).
Independent DFS-target failover, Witness, directory-lease failures, and the
four-channel resize failure were outside this minimal follow-up.

### Samba-only 60% target (2026-10-02)

The next same-build Samba-only aggregate reached **60.11% line coverage**:
18,938 / 31,508 lines, 897 / 1,179 functions (**76.08%**), and
8,455 / 22,392 branches (**37.76%**). Compared with the recovery aggregate,
this adds **442 lines, 20 functions, and 223 branches**. No Windows results,
counter reset, kernel rebuild, module reload, or denominator exclusions were
used. Coverage includes fixture activity and failed/skipped attempts; it is
not a passing-tests-only metric.

| Phase | New Unique Lines | Cumulative Line Coverage |
| --- | ---: | ---: |
| Independent DFS-target failover | 208 | 59.36% |
| Host-loopback multichannel and directory-lease checks | 73 | 59.59% |
| Reparse probes | 0 | 59.59% |
| Oplock/lock/ACL/xattr checks | 14 | 59.64% |
| Mount and remount validation | 70 | 59.86% |
| SMB 3.1.1 NetBIOS session transport | 77 | 60.11% |

Four tests passed with substantive assertions: `320` stopped the active
DFS target and verified data through the alternate; `405` retained its
session and open-file I/O across 4 -> 2 -> 1 -> 4 channels; `365` rejected
42 malformed/conflicting mount cases and eight immutable remount changes
while preserving control data; `403` completed its I/O/metadata lifecycle
over port 139 and verified negotiated dialect `0x311`. SMB1 was never enabled.

Failures in that run were `345`/`385` stale directory enumeration, `354` stale
held-descriptor reads, `349` lock-query type mismatch, `360` ACL mode mismatch,
and `401` an unexpectedly successful negative xattr operation. Reparse tests
`225`, `378`, and `402` skipped as unsupported. An initial `320` skip led to
target-specific socket selection; an initial unassigned-loopback preflight
failed before tests ran. All attempts remain in the results.

The runner now supports these mutually exclusive opt-in profiles:

| Option | Default Tests | Fixture |
| --- | --- | --- |
| `--dfs` | `320` | Private referral root plus independently stoppable targets on 127.0.0.2 and 127.0.0.3, sharing disposable data |
| `--host-loopback` | Existing feature selection; use `--tests cifs/405` for resize | Host network namespace, owned temporary 127.0.0.2/32 alias, private mounts/processes/storage |
| `--oplocks` | `349 354 360 401` | SMB3-only server with leases disabled |
| `--netbios` | `403` | Private ports 445 and 139, both endpoints restricted to SMB 3.1.1 |

Use the recovery command above with a fresh name and the desired profile.
For `--host-loopback` only, omit `--net` from `unshare`. This mode temporarily
changes loopback addressing: obtain approval first. It refuses a pre-existing
alias or occupied endpoint, removes only its owned alias, and records exact
before/after address state. The packaged Samba service is not restarted.
Reparse tests and `365` can be selected with `--tests` in the normal private
profile. Tests `225` and `349` now use independent mounts for their remote
metadata and lock checks.

Host Samba PID/start time/configuration, firewall, CIFS settings, and kernel
taint were unchanged. Owned runtimes and the approved loopback alias were
removed; no severe kernel diagnostics were found. These checks do not remove
the older interrupted fixture recorded in the earlier feature report.

Evidence: [coverage gains](results-runs/samba60-20261002-gcov/coverage-gains.json),
[merged Samba trace](results-runs/samba60-20261002-gcov/all-samba-combined.info),
and [host audit](results-runs/samba60-20261002-gcov/audit-after.json).
The LCOV merge exactly matches an independent union of covered entities,
with archived input hashes and kernel/source identities verified.

## Suite coverage

The suite covers:

- File and directory semantics: create/read/write, truncate, mmap, sync,
  rename/unlink, hardlinks and symlinks, timestamps, directory enumeration,
  Unicode names, and path-length boundaries.
- Data integrity and allocation: sparse files, hole punching, zero ranges,
  seek boundaries, large files, splice/sendfile, and server-side copy via
  `copy_file_range`.
- Permissions and metadata: ownership and mode mapping, POSIX ACLs, `cifsacl`,
  security descriptors, extended attributes, and alternate data streams.
- Mount and protocol behavior: dialect negotiation, socket sharing, I/O-size
  options, remount transitions, mount-helper parsing, and SMB3 over port 139.
- Authentication and identity: Kerberos, credential-source precedence,
  `cifscreds`, multiuser sessions, and credential-cache/keyring isolation.
- Security: signing, SMB3 encryption and cipher negotiation, session-key
  reporting, and decrypt-offload checks.
- Caching and coherency: page and attribute caches, directory-handle reuse,
  cross-mount visibility and invalidation, and FS-Cache configuration checks.
- Locking and leases: advisory and byte-range locks, oplock/lease breaks,
  directory leases, deferred close, and handle reuse.
- Recovery and failover: disconnects during I/O, DNS re-resolution, DFS
  referrals and target failover, durable/persistent handles, and server
  restart recovery.
- Transport and flow control: multichannel setup, channel failover and
  resizing, credit pressure, and recovery from network stalls.
- Optional filesystem and server features: SMB3 POSIX extensions, reparse
  points, snapshots, quotas, SMB wire compression, and server-side filesystem
  compression.
- Diagnostics and controls: CIFS statistics, DebugData and open-file reporting,
  selected userspace-accessible IOCTLs/FSCTLs, and kernel module parameters.
- Error paths and regressions: invalid options and credentials, errno mapping,
  permission failures, ENOSPC recovery, and targeted data-corruption checks.
- Stress and performance: concurrent data/metadata and Git workloads,
  multi-mount consistency, lease floods, reconnect/writeback races, caching
  and copy benchmarks, and `rsize`/`wsize` sweeps.

These are test areas, not a claim that every path has been validated on every
server. Individual tests can require specific kernel/server capabilities,
tools, credentials, and isolated fixtures; a skip is not a pass.

## Historical results and review

The summaries below preserve earlier runs. For the latest-observed cross-server
matrix and validation details, see
[cifs-results_latest.md](cifs-results_latest.md) and
[cifs-results-20261006.md](cifs-results-20261006.md).

[Windows results: 2026-10-01](cifs-results-windows-20261001.md) records the
completed run of 269 published tests at `1ebff9ed`: **209 PASS, 22 FAIL, 37 SKIP,
0 TIMEOUT, 1 NOT_RUN**. All 268 selected tests finished; `168` was deliberately
deferred because its ENOSPC workload would consume approximately 353 GiB.
Original host mounts and monitored settings were preserved. See the report for
complete ID lists, qualified failure/skip findings, and remote-cleanup limits.

[ksmbd results: 2026-09-25](cifs-results-ksmbd-20260925.md) records the completed
run of the same 269 published tests against the in-tree ksmbd server:
**209 PASS, 17 FAIL, 41 SKIP, 2 TIMEOUT, 0 NOT_RUN**. Tests `147` and `152`
timed out. This local baseline used two bounded ext4 shares, with multichannel,
SMB2 leases, and durable handles disabled. All tests were reached; Samba was
restored and the temporary RAM-backed fixtures released. See the report for
complete ID lists, failure qualifications, and retained setup details.

[Azure Files results: 2026-09-24](cifs-results-azure-20260924.md) records the completed
run of the 269 published tests at `1ebff9ed`: **201 PASS, 23 FAIL, 41 SKIP,
3 TIMEOUT, 1 NOT_RUN**. Tests `256`, `275`, and `311` timed out; `168` was deferred
because its ENOSPC workload would fill approximately 168 GiB. All other tests
were reached, and post-run host checks passed. See the report for complete ID
lists, failure qualifications, and cleanup limits.

[Samba results: 2026-09-17](cifs-results-20260917.md) is the Samba pass/fail list:
**235 PASS, 9 FAIL, 58 SKIP** across 302 tests. These are latest observed results
as of that report, from multiple September runs, not a fresh full-suite run or
blanket correctness certification. Historical passes can predate repairs.

The September follow-up reviewed 43 remaining tests and repaired 11. Twelve targeted
Samba reruns produced **1 PASS, 6 FAIL, 5 SKIP**. Test `192` passed its real
read, directory, and metadata reconnect workload. The other 31 tests received
static review without a fresh live run. All 43 scripts and four helpers passed
Bash syntax and warning-level ShellCheck with framework-variable exclusions
at that review checkpoint; this does not validate later working-tree changes.

The approved 62-test passing series was already committed and pushed. The
additional `192` repair, `4cdea47e`, is published through merge `1ebff9ed`.
See [the detailed review](cifs-review-20260916.md) for repair history, the six retained
follow-up failures, earlier failures `191`, `221`, and `238`, and unverified
feature paths. That review did not include fresh Windows Server or Azure Files
results; the later Windows and Azure runs are reported separately above.

## Repository and upstream

The configured origin is [bharathsm-ms/smb-xfstests-dev](https://github.com/bharathsm-ms/smb-xfstests-dev),
branch `cifs-xfstests`. Upstream is
[kdave/xfstests](https://github.com/kdave/xfstests), branch `master`, not `main`.
The recorded September merge `19378166` incorporates upstream `a370dcbe`; backup branch
`backup/cifs-xfstests-pre-kdave-20260917` preserves pre-merge tip `6628667d`.

The merge passed a full build and 327 shell syntax checks in a separate worktree.
The September live follow-up used the original checkout's harness and local
repairs, not the merged harness. Updating a dirty checkout and rerunning against
the merged harness are separate steps; preserve unfinished work before syncing.
Do not infer current remote publication or build status from that historical
merge. Review the current history before choosing a rollback; Git rollback
does not undo server or filesystem changes caused by test runs.

## Prepare the environment

[tools/prepare_env.sh](tools/prepare_env.sh) is a local-only helper for opt-in dependency
installation, helper builds, local Samba setup, profile creation, and preflight
checks. With no action flags, it only checks the current environment:

```bash
sudo -n bash tools/prepare_env.sh --check
bash tools/prepare_env.sh --help
```

**Use a disposable test host and dedicated test/scratch shares. Tests can delete
data, fill filesystems, disrupt networking, and change global CIFS settings.**
For a full local run, mount disposable backing storage at `/srv/samba` before
provisioning; do not use the operating-system filesystem for fill/stress tests.

### Fresh local Samba host

On a Debian/Ubuntu systemd host with working package repositories:

```bash
sudo -n bash tools/prepare_env.sh --all
```

This installs missing client/build/server packages, runs `make` in this checkout,
and creates a non-login `xfstest` account with a randomly generated Samba password.
The root-only credentials file is `/root/.cifs-cred-xfstest`; passwords are not
printed or passed on command lines. Builds run as the invoking user when using
`sudo`. No kernel build or system-wide `make install` is performed.

The two shares, `//127.0.0.1/xfstest` and `//127.0.0.1/xfstest_scratch`, use
`/srv/samba/xfstest` and `/srv/samba/xfstest_scratch`. New Samba configuration
binds only to loopback on port 445 and enables server multichannel support.
The original configuration is backed up, an include is added, `testparm` checks
the candidate, and `smbd` is restarted. A failed restart restores the original
configuration; a partial setup may leave the new account/include for inspection.

Existing test shares, credentials, and profiles are preserved. Provisioning
refuses to take over unrelated Samba accounts/shares, domain configurations, or
nonempty backing directories. It never recursively changes ownership of existing
data. Package installation does not rewrite repository sources or preseed realms;
normal distribution package/service hooks still apply.

The generated [local.config.samba](local.config.samba) uses an `[smb3]` section,
`credentials=`, and separate `/mnt/testshare4` and `/mnt/scratchshare` mountpoints.
Existing profiles are not edited, including when different option values are
supplied on a rerun.

### Existing or remote server

Install/build independently without changing Samba configuration:

```bash
sudo -n bash tools/prepare_env.sh --install --build
```

For a new profile, first prepare a root-owned mode-600 credentials file containing
`username=` and `password=` entries, optionally `domain=`. Enter secrets through
an editor such as `sudoedit`, not shell arguments/history. Then use your dedicated
share names:

```bash
sudo -n bash tools/prepare_env.sh --configure \
  --profile "$PWD/local.config.remote" \
  --credentials /root/.cifs-cred-remote \
  --test-dev //server/test --scratch-dev //server/scratch \
  --test-dir /mnt/cifs-test --scratch-dir /mnt/cifs-scratch
sudo -n bash tools/prepare_env.sh --profile "$PWD/local.config.remote" --probe
```

Omit `--setup-samba` and `--all` for remote or shared servers. On other Linux
distributions, install dependencies from [README](README) plus the CIFS client
tools manually, then use `--build`, `--configure`, and `--probe`.

### Readiness and limits

`--check` validates tools, built `fsx`/`fsstress` helpers, the CIFS module, profile,
credential permissions, mountpoints, and local free space. It does not authenticate
to the server. `--probe` also loads the CIFS module if needed and performs a 4 KiB
write/fsync/read/delete on each share using temporary private-namespace mounts.
The probe is bounded by a 90-second timeout plus a 5-second termination grace.
It does not run the test suite or unmount existing host mounts.

The default minimum is **10 GiB free** on the checkout filesystem and each probed
share. Stress/fill tests can need considerably more, particularly when both
shares share one backing filesystem. `--min-free-gib 1` is an explicit allowance
for small smoke probes, not evidence that the full suite is ready.

Unrelated network mounts are reported without traversing them. Isolate the test
runner from unresponsive mounts before a suite run: harness-wide filesystem scans
can block on them even when the share probe succeeds. The helper does not remove
host mounts or clear firewall rules.

Kerberos realms/keytabs, DFS topology, secondary identities, quotas, snapshots,
and custom kernels are not provisioned. Multichannel still requires suitable
NICs/RSS; directory leasing and compression depend on server/kernel support.
Successful preparation does not guarantee that every feature test will pass or
run; inspect `[not run]` reasons and failures separately.

### Optional test fixtures

| Tests | Requirement |
| --- | --- |
| 106-108, 177, 330, 392 | Multiple usable SMB channels; one interface can suffice with RSS. Enabling server multichannel alone is not enough. |
| 149 | Hostname TEST_DEV, an absolute executable CIFS149_DNS_HOOK with switch/restore operations, and CIFS149_SECOND_IP on a dedicated DNS fixture. |
| 192 | Owned cifsacl or modefromsid mount with mode round-trip support. Fixed modes on the unrelated baseline mount do not require a skip. |
| 232, 275, 345, 355, 385 | Observable directory handle/enumeration reuse or advertised directory leasing, as required by each test. |
| 244, 343 | Linux file leases enabled by the host administrator. Do not change shared NFS/SMB host settings merely to turn a skip into a pass. |
| 306 | Dedicated client with no unrelated SMB connections. The localhost path can reset all port-445 sockets during setup; the remote path installs a server-wide OUTPUT DROP rule. This is not a test-owned-socket-only disruption. |
| 315 | Explicit CIFS_ALLOW_DFS_CACHE_FLUSH=yes; this operation affects the global DFS referral cache. |
| 318, 320 | Short DFS TTL of 1-30 seconds for 318; uniquely identifiable test-owned target socket for 320. |
| 323-333, 404 | Working CIFS_KRB5_REALM/USER/PASS and a dedicated existing non-root CIFS_KRB5_UID for private caches. Test 329 also needs CIFS_KRB5_SECOND_UID; 404 needs a distinct ticket-free CIFS_KRB5_EMPTY_UID. |
| 158, 203, 356 | CIFS_CRED_FILE2 for a distinct server account in the mount account's domain; 203/356 also require a dedicated non-root CIFS_MULTIUSER_UID and private session-keyring support. |
| 377 | Explicit CIFS_ALLOW_MODULE_RELOAD=yes on a dedicated host, with no active CIFS mounts. |
| 387, 397 | Explicit CIFS_ALLOW_SAMBA_RESTART=yes and literal loopback TEST_DEV on a dedicated server; the private fixture uses CIFS_SAMBA_CONTROL to restrict restarts to its owned server. |
| 391 | Dedicated host, explicit restart opt-in, and a continuously available share with persistent handles. This local test restarts the host smbd service directly and is not isolated by CIFS_SAMBA_CONTROL. |
| 378, 379, 402 | Native symlinks, existing server snapshots, or NFS reparse nodes, respectively. Test 379 can use CIFS_SNAPSHOT_DEV. |

These opt-ins are not recommended defaults. Private credential caches do not
authorize resetting passwords or modifying unrelated realms, keytabs, or users.
Some older tests do not gate all global changes behind opt-ins. A private mount
namespace alone does not isolate host network disruption, module parameters,
or cache drops; use a dedicated test VM for broad suite runs.

## How to run CIFS tests

After preparation, [tools/run_cifs_samba.sh](tools/run_cifs_samba.sh) uses
[local.config.samba](local.config.samba), records per-test results, and stops on
a timeout:

```bash
# Single test, then a selected set
sudo -n bash tools/run_cifs_samba.sh cifs/100
sudo -n bash tools/run_cifs_samba.sh cifs/151 cifs/156 cifs/161

# All numbered CIFS tests, including destructive/stress tests
sudo -n bash tools/run_cifs_samba.sh

# Explicit profile, or direct use of the harness
sudo -n env HOST_OPTIONS="$PWD/local.config.remote" bash tools/run_cifs_samba.sh cifs/100
sudo -n env HOST_OPTIONS="$PWD/local.config.samba" ./check -s smb3 -R xunit cifs/100
```

Results default to a new timestamped directory under `results-runs`. Set
`RESULT_BASE` to an unused directory to select another destination. Review xUnit,
`.notrun`, and `.out.bad` files; a zero harness exit status can include skips.
The runner's default per-test timeout is 300 seconds plus a 30-second termination
grace; set `CIFS_REVIEW_TIMEOUT` for an explicitly selected longer workload.
Per-test artifacts are under `<RESULT_BASE>/<NNN>/smb3/cifs/`; the xUnit report is
`<RESULT_BASE>/<NNN>/smb3/result.xml`. Raw logs can contain SMB session keys and
must not be published unredacted.

The preparation and runner scripts are local untracked tools at the review
checkpoint; they are not yet part of the published passing-test series.

## Supported backends

The suite has been tested against the following backends. Results through
**2026-10-08** combine baseline runs and targeted reruns; they are not a single
fresh full-suite run on every backend or a claim that all tests pass.

| Backend | Latest test dates (2026) | Notes |
| --- | --- | --- |
| **Samba 4.22.11** | Oct 6-7 | Local Samba results with feature-specific fixtures; retained failures and skips are documented. |
| **Azure Files** | Oct 3-7 | Combined observations from main, canary, and preproduction endpoints; capabilities depend on the endpoint and share configuration. |
| **Windows Server** | Oct 1-3, 7 | October baseline plus targeted reruns, including repaired tests; retained failures and skips are documented. |
| **ksmbd** | Sep 25, Oct 7-8 | In-tree Linux SMB server; outcomes recorded for all 290 committed test IDs. Multichannel, SMB2 leases, and durable handles were disabled in the tested fixture; missing feature fixtures and disabled opt-ins account for many skips. |

See the [latest cross-server matrix](cifs-results_latest.md),
[failure and skip reasons](cifs-results-failures-20261006.md), and
[run details and source-version limits](cifs-results-20261006.md).

Some tests will skip (`[not run]`) if the backend doesn't support a specific
feature (e.g., compression, directory leases, VSS snapshots). A skip is not a
pass. Missing tools, credentials, or fixture configuration can also prevent a
test from reaching the feature under test. Missing results (`-`) and deliberately
deferred tests are distinct from skips and do not establish compatibility.

## Prerequisites checklist (production/CI)

Use this checklist before trusting CIFS test results for production gating.

### 1) Server and share setup
- SMB server (Samba, Azure Files, Windows, or ksmbd) reachable from test host.
- Dedicated test shares exist (test + scratch), for example:
  - `//<host>/testshare`
  - `//<host>/scratchshare`
- Shares are writable by the test user.
- Optional feature tests require corresponding server support:
  - multichannel, compression, signing, encryption, directory leases.

### 2) Credentials and auth
- Credential file exists and is root-readable only (recommended):
  - `/root/.cifs-cred-xfstest`
  - `chmod 600 /root/.cifs-cred-xfstest`
- The selected profile includes literal `credentials=...` mount options in:
  - `CIFS_MOUNT_OPTIONS`
  - `MOUNT_OPTIONS`
  - `TEST_FS_MOUNT_OPTS`
- For tests that call `mount.cifs` directly, non-interactive auth must be available (no password prompt).

### 3) Host/kernel requirements
- Run tests as root.
- CIFS kernel client and debug interfaces available:
  - `/proc/fs/cifs/DebugData`
  - `/proc/fs/cifs/open_files` (for tests that need it)
- Kernel supports features under test (otherwise expect `[not run]`):
  - multichannel, leases, compression, etc.

### 4) Required tools on test host
- Core tools: `mount.cifs`, `getent`, `awk`, `sed`, `sha256sum`, `md5sum`.
- Reviewed socket-reconnect tests use `ss` to reset a verified test-owned
  connection. Older tests may still require firewall tools and broader isolation.
- Some tests also require: `python3`, a C compiler, `timeout`, and `setsid`.

### 5) Isolation and cleanliness
- Do not reuse production shares.
- Ensure no stale DROP firewall rules before run.
- Use a clean result directory and review:
  - `results/check.log`
  - `results/smb3/cifs/*.full`
  - `results/smb3/cifs/*.out.bad`

## Notes

- Some tests are capability-dependent and may report **[not run]** if kernel/server does not support the feature.
- Some tests intentionally validate invalid options or invalid credentials and expect specific failures.
- Reconnect/fault-injection tests use network disruption and can be environment-sensitive.

## Backend support (Samba, Azure Files, Windows, ksmbd)

This CIFS test suite is intended to work with:

- **Samba shares** (Linux SMB server)
- **Azure Files SMB shares**
- **Windows Server SMB shares**
- **ksmbd shares** (in-kernel Linux SMB server)

### Baseline mount options

```text
-o credentials=/root/.cifs-cred-xfstest,vers=3.1.1
```

This is a minimal SMB3.1.1 example, not a requirement for every test. Add
signing/encryption, cache, multichannel, or symlink/reparse options only as
required by the server and test contract. Fixed `file_mode`/`dir_mode` values
can mask permission semantics; do not impose `0777` as a suite-wide default.
Tests for other dialects or mount options need their own configurations.

### Important compatibility rule

Pass/fail interpretation must use the test's explicit prerequisites and contract:

- A verified missing prerequisite can produce **[not run]** before the tested
  contract is exercised.
- Once a positive control succeeds or support is negotiated, incorrect data,
  metadata, return codes, or recovery remain failures. Do not reclassify a failed
  assertion as unsupported merely to improve the pass count.

### Backend-specific configuration guidance

- Keep backend-specific values in [local.config](local.config):
  - `TEST_DEV`, `SCRATCH_DEV`
  - auth/mount opts via `CIFS_MOUNT_OPTIONS`, `MOUNT_OPTIONS`, `TEST_FS_MOUNT_OPTS`
- Use non-interactive auth (`credentials=...`) for all backends.
- Prefer backend-specific sections/profiles if you run multiple environments in CI.

## Where to debug failures

- Current cross-server results: [cifs-results_latest.md](cifs-results_latest.md).
- Failure and skip explanations: [cifs-results-failures-20261006.md](cifs-results-failures-20261006.md).
- Run provenance and source-version limits: [cifs-results-20261006.md](cifs-results-20261006.md).
- Local runner exit-status ledger: `<RESULT_BASE>/status.tsv`; inspect xUnit and `.notrun` files to distinguish PASS from SKIP.
- Local runner logs and output diffs: `<RESULT_BASE>/<NNN>/smb3/cifs/`; generic tests use `<RESULT_BASE>/generic/<NNN>/smb3/generic/`.
- Raw logs and key-dump output can contain secrets; redact them before sharing.

## Test index

IDs are sparse. This catalogue includes local additions that may not exist in
a committed checkout; use the scripts present in your checkout and its generated
group list for selection. Descriptions summarize test intent, not exhaustive
assertion coverage or passing results. Optional or diagnostic-only subchecks
must not be treated as independently validated features.

### cifs/001
- Legacy CIFS baseline test.

### cifs/100-119 (basic SMB/CIFS functionality)
- **100**: Basic create/read smoke test.
- **101**: `vers=` negotiation across SMB dialects.
- **102**: `sharesock` reuse vs `nosharesock` behavior across shares.
- **103**: Shared-socket versus `nosharesock` visibility in DebugData; the baseline requires no global `nosharesock` option.
- **104**: Per-share Stats counter increments after I/O.
- **105**: DebugData server-interface and channel reporting.
- **106**: SMB3 multichannel activation check.
- **107**: `max_channels=2` behavior with multichannel.
- **108**: `nosharesock + multichannel` across two shares.
- **109**: `mfsymlinks` create/read/traverse behavior.
- **110**: `prefixpath` mount behavior.
- **111**: Hardlink basic semantics.
- **112**: mtime/ctime update semantics.
- **113**: Delete-on-close semantics.
- **114**: Advisory flock semantics.
- **115**: Unicode filename handling.
- **116**: Sparse/punch-hole behavior.
- **117**: Server-side copy (`copy_file_range`) behavior.
- **118**: Signing requested with `-o sign`.
- **119**: SMB3 encryption requested with `-o seal`.

### cifs/120-142 (locks, cache, mount-option semantics)
- **120**: Byte-range lock (`fcntl`) basic behavior.
- **121**: Path component max-length boundary handling.
- **122**: Negotiated capability baseline from Sessions data.
- **123**: `/proc/fs/cifs/open_files` basic compatibility check.
- **124**: Deferred-close behavior visibility.
- **125**: Deferred-close handle reuse behavior.
- **126**: `actimeo` attribute-cache behavior across mounts.
- **127**: Directory lease cache behavior via QueryDirectories counters.
- **128**: `nolease` effect on QueryDirectories frequency.
- **129**: Read-only mount write blocking and write counters.
- **130**: `noperm` client-side permission check behavior.
- **131**: `serverino` inode stability across remount.
- **132**: `noserverino` inode behavior across remount.
- **133**: `actimeo=0` immediate attribute refresh behavior.
- **134**: `bsize=` influence on `statfs` (if supported).
- **135**: `nobrl` effect on lock requests.
- **136**: RO mount blocks chmod/chown/truncate.
- **137**: Signing verification via DebugData.
- **138**: `cache=none` cross-mount read coherency.
- **139**: `nosharesock` creates separate socket/session usage.
- **140**: `mfsymlinks` symlink emulation behavior.
- **141**: `uid/gid` mount-option ownership behavior.
- **142**: `file_mode/dir_mode` behavior for new objects.

### cifs/143-179 (reconnect, stress, lease/multichannel/compression)
- **143**: Reconnect integrity under sustained writes with induced disconnects.
- **144**: Reconnect integrity under sustained reads with induced disconnects.
- **145**: Readdir consistency under disconnect/reconnect.
- **146**: `statfs/df` accounting after data churn.
- **147**: Change notify ioctl event behavior.
- **148**: `acregmax/acdirmax` cache-window behavior.
- **149**: Hostname re-resolve behavior after reconnect.
- **150**: Credit pressure/recovery under metadata stress.
- **151**: `forcedirectio` and cache visibility behavior.
- **152**: Long-path/component error mapping.
- **153**: Credit starvation recovery under stalls.
- **154**: `rsize/wsize/rasize` negotiation behavior.
- **155**: `nodelete` option semantics.
- **156**: Hard vs soft mount behavior during network loss.
- **157**: `strictsync` mount, successful `fsync`, and a share-scoped Flush counter increase.
- **158**: `multiuser` isolation behavior.
- **159**: `nosparse` behavior.
- **160**: `retrans` behavior check.
- **161**: Default auth security type behavior.
- **162**: Multichannel presence (or skip if unsupported).
- **163**: Share/open mode behavior under lock/open patterns.
- **164**: Hardlink count integrity.
- **165**: TCP disconnect mid-I/O integrity.
- **166**: Lease-break storm handling for many files.
- **167**: Directory lease invalidation after remote updates.
- **168**: ENOSPC recovery during append.
- **169**: Encryption cipher/key reporting via `smbinfo` keys.
- **170**: Lease downgrade/break sequence across two mounts.
- **171**: Lease stress with `closetimeo=30`.
- **172**: Lease reclaim behavior after reconnect.
- **173**: Open-downgrade analog with advisory locking.
- **174**: Directory consistency under churn.
- **175**: Multi-address `ip=addr1,addr2` failover behavior.
- **176**: SMB3 compression behavior and stats.
- **177**: SMB3 multichannel failover behavior.
- **178**: Extended attributes round-trip (`setfattr/getfattr`) across two mounts.
- **179**: Persistent/durable handle reconnect validation via `/proc/fs/cifs/open_files`.

### cifs/181-203 (mount helper edge cases, auth, reconnect-hardening)
- **181**: Mount option-length overflow handling.
- **182**: UNC parser/validation error paths.
- **183**: Byte-range lock robustness after reconnect.
- **184**: Sequential-write integrity across reconnect.
- **185**: `sloppy` unknown-option handling.
- **186**: `cache=strict` vs `cache=none` coherency comparison.
- **187**: `max_credits=4` pressure behavior.
- **188**: Lock persistence across repeated reconnects.
- **189**: Guest vs `sec=none` behavior.
- **190**: Open-file leak checks across close/unmount cycles.
- **191**: Multichannel throughput comparison baseline.
- **192**: Read/dir/metadata resilience across reconnect.
- **193**: `mount.cifs` username/domain length handling.
- **194**: `mount.cifs` password length handling.
- **195**: RO/RW remount transition enforcement.
- **196**: `exec/noexec` transition enforcement.
- **197**: `nosuid` behavior for setuid binaries.
- **198**: Random packet-loss tolerance during sustained I/O.
- **199**: Credential-source precedence (`credentials=`, `PASSWD`, `PASSWD_FD`, `PASSWD2`).
- **200**: Space accounting predictability (`statvfs/df`).
- **201**: Open/close stress with constrained `max_credits`.
- **202**: Concurrent lock/open-close latency boundedness.
- **203**: `cifscreds` + `multiuser` credential fallback behavior.

### cifs/206-207 (xattr, persistent handles)
- **206**: Extended attributes round-trip and cross-mount visibility.
- **207**: Persistent/durable handle survives reconnect.

### cifs/208-217 (POSIX I/O semantics)
- **208**: `truncate`/`ftruncate` — grow, shrink, zero-length, data preservation.
- **209**: `mmap` — MAP_SHARED write, MAP_PRIVATE read, msync persistence.
- **210**: `rename` — same-dir, cross-dir, atomic replace, dir rename, ENOTEMPTY.
- **211**: `pread`/`pwrite` — positional I/O, file position preservation, concurrent.
- **212**: Open flags — `O_CREAT|O_EXCL`, `O_TRUNC`, `O_APPEND` semantics.
- **213**: `fdatasync` — persistence, repeated sync, comparison with `fsync`.
- **214**: `lseek` — SEEK_SET/CUR/END, past-EOF gap, optional SEEK_HOLE/SEEK_DATA.
- **215**: Large files — >2 GiB and >4 GiB boundary correctness.
- **216**: Readdir stress — 500 files, concurrent deletion, special names, empty dir.
- **217**: `stat`/`fstat` — size, nlink, ino stability, blocks, fstat==stat.

### cifs/218-223 (POSIX permissions / mount extensions)
- **218**: `chmod`/`chown`/`chgrp` with unix/modefromsid extensions.
- **219**: `forceuid`/`forcegid` vs `noforceuid`/`noforcegid` behavior.
- **220**: POSIX ACLs via `cifsacl` — setfacl/getfacl round-trip, default ACLs.
- **221**: `modefromsid` — mode bits persist in SID across remount.
- **222**: Special files — symlink, mkfifo, readlink via reparse points.
- **223**: Umask interaction with POSIX extensions.

### cifs/224-234 (sparse, fallocate, reparse, dir cache, encryption, VSS)
- **224**: `SEEK_DATA`/`SEEK_HOLE` correctness with sparse files.
- **225**: WSL reparse special files (reparse=wsl).
- **226**: `fallocate` FALLOC_FL_ZERO_RANGE correctness.
- **227**: `fiemap` (FSCTL_QUERY_ALLOCATED_RANGES).
- **228**: Cached directory handle validation — reuse reduces Creates.
- **229**: NFS reparse mknod (block, char, FIFO, socket).
- **230**: AES-256-GCM encryption negotiation and I/O validation.
- **231**: `max_cached_dirs` / `dir_cache_timeout` tuning.
- **232**: `nohandlecache` — every readdir causes fresh Open.
- **233**: `fallocate` collapse-range and insert-range.
- **234**: VSS snapshot enumeration (FSCTL_SRV_ENUMERATE_SNAPSHOTS).

### cifs/235-244 (I/O, caching, ioctls, and controls)
- **235**: Splice/sendfile — zero-copy I/O paths, data integrity.
- **236**: FS-Cache registration, `-o fsc` mounting, and reread/coherency checks; these do not prove data was served from the local disk cache.
- **237**: Ioctls — `CIFS_QUERY_INFO`, `FS_IOC_GETFLAGS/SETFLAGS` (chattr).
- **238**: Inotify/fsnotify — `inotify_add_watch` event delivery on CIFS.
- **239**: SMB2 error mapping — EEXIST, ENOENT, EISDIR, ENOTDIR, ENOTEMPTY, ENAMETOOLONG.
- **240**: Swap-over-SMB — `swapon`/`swapoff` on CIFS file.
- **241**: Mount option parsing batch 1 — echo_interval, handletimeout, tcp_nodelay, noac, srcaddr.
- **242**: Mount option parsing batch 2 — iocharset, backupuid/gid, resilienthandles, dynperm, locallease.
- **243**: Filesystem freeze/thaw — `fsfreeze -f/-u`, write blocking during freeze.
- **244**: `F_SETLEASE` — kernel file leases, read/write lease, lease release.

### cifs/245-260 (I/O, ACLs, metadata, and concurrency)
- **245**: `O_DIRECT` individual file opens — direct write+read, mixed direct/buffered.
- **246**: Windows ACL ↔ POSIX mode mapping via `cifsacl`.
- **247**: Reparse edge cases — symlink chains, dir symlinks, dangling, rename, native sockets.
- **248**: SMB3 compression data integrity — compressible, random, large.
- **249**: Writeback/readahead stress — sequential, random, concurrent, dirty overwrite, small writes.
- **250**: cifsacl deep — all 12 permission bits, persistence across remount, zero-mode round-trip.
- **251**: cifsacl owner/group SID exercises, descriptor queries, and idsfromsid creation/stat checks; some ownership and descriptor checks are diagnostic only.
- **252**: Reparse mknod deep — FIFO, char/block dev, socket via reparse, stat file types.
- **253**: Reparse WSL vs NFS — symlink modes, directory detection, multi-component, parent traversal.
- **254**: Xattr deep — listxattr, removexattr, binary values, dir xattr, size limits.
- **255**: Hardlink edge cases — cross-dir, nlink>2, unlink-while-open, write-through-link.
- **256**: Huge readdir — 10K files, concurrent readdir+delete, varied name patterns.
- **257**: Inode setattr combo — size+mode+mtime, statx refresh, rapid size oscillation.
- **258**: Remount transitions — ro/rw, actimeo change, closetimeo change, rapid remounts.
- **259**: Concurrent open stress — 200 sequential, 100 simultaneous fds, 16-thread parallel, rapid reopen.
- **260**: Sharing violation / lock conflicts — flock EAGAIN, byte-range lock conflict, non-overlapping OK.

### cifs/261-272 (lease break, IOCTLs, ADS, quota, keys)
- **261**: Lease break mid-I/O — write integrity during lease break, concurrent dual writes, rapid storm.
- **262**: `CIFS_IOC_SET_INTEGRITY` — FSCTL_SET_INTEGRITY_INFORMATION.
- **263**: `CIFS_IOC_GET_MNT_INFO` / `CIFS_IOC_GET_TCON_INFO` diagnostic ioctls.
- **264**: `FSCTL_DUPLICATE_EXTENTS_TO_FILE` — FICLONE/FICLONERANGE server-side clone.
- **265**: `CIFS_IOC_SHUTDOWN` — graceful filesystem shutdown ioctl.
- **266**: Cross-mount cache coherency — write on A, read on B, size/mtime propagation.
- **267**: Unicode/i18n filename stress — CJK, emoji, Cyrillic, Arabic, combining chars.
- **268**: File locking stress — 200 locks, upgrade/downgrade, split, fork, flock cycles.
- **269**: SMB2_write encryption page cache corruption — O_WRONLY mid-file + socket kill.
- **270**: smbinfo comprehensive — all 14 CIFS_QUERY_INFO subcommands on file and dir.
- **271**: NTFS alternate data streams — write/read `:stream`, multiple streams, large ADS.
- **272**: SMB2 quota query + CIFS_DUMP_KEY / CIFS_DUMP_FULL_KEY ioctls.

### cifs/273-274 (data/metadata corruption corner cases)
- **273**: Truncate+write race, truncate-to-zero while reading, extend+stat consistency, O_WRONLY partial page write, write+fsync+rename atomicity.
- **274**: mmap/truncate and zero-fill checks, concurrent mmap reads/writes, optional punch-hole diagnostics, and fsync/cache-drop/reread. The final reread does not compare against pre-drop contents; this is not a power-loss or crash-durability test.

### cifs/275-278 (SMB performance tests)
- **275**: Directory lease performance — rsync with/without dir leases, QueryDirs comparison.
- **276**: Deferred close performance — closetimeo=30 vs closetimeo=0, Creates/Closes saved.
- **277**: Cache mode throughput — cache=strict vs cache=none repeated read throughput.
- **278**: copy_file_range vs cp vs dd — server-side COPYCHUNK vs network data transfer.

### cifs/279-285 (bug regression tests)
- **279**: Beyond-EOF DIO read (commit 4ae4dde6f34a) — short read past EOF, not error.
- **280**: Writeback boundary corruption (commits f3dc1bdb6b0b, 4860abb91f3d) — wsize boundary page skip, various chunk sizes.
- **281**: Reparse hardlink/rename (commits 5408990aa662, 7435d51b7ea2) — hardlink/rename symlinks with OPEN_REPARSE_POINT.
- **282**: O_WRONLY + fscache (commit e9e62243a3e2) — partial write caching, mid-file write, cache drop coherency.
- **283**: Rename of open file (commits c5ea3065586d, d84291fc7453) — data loss prevention, concurrent open+rename race.
- **284**: Concurrent unlink race (commit 0af1561b2d60) — stale dentry detection, concurrent open+unlink.
- **285**: Read-after-invalidate corruption (commit a395726cf823) + fallocate+DIO race (commit dba9f997c9d9) + actimeo/closetimeo integer overflow.

### cifs/286-289 (data integrity and module parameters)
- **286**: rsize/wsize data integrity — 9 configurations × 5 I/O patterns (cp, dd, small→large, pwrite, append).
- **287**: `enable_oplocks` toggle — disable oplocks, verify increased server Reads, data integrity, restore.
- **288**: `disable_legacy_dialects` — block vers=1.0, allow SMB2+, toggle and verify.
- **289**: `drop_dir_cache` — force cached dir invalidation, open_dirs verification, rapid drops, new file visibility.

### cifs/290-301 (negative tests, connectathon equivalents, error paths)
- **290**: Kerberos `sec=krb5` negative path — mount without valid ticket fails cleanly, no crash/hang.
- **291**: Negative lookup — `stat`/`open`/`readlink`/`unlink`/`rmdir`/`rename` on non-existent paths return ENOENT.
- **292**: `fcntl F_SETLKW` blocking lock — exclusive lock blocks waiter, waiter proceeds after release.
- **293**: Lock release on close — closing fd releases all held POSIX locks (even with other fds open).
- **294**: Wrong password → clean mount failure (EACCES/EPERM), no crash or hang.
- **295**: Non-existent share → clean mount failure (BAD_NETWORK_NAME), no crash or hang.
- **296**: `rmdir` non-empty → ENOTEMPTY, double `unlink` → ENOENT, double `mkdir` → EEXIST.
- **297**: Symlink loop (`a→b→a`) → ELOOP on stat, no hang or crash.
- **298**: Invalid `vers=` mount option → clean rejection, no kernel oops.
- **299**: I/O on invalid fd modes — read from O_WRONLY → EBADF, write to O_RDONLY → EBADF.
- **300**: Write beyond max offset ($2^{63}-2$) → EFBIG/EINVAL, no crash; negative lseek → EINVAL.
- **301**: Hardlink across different mounts → EXDEV; hardlink to non-existent source → ENOENT.

### cifs/302-312 (stress tests)
- **302**: Interrupted close with SIGTERM, SIGKILL, and 50 rapid kill cycles; bounded `stat`/`rm` checks test forward progress, not server-side handle-leak accounting.
- **303**: Git workload — `git init`/`add`/`commit`/`branch`/`checkout`/`merge`/`diff` on CIFS share, data integrity verification.
- **304**: nosharesock mount stress — progressive 10→50→100 mount scaling, I/O on each, leak check after unmount.
- **305**: 1000-process concurrent write/read — 1000 separate files + 1000 writers to same file at unique offsets, data verification.
- **306**: Reconnect workload attempting 100 open files, using firewall drops or socket resets, followed by read and checksum checks. It does not assert that all handles opened or that persistent handles were negotiated; disruption can affect unrelated SMB connections.
- **307**: 500-file lease break flood — 2 nosharesock mounts, open 500 files on mount A, touch all from mount B, verify integrity.
- **308**: readdir + drop_dir_cache race — concurrent `ls -R` loop + `drop_dir_cache` writes, verify no crash or corruption.
- **310**: Ten-mount concurrent writes and directory creation, exact cross-mount byte checks, cleanup, and an `OplockBreaks` counter-increase assertion. The counter assertion does not establish that a lease/oplock grant required a break.
- **311**: Deferred close overflow — 3 rounds × 5000 rapid open/close with closetimeo=30, verify no resource exhaustion, data integrity, handle leaks, dmesg warnings.
- **312**: Rapid mount/unmount stress — 100 parallel processes each mount/write/unmount + 50 sequential cycles, session/tcon leak detection, handle leak check.

### cifs/313-407 (extended SMB feature tests)

The index below describes intended test behavior, not a passing result or
proof that every related kernel path was exercised. Some entries are local
additions and may not be present in a committed checkout. See the
[latest cross-server matrix](cifs-results_latest.md),
[failure and skip reasons](cifs-results-failures-20261006.md), and
[run details](cifs-results-20261006.md) for observed outcomes and validation limits.

| IDs | Coverage |
| --- | --- |
| 313-322, 396 | DFS traversal, referrals, cache lifecycle, TTL, read-only behavior, and reconnect/remount checks. |
| 323-333, 404 | Kerberos authentication with private credential caches, signing/encryption, ticket removal, multiuser access, reconnect, DFS, and `cruid` selection. |
| 334, 337-340, 361-362, 381 | CIFS proc controls, restoration, counters, and checked I/O. |
| 335, 341, 360, 380, 395 | SID interpretation, `cifsacl` mode round trips, security-descriptor xattrs, and semantic DACL copying. |
| 336, 342, 371, 386, 399 | Negotiation and mount-information ioctls, ABI/error handling, and bounded key-buffer checks. |
| 343, 349, 352, 354, 358-359, 394 | File leases, byte-range locks, lock recovery, oplock breaks, and close/reopen handle lifecycle. |
| 344, 346, 350, 357, 363, 372, 375, 398 | Direct, buffered, vectored, and large I/O; fallocate modes; cache-mode behavior; and data integrity. |
| 345, 355, 373, 385 | Directory caching, lease-break invalidation, and fresh metadata queries with attribute caching and leases disabled. |
| 347 | Native CIFS notify ioctl event delivery and cancellation. |
| 348, 370, 374, 384, 388 | Directory enumeration, concurrent file operations, case-insensitive lookup, metadata, symlinks, and hardlink lifecycle. |
| 351, 382, 401 | Extended attributes, DOS metadata, and exact negative-operation errors. |
| 353, 378, 383, 402 | SFU nodes, native/MF symlinks, and NFS reparse nodes. |
| 356 | Private cifscreds keyring lifecycle and multiuser I/O. |
| 364, 376, 393 | Encrypted I/O and negotiated dialect, signing, and encryption controls. |
| 365-369, 400 | Invalid mount options, shares, credentials, file descriptors, permissions, and path-length boundaries; mount failures are checked against positive controls. |
| 377 | CIFS module load/unload lifecycle on an explicitly opted-in, dedicated host. |
| 379 | Server snapshot enumeration with validated UTF-16 labels. |
| 387, 391, 397 | Samba restart and interrupted-I/O recovery; persistent-handle recovery requires a continuously available share. |
| 389 | Transport workloads with credit, signing, and encryption checks. |
| 390 | Negotiated SMB3.1.1 POSIX extensions and filesystem semantics. |
| 392, 405 | Multichannel limits, independent connections, and live channel resizing while preserving open-file I/O. |
| 403 | SMB3 negotiation, file I/O, and metadata lifecycle over port 139. |
| 406 | Decryption-offload checks and negative controls using private tracing. |
| 407 | Server filesystem compression behavior, distinct from SMB wire compression. |

Module reload and server-restart tests are disruptive and require explicit
opt-in on an isolated test host. Feature-specific tests also depend on the
required server capabilities, tools, and credentials; skips and missing results
are not passes.
