# CIFS xfstests — Test Results

**Generated**: 2026-03-06

This is an archived cross-backend report. See the
[latest results page](cifs-results_latest.md) and the
[2026-10-06 cross-server matrix](cifs-results-20261006.md) for dated Samba,
Windows, Azure Files and ksmbd outcomes, source-version limits and commit
selection. The March tables below remain historical; do not combine them
with the later runs.

## Summary

| Result | Samba | Windows Server | Azure Files |
|---|---|---|---|
| ✅ Passed | **164** | **158** | **139** |
| ⏭️ Skipped | **39** | **35** | **46** |
| ❌ Failed | **4** | **7** | **15** |
| **Total** | **207** | **200** | **200** |

## Environment

| Parameter | Samba | Windows Server | Azure Files |
|---|---|---|---|
| **Client Kernel** | 6.19.0-rc1+ | 6.19.0-rc1+ | 6.19.0-rc1+ |
| **Server** | Samba 4.21.4 (localhost) | Windows Server | Azure Files Premium |
| **Protocol** | SMB3 (auto) | SMB 3.1.1 | SMB 3.1.1 |
| **Multichannel** | No (single NIC) | Yes (3 channels) | Yes (multichannel) |

## Detailed Results

| Test | Samba | Windows | Azure Files |
|---|---|---|---|
| cifs/001 | — | ✅ 2s | ❌ |
| cifs/100 | ✅ 2s | ✅ 2s | ✅ 2s |
| cifs/101 | ✅ 2s | ✅ 2s | ✅ 7s |
| cifs/102 | ✅ 2s | ✅ 2s | ✅ 8s |
| cifs/103 | ✅ 2s | ✅ 2s | ✅ 5s |
| cifs/104 | ⏭️ | ⏭️ | ✅ 5s |
| cifs/105 | ✅ 2s | ✅ 2s | ✅ 3s |
| cifs/106 | ✅ 1s | ✅ 2s | ✅ 4s |
| cifs/107 | ⏭️ | ✅ 2s | ✅ 4s |
| cifs/108 | ✅ 2s | ✅ 3s | ✅ 6s |
| cifs/109 | ✅ 1s | ✅ 2s | ✅ 4s |
| cifs/110 | ⏭️ | ⏭️ | ⏭️ |
| cifs/111 | ⏭️ | ⏭️ | ⏭️ |
| cifs/112 | ✅ 2s | ✅ 2s | ✅ 5s |
| cifs/113 | ✅ 1s | ✅ 2s | ✅ 3s |
| cifs/114 | ✅ 1s | ✅ 2s | ✅ 3s |
| cifs/115 | ✅ 2s | ✅ 1s | ✅ 4s |
| cifs/116 | ✅ 1s | ✅ 1s | ❌ |
| cifs/117 | ✅ 2s | ✅ 2s | ✅ 4s |
| cifs/118 | ⏭️ | ⏭️ | ⏭️ |
| cifs/119 | ✅ 2s | ✅ 1s | ✅ 3s |
| cifs/120 | ✅ 2s | ✅ 3s | ❌ |
| cifs/121 | ✅ 2s | ✅ 1s | ✅ 3s |
| cifs/122 | ✅ 1s | ✅ 2s | ✅ 6s |
| cifs/123 | ✅ 2s | ✅ 2s | ✅ 3s |
| cifs/124 | ✅ 34s | ✅ 33s | ✅ 35s |
| cifs/125 | ✅ 16s | ✅ 16s | ✅ 20s |
| cifs/126 | ✅ 13s | ✅ 12s | ❌ |
| cifs/127 | ✅ 34s | ✅ 34s | ❌ |
| cifs/128 | ✅ 1s | ✅ 1s | ❌ |
| cifs/129 | ✅ 3s | ✅ 3s | ✅ 5s |
| cifs/130 | ✅ 3s | ✅ 3s | ✅ 5s |
| cifs/131 | ✅ 2s | ✅ 1s | ✅ 4s |
| cifs/132 | ✅ 1s | ✅ 3s | ✅ 4s |
| cifs/133 | ✅ 2s | ✅ 2s | ✅ 5s |
| cifs/134 | ⏭️ | ⏭️ | ⏭️ |
| cifs/135 | ✅ 2s | ✅ 2s | ✅ 4s |
| cifs/136 | ✅ 2s | ✅ 1s | ✅ 4s |
| cifs/137 | ⏭️ | ⏭️ | ⏭️ |
| cifs/138 | ✅ 1s | ✅ 2s | ✅ 5s |
| cifs/139 | ✅ 1s | ✅ 2s | ✅ 4s |
| cifs/140 | ✅ 2s | ✅ 1s | ✅ 3s |
| cifs/141 | ✅ 1s | ✅ 1s | ✅ 3s |
| cifs/142 | ✅ 2s | ✅ 2s | ✅ 4s |
| cifs/143 | ✅ 20s | ✅ 19s | ✅ 26s |
| cifs/144 | ✅ 20s | ✅ 19s | ✅ 25s |
| cifs/145 | ✅ 13s | ✅ 10s | ✅ 91s |
| cifs/146 | ✅ 2s | ✅ 2s | ✅ 12s |
| cifs/147 | ✅ 3s | ✅ 3s | ✅ 4s |
| cifs/148 | ✅ 13s | ✅ 13s | ✅ 18s |
| cifs/149 | ⏭️ | ⏭️ | ⏭️ |
| cifs/150 | ✅ 53s | ✅ 56s | ✅ 65s |
| cifs/151 | ⏭️ | ⏭️ | ⏭️ |
| cifs/152 | ✅ 3s | ✅ 2s | ❌ |
| cifs/153 | ✅ 9s | ✅ 10s | ✅ 26s |
| cifs/154 | ✅ 1s | ✅ 1s | ⏭️ |
| cifs/155 | ✅ 2s | ✅ 2s | ✅ 4s |
| cifs/156 | ⏭️ | ⏭️ | ⏭️ |
| cifs/157 | ✅ 1s | ✅ 2s | ⏭️ |
| cifs/158 | ⏭️ | ⏭️ | ⏭️ |
| cifs/159 | ✅ 2s | ✅ 1s | ⏭️ |
| cifs/160 | ✅ 2s | ✅ 2s | ✅ 3s |
| cifs/161 | ✅ 1s | ✅ 1s | ✅ 2s |
| cifs/162 | ✅ 7s | ✅ 8s | ✅ 9s |
| cifs/163 | ⏭️ | ⏭️ | ⏭️ |
| cifs/164 | ✅ 1s | ✅ 1s | ❌ |
| cifs/165 | ✅ 8s | ❌ | ✅ 22s |
| cifs/166 | ✅ 15s | ✅ 15s | ✅ 238s |
| cifs/167 | ⏭️ | ✅ 2s | ⏭️ |
| cifs/168 | ⏭️ | ⏭️ | ⏭️ |
| cifs/169 | ✅ 2s | ✅ 1s | ✅ 4s |
| cifs/170 | ⏭️ | ⏭️ | ⏭️ |
| cifs/171 | ✅ 17s | ✅ 17s | ✅ 28s |
| cifs/172 | ⏭️ | ⏭️ | ⏭️ |
| cifs/173 | ✅ 2s | ✅ 1s | ✅ 2s |
| cifs/174 | ✅ 22s | ✅ 15s | ✅ 375s |
| cifs/175 | ⏭️ | ⏭️ | ⏭️ |
| cifs/176 | ⏭️ | ⏭️ | ⏭️ |
| cifs/177 | ⏭️ | ⏭️ | ⏭️ |
| cifs/178 | ✅ 2s | ⏭️ | ❌ |
| cifs/179 | ⏭️ | ⏭️ | ⏭️ |
| cifs/181 | ⏭️ | ⏭️ | ⏭️ |
| cifs/182 | ✅ 2s | ✅ 1s | ✅ 1s |
| cifs/183 | ✅ 8s | ✅ 8s | ✅ 9s |
| cifs/184 | ✅ 11s | ✅ 10s | ✅ 30s |
| cifs/185 | ⏭️ | ⏭️ | ⏭️ |
| cifs/186 | ✅ 2s | ✅ 1s | ✅ 4s |
| cifs/187 | ✅ 3s | ✅ 7s | ✅ 72s |
| cifs/188 | ✅ 12s | ✅ 12s | ✅ 14s |
| cifs/189 | ⏭️ | ⏭️ | ⏭️ |
| cifs/190 | ✅ 3s | ✅ 3s | ✅ 21s |
| cifs/191 | ⏭️ | ⏭️ | ⏭️ |
| cifs/192 | ⏭️ | ⏭️ | ⏭️ |
| cifs/193 | ✅ 2s | ✅ 2s | ✅ 2s |
| cifs/194 | ❌ | ❌ | ❌ |
| cifs/195 | ✅ 1s | ✅ 2s | ⏭️ |
| cifs/196 | ✅ 1s | ✅ 1s | ⏭️ |
| cifs/197 | ⏭️ | ⏭️ | ⏭️ |
| cifs/198 | ✅ 3s | ✅ 18s | ✅ 5s |
| cifs/199 | ✅ 1s | ✅ 2s | ✅ 3s |
| cifs/200 | ✅ 3s | ✅ 2s | ✅ 9s |
| cifs/201 | ✅ 8s | ✅ 7s | ✅ 89s |
| cifs/202 | ✅ 12s | ✅ 11s | ✅ 16s |
| cifs/203 | ⏭️ | ⏭️ | ⏭️ |
| cifs/206 | ✅ 2s | ⏭️ | ❌ |
| cifs/207 | ⏭️ | ⏭️ | ⏭️ |
| cifs/208 | ✅ 2s | ✅ 1s | ✅ 4s |
| cifs/209 | ✅ 4s | ✅ 3s | ✅ 6s |
| cifs/210 | ✅ 2s | ✅ 2s | ✅ 9s |
| cifs/211 | ✅ 2s | ✅ 1s | ✅ 4s |
| cifs/212 | ✅ 1s | ✅ 2s | ✅ 5s |
| cifs/213 | ✅ 3s | ✅ 2s | ✅ 6s |
| cifs/214 | ✅ 2s | ✅ 2s | ✅ 5s |
| cifs/215 | ✅ 1s | ✅ 1s | ✅ 5s |
| cifs/216 | ✅ 6s | ✅ 6s | ✅ 132s |
| cifs/217 | ✅ 1s | ✅ 2s | ✅ 5s |
| cifs/218 | ✅ 2s | ✅ 2s | ✅ 8s |
| cifs/219 | ✅ 1s | ✅ 2s | ✅ 4s |
| cifs/220 | ⏭️ | ⏭️ | ⏭️ |
| cifs/221 | ✅ 2s | ✅ 2s | ✅ 8s |
| cifs/222 | ✅ 2s | ✅ 2s | ✅ 8s |
| cifs/223 | ✅ 2s | ✅ 1s | ✅ 6s |
| cifs/224 | ⏭️ | ⏭️ | ⏭️ |
| cifs/225 | ⏭️ | ✅ 1s | ⏭️ |
| cifs/226 | ✅ 2s | ✅ 2s | ⏭️ |
| cifs/227 | ✅ 1s | ✅ 2s | ⏭️ |
| cifs/228 | ✅ 3s | ✅ 2s | ✅ 8s |
| cifs/229 | ⏭️ | ✅ 2s | ⏭️ |
| cifs/230 | ⏭️ | ⏭️ | ⏭️ |
| cifs/231 | ✅ 5s | ✅ 4s | ✅ 15s |
| cifs/232 | ⏭️ | ✅ 6s | ⏭️ |
| cifs/233 | ✅ 1s | ✅ 3s | ⏭️ |
| cifs/234 | ⏭️ | ⏭️ | ⏭️ |
| cifs/235 | ✅ 2s | ✅ 2s | ✅ 6s |
| cifs/236 | ✅ 4s | ✅ 3s | ✅ 7s |
| cifs/237 | ✅ 2s | ✅ 2s | ✅ 5s |
| cifs/238 | ❌ | ❌ | ❌ |
| cifs/239 | ✅ 1s | ✅ 1s | ✅ 6s |
| cifs/240 | ⏭️ | ⏭️ | ⏭️ |
| cifs/241 | ✅ 2s | ✅ 2s | ✅ 8s |
| cifs/242 | ✅ 2s | ✅ 2s | ✅ 12s |
| cifs/243 | ✅ 3s | ✅ 3s | ✅ 6s |
| cifs/244 | ✅ 2s | ✅ 1s | ✅ 4s |
| cifs/245 | ✅ 2s | ✅ 2s | ✅ 6s |
| cifs/246 | ✅ 2s | ✅ 3s | ✅ 8s |
| cifs/247 | ✅ 2s | ✅ 2s | ✅ 12s |
| cifs/248 | ⏭️ | ⏭️ | ⏭️ |
| cifs/249 | ✅ 3s | ✅ 3s | ✅ 28s |
| cifs/250 | ✅ 3s | ✅ 4s | ✅ 27s |
| cifs/251 | ✅ 1s | ✅ 1s | ✅ 7s |
| cifs/252 | ⏭️ | ✅ 1s | ⏭️ |
| cifs/253 | ✅ 2s | ✅ 2s | ✅ 16s |
| cifs/254 | ✅ 1s | ⏭️ | ⏭️ |
| cifs/255 | ✅ 2s | ✅ 3s | ⏭️ |
| cifs/256 | ✅ 140s | ✅ 67s | ✅ 2255s |
| cifs/257 | ✅ 3s | ✅ 3s | ✅ 12s |
| cifs/258 | ✅ 2s | ✅ 2s | ✅ 6s |
| cifs/259 | ✅ 13s | ✅ 24s | ✅ 428s |
| cifs/260 | ✅ 2s | ✅ 2s | ✅ 5s |
| cifs/261 | ✅ 12s | ✅ 12s | ✅ 45s |
| cifs/262 | ✅ 1s | ✅ 2s | ✅ 3s |
| cifs/263 | ✅ 2s | ✅ 2s | ✅ 4s |
| cifs/264 | ✅ 2s | ✅ 1s | ✅ 5s |
| cifs/265 | ✅ 1s | ✅ 1s | ✅ 5s |
| cifs/266 | ✅ 6s | ✅ 5s | ✅ 18s |
| cifs/267 | ✅ 2s | ✅ 2s | ✅ 13s |
| cifs/268 | ✅ 2s | ✅ 2s | ✅ 5s |
| cifs/269 | ✅ 41s | ✅ 42s | ✅ 74s |
| cifs/270 | ✅ 4s | ✅ 4s | ✅ 7s |
| cifs/271 | ✅ 1s | ✅ 2s | ✅ 5s |
| cifs/272 | ✅ 2s | ✅ 1s | ✅ 3s |
| cifs/273 | ✅ 4s | ✅ 4s | ✅ 22s |
| cifs/274 | ✅ 3s | ✅ 4s | ✅ 17s |
| cifs/275 | ✅ 72s | ✅ 89s | ✅ 3737s |
| cifs/276 | ✅ 6s | ✅ 7s | ✅ 191s |
| cifs/277 | ✅ 6s | ✅ 10s | ✅ 93s |
| cifs/278 | ✅ 6s | ✅ 8s | ✅ 101s |
| cifs/279 | ✅ 4s | ✅ 3s | ✅ 7s |
| cifs/280 | ✅ 7s | ✅ 8s | ✅ 19s |
| cifs/281 | ✅ 2s | ✅ 2s | ✅ 8s |
| cifs/282 | ✅ 1s | ✅ 3s | ✅ 6s |
| cifs/283 | ✅ 2s | ✅ 2s | ✅ 33s |
| cifs/284 | ✅ 2s | ✅ 3s | ✅ 44s |
| cifs/285 | ✅ 2s | ✅ 3s | ✅ 7s |
| cifs/286 | ✅ 19s | ✅ 22s | ✅ 219s |
| cifs/287 | ✅ 38s | ✅ 38s | ✅ 28s |
| cifs/288 | ✅ 2s | ✅ 2s | ✅ 6s |
| cifs/289 | ✅ 2s | ❌ | ✅ 11s |
| cifs/290 | ✅ 18s | ✅ 12s | ✅ 14s |
| cifs/291 | ❌ | ❌ | ❌ |
| cifs/292 | ✅ 4s | ✅ 4s | ✅ 5s |
| cifs/293 | ✅ 1s | ✅ 1s | ✅ 4s |
| cifs/294 | ✅ 2s | ✅ 2s | ✅ 3s |
| cifs/295 | ✅ 2s | ✅ 1s | ✅ 2s |
| cifs/296 | ✅ 2s | ✅ 2s | ✅ 6s |
| cifs/297 | ❌ | ❌ | ❌ |
| cifs/298 | ✅ 2s | ✅ 2s | ✅ 4s |
| cifs/299 | ✅ 1s | ✅ 1s | ✅ 3s |
| cifs/300 | — | ❌ | ❌ |
| cifs/301 | — | ✅ 2s | ✅ 5s |
| cifs/302 | ✅ 435s | — | — |
| cifs/303 | ✅ 7s | — | — |
| cifs/304 | ✅ 25s | — | — |
| cifs/305 | ✅ 43s | — | — |
| cifs/306 | ⏭️ | ✅ 27s | — |
| cifs/307 | ✅ 19s | — | — |
| cifs/308 | ✅ 33s | — | — |
| cifs/310 | ✅ 9s | — | — |
| cifs/311 | ✅ 191s | — | — |
| cifs/312 | ✅ 20s | — | — |

