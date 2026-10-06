# CIFS xfstests README

This document describes the CIFS/SMB client test suite for xfstests.

**Working-tree inventory on 2026-10-06: 305 numbered tests**, including
290 committed scripts and 15 untracked additions. IDs are sparse, through
`cifs/407`; a committed checkout does not contain every local addition.

## Commit status (2026-10-06)

The following **19 test changes were reviewed as good to commit and committed
locally in `028c3dc6`**. That commit has not been pushed. Each selected script
and expected output matches an archived passing Samba attempt; this is not
an all-server compatibility claim.

| Status | Count | Test IDs (`cifs/` prefix omitted) |
| --- | ---: | --- |
| Committed repairs | 5 | 149, 158, 203, 215, 244 |
| Committed additions | 14 | 323, 324, 326, 327, 328, 329, 330, 331, 333, 356, 379, 387, 404, 406 |
| Good to commit, still pending | 0 | None of the remaining reviewed changes is currently cleared. |
| Held repairs to already committed tests | 5 | 192, 194, 225, 236, 275 |
| Held untracked additions | 15 | 318, 325, 343, 345, 349, 360, 377, 378, 385, 391, 395, 397, 401, 402, 405 |

The 20 held changes need further fixes, fixture validation, failure attribution
or duplicate-test consolidation. A committed test can still have an uncommitted
repair on hold; committed status alone does not certify the current working
copy. Previously committed tests are not newly approved by this list.

See [the commit selection and cross-server results](cifs-results-20261006.md)
for per-test behavior, hold reasons, fixture requirements and source-version
limits. The complete runnable inventory remains in
[tests/cifs/group.list](tests/cifs/group.list); its working-tree version also
includes the held local additions. Historical checksummed attempt lists under
`coverage/` remain unchanged and record executions, not commit readiness.

The suite covers:
- POSIX I/O semantics, permissions, ACLs, xattr, locking
- 45+ mount options, module parameters, remount transitions
- Reconnect/resilience, lease/oplock handling, credit management
- Selected userspace-accessible IOCTLs and FSCTLs
- SMB3 encryption, compression, multichannel, deferred close
- Data corruption corner cases and 10+ bug regression tests
- Performance benchmarks (dir leases, caching, copy_file_range, deferred close)
- Unicode/i18n, large files, concurrent stress, rsize/wsize sweep
- NTFS alternate data streams, quota, key dump
- Kernel module parameter validation (enable_oplocks, disable_legacy_dialects, drop_dir_cache)
- Negative/error-path tests (bad credentials, invalid options, ELOOP, EXDEV, EBADF)
- Stress tests (git workload, multi-mount consistency, lease flood, reconnect, writeback races)

## How to run CIFS tests

- Configure [local.config](local.config) with CIFS test share details.
- Run as root:
  ```bash
  # Single test
  sudo ./check cifs/100

  # Range of tests
  sudo ./check cifs/{208..310}

  # Stress tests only
  sudo ./check -g stress

  # All CIFS tests
  sudo ./check $(ls tests/cifs/ | grep -E '^[0-9]+$' | sort -n | sed 's/^/cifs\//')
  ```

## Supported backends

| Backend | Status | Notes |
|---|---|---|
| **Samba** | ✅ Tested | Local or remote Samba server |
| **Windows Server** | ✅ Tested | SMB3.1.1, multichannel |
| **Azure Files** | ✅ Compatible | Premium/Standard SMB shares |

Some tests will skip (`[not run]`) if the backend doesn't support a specific
feature (e.g., compression, directory leases, VSS snapshots). This is expected
behavior — the tests are capability-aware.

## Prerequisites checklist (production/CI)

Use this checklist before trusting CIFS test results for production gating.

### 1) Server and share setup
- SMB server (Samba, Windows, or Azure Files) reachable from test host.
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
- [local.config](local.config) includes `credentials=...` in:
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
- For fault-injection/reconnect tests: `iptables` (preferred) and/or `ss`.
- Some tests also require: `python3`, `gcc`.

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