## Failed Tests

| Test | Samba | Windows | Azure Files | Notes |
|---|---|---|---|---|
| cifs/001 | — | ✅ | ❌ | Azure Files: clone not supported |
| cifs/116 | ✅ | ✅ | ❌ | Azure Files: fallocate punch-hole not supported |
| cifs/120 | ✅ | ✅ | ❌ | Azure Files: byte-range lock failed to acquire |
| cifs/126 | ✅ | ✅ | ❌ | Azure Files: mtime did not refresh after actimeo TTL |
| cifs/127 | ✅ | ✅ | ❌ | Azure Files: QueryDirectories did not increment (no dir leases) |
| cifs/128 | ✅ | ✅ | ❌ | Azure Files: no QueryDirectories increment (no dir leases) |
| cifs/152 | ✅ | ✅ | ❌ | Azure Files: long path error mapping differs |
| cifs/164 | ✅ | ✅ | ❌ | Azure Files: hardlinks not supported |
| cifs/165 | ✅ | ❌ | ✅ | Windows Server session timeout faster than reconnect grace period |
| cifs/178 | ✅ | ⏭️ | ❌ | xattr: setfattr fails on Azure Files / getfattr empty on Windows |
| cifs/194 | ❌ | ❌ | ❌ | ⚠️ cifs-utils bug: mount.cifs doesn't enforce MOUNT_PASSWD_SIZE=512 limit |
| cifs/206 | ✅ | ⏭️ | ❌ | xattr: setfattr fails on Azure Files / getfattr empty on Windows |
| cifs/238 | ❌ | ❌ | ❌ | ⚠️ Client limitation: inotify IN_CREATE not delivered via lease breaks |
| cifs/254 | ✅ | ⏭️ | ⏭️ | user.* xattr not supported on Windows/Azure |
| cifs/289 | ✅ | ❌ | ✅ | ⚠️ Possible kernel bug: segfault in drop_dir_cache on Windows Server |
| cifs/291 | ❌ | ❌ | ❌ | ⚠️ Client issue: readlink on non-existent path returns empty error with mfsymlinks |
| cifs/297 | ❌ | ❌ | ❌ | ⚠️ Client issue: stat on symlink loop succeeds with mfsymlinks (loop not detected) |
| cifs/300 | — | ❌ | ❌ | Server accepts near-max-offset writes (server permissiveness) |