## Backend support (Samba, Windows, Azure Files)

This CIFS test suite is intended to work with:

- **Samba shares** (Linux SMB server)
- **Windows Server SMB shares**
- **Azure Files SMB shares**

### Recommended mount options

```
-o credentials=/root/.cifs-cred-xfstest,vers=3.1.1,dir_mode=0777,file_mode=0777,serverino,actimeo=1,mfsymlinks,reparse=nfs
```

### Important compatibility rule

Pass/fail interpretation must be **capability-based**:

- If a backend does not implement a feature (example: specific lease, multichannel, compression, signing/encryption mode, helper option), tests should be treated as **[not run]** where applicable.
- Tests should only be treated as hard failures when the backend advertises/supposedly supports the feature but behavior is incorrect.

### Backend-specific configuration guidance

- Keep backend-specific values in [local.config](local.config):
  - `TEST_DEV`, `SCRATCH_DEV`
  - auth/mount opts via `CIFS_MOUNT_OPTIONS`, `MOUNT_OPTIONS`, `TEST_FS_MOUNT_OPTS`
- Use non-interactive auth (`credentials=...`) for all backends.
- Prefer backend-specific sections/profiles if you run multiple environments in CI.

## Test index

### cifs/001
- Legacy CIFS baseline test.

### cifs/100-119 (basic SMB/CIFS functionality)
- **100**: Basic create/read smoke test.
- **101**: `vers=` negotiation across SMB dialects.
- **102**: `sharesock` reuse vs `nosharesock` behavior across shares.
- **103**: `nosharesock` visibility in DebugData.
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
- **157**: `strictsync` flush behavior.
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

## Where to debug failures

- Result summary: `results/check.log`
- Per-test full logs: `results/smb3/cifs/<test>.full`
- Output diffs: `results/smb3/cifs/<test>.out.bad`
- Test results report: [cifs-results.md](cifs-results.md)

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

### cifs/235-244 (kernel code gap coverage)
- **235**: Splice/sendfile — zero-copy I/O paths, data integrity.
- **236**: FS-Cache — `-o fsc` local disk caching, coherency.
- **237**: Ioctls — `CIFS_QUERY_INFO`, `FS_IOC_GETFLAGS/SETFLAGS` (chattr).
- **238**: Inotify/fsnotify — `inotify_add_watch` event delivery on CIFS.
- **239**: SMB2 error mapping — EEXIST, ENOENT, EISDIR, ENOTDIR, ENOTEMPTY, ENAMETOOLONG.
- **240**: Swap-over-SMB — `swapon`/`swapoff` on CIFS file.
- **241**: Mount option parsing batch 1 — echo_interval, handletimeout, tcp_nodelay, noac, srcaddr.
- **242**: Mount option parsing batch 2 — iocharset, backupuid/gid, resilienthandles, dynperm, locallease.
- **243**: Filesystem freeze/thaw — `fsfreeze -f/-u`, write blocking during freeze.
- **244**: `F_SETLEASE` — kernel file leases, read/write lease, lease release.

### cifs/245-260 (deep kernel coverage)
- **245**: `O_DIRECT` individual file opens — direct write+read, mixed direct/buffered.
- **246**: Windows ACL ↔ POSIX mode mapping via `cifsacl`.
- **247**: Reparse edge cases — symlink chains, dir symlinks, dangling, rename, native sockets.
- **248**: SMB3 compression data integrity — compressible, random, large.
- **249**: Writeback/readahead stress — sequential, random, concurrent, dirty overwrite, small writes.
- **250**: cifsacl deep — all 12 permission bits, persistence across remount, zero-mode round-trip.
- **251**: cifsacl owner/group SID — chown/chgrp, security descriptor query, idsfromsid.
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
- **274**: mmap+truncate below, truncate-extend zero fill, concurrent mmap write+read, fallocate punch+concurrent read, power-loss simulation.

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

### cifs/302-310 (stress tests)
- **302**: Interrupted close — kill process with open file handle, verify no server-side handle leak (stat/rm don’t hang). SIGTERM, SIGKILL, 50 rapid kill cycles.
- **303**: Git workload — `git init`/`add`/`commit`/`branch`/`checkout`/`merge`/`diff` on CIFS share, data integrity verification.
- **304**: nosharesock mount stress — progressive 10→50→100 mount scaling, I/O on each, leak check after unmount.
- **305**: 1000-process concurrent write/read — 1000 separate files + 1000 writers to same file at unique offsets, data verification.
- **306**: Reconnect with 100 open files — open 100 files, iptables DROP 5s, restore, verify all data via persistent handles.
- **307**: 500-file lease break flood — 2 nosharesock mounts, open 500 files on mount A, touch all from mount B, verify integrity.
- **308**: readdir + drop_dir_cache race — concurrent `ls -R` loop + `drop_dir_cache` writes, verify no crash or corruption.
- **310**: Multi-mount consistency — 10 nosharesock mounts × 10 parallel processes: shared file writes at unique offsets, shared directory creates, cross-mount read verification, lease break confirmation, handle leak check.
- **311**: Deferred close overflow — 3 rounds × 5000 rapid open/close with closetimeo=30, verify no resource exhaustion, data integrity, handle leaks, dmesg warnings.
- **312**: Rapid mount/unmount stress — 100 parallel processes each mount/write/unmount + 50 sequential cycles, session/tcon leak detection, handle leak check.

### cifs/313-407 (additional reviewed tests)

This range contains both committed tests and held local additions. See the
commit-status list above for the selected and held IDs, and the
[dated result page](cifs-results-20261006.md) for outcomes and validation limits.
The index below is a feature map, not a pass or commit-readiness claim.

| IDs | Coverage |
| --- | --- |
| 313-322, 396 | DFS traversal, referrals, cache lifecycle, TTL, read-only behavior, and reconnect/remount checks. |
| 323-333, 404 | Private Kerberos authentication, signing/encryption, ticket removal, multiuser, reconnect, DFS, and credential-UID selection. |
| 334, 337-340, 361-362, 381 | CIFS proc controls, restoration, counters, and checked I/O. |
| 335, 360, 380, 395 | SID interpretation, cifsacl mode round trips, and semantic DACL copying. |
| 336, 342, 371, 386, 399 | Negotiation and ioctl ABI, error handling, and bounded key-buffer checks. |
| 341, 344, 346, 348, 350, 357, 363-364, 367-370, 372-376, 388-389, 393, 398, 403 | File and directory operations, data integrity, mount options, and concurrent workloads. |
| 343, 345, 349, 352, 354-355, 358-359, 384-385, 394 | File locks, leases, directory caching, handle lifecycle, and nocase directory behavior. |
| 347 | Native CIFS notify ioctl event delivery and cancellation. |
| 351, 382, 401 | Extended attributes, DOS metadata, and exact negative-operation errors. |
| 353, 378, 383, 402 | SFU nodes, native/MF symlinks, and NFS reparse nodes. |
| 356 | Private cifscreds keyring lifecycle and multiuser I/O. |
| 365-366, 400 | Mount-option, share-name, and credential negative controls with positive controls. |
| 377, 387, 391, 397 | Explicitly opted-in module reload or Samba restart tests; persistent-handle recovery requires CA support. |
| 379 | Server snapshot enumeration with validated UTF-16 labels. |
| 390, 392 | Negotiated SMB3 POSIX semantics and multichannel limits. |
| 405 | Live multichannel resizing with open-file I/O; held local addition. |
| 406 | Verified decryption offload and negative controls using private tracing; committed in 028c3dc6. |
| 407 | Server filesystem compression behavior, not SMB wire compression; previously committed. |
