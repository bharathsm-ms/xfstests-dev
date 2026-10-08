# CIFS Test Results

**Updated:** 2026-10-07 | **Results through:** 2026-10-07

**Scope:** 290 committed tests: 269 in the last-known remote inventory and
21 committed locally but not yet pushed. Untracked tests are excluded.

## Summary

| Server | Test Dates (2026) | ✅ Pass | ❌ Fail | ⏭️ Skip | ⏱️ Timeout | ⏸️ Deferred | Total |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Samba 4.22.11 | Oct 6-7 | 239 | 24 | 27 | 0 | 0 | 290 |
| Azure | Oct 3-7 | 206 | 26 | 54 | 3 | 1 | 290 |
| Windows | Oct 1-3, 7 | 218 | 22 | 49 | 0 | 1 | 290 |
| ksmbd | Sep 25, Oct 7 | 210 | 16 | 41 | 2 | 0 | 269 |

ksmbd has no recorded results for 21 committed tests. These are shown as `-`
in the matrix, not counted as skips. Deferred tests were not run.

[View all 290 test results](#complete-per-test-matrix)
| [Failure and skip reasons](cifs-results-failures-20261006.md)
| [Run details and sources](cifs-results-20261006.md)
| [Test catalogue](README.cifs-tests.md)

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

## Previous Reports

Historical reports have their own test inventories and are not included in
the totals above.

- [Windows: October 1](cifs-results-windows-20261001.md)
- [ksmbd: September 25](cifs-results-ksmbd-20260925.md)
- [Azure: September 24](cifs-results-azure-20260924.md)
- [Samba: September 17 (includes local candidates)](cifs-results-20260917.md)
- [Cross-server results: March 6](cifs-results.md)

<details>
<summary>Windows: 2026-10-01</summary>

[Windows results](cifs-results-windows-20261001.md): completed from 13:43:07 to
14:22:45 UTC against the two Windows shares at `192.168.0.1`. Scope is the same
269 published tests at `1ebff9ed`; the Windows edition/build was not identified.

| Result | Windows |
| --- | ---: |
| PASS | 209 |
| FAIL | 22 |
| SKIP | 37 |
| TIMEOUT | 0 |
| NOT_RUN | 1 |
| **Total** | **269** |

Failed test IDs (`cifs/` prefix omitted):

```text
106 108 127 128 146 191 192 194 216 221 232 238 251 304 310 335
341 348 351 376 380 388
```

All 268 selected tests finished. Test `168` was deliberately deferred with
approval because its ENOSPC workload would consume approximately 353 GiB.
Failures include permission denials, test thresholds/output issues, and content
mismatches needing isolation; they are not all established Windows defects.
Original host mounts and monitored settings were preserved. Remote cleanup is
not certified: `192` logged a nonempty directory. The full report contains all
outcomes, failure evidence, skip reasons, and the host audit.

</details>

<details>
<summary>ksmbd: 2026-09-25</summary>

[ksmbd results](cifs-results-ksmbd-20260925.md): completed on 2026-09-25 UTC
against all 269 published tests at `1ebff9ed`.

| Result | ksmbd |
| --- | ---: |
| PASS | 209 |
| FAIL | 17 |
| SKIP | 41 |
| TIMEOUT | 2 |
| NOT_RUN | 0 |
| **Total** | **269** |

Failed test IDs (`cifs/` prefix omitted):

```text
106 108 122 125 157 192 194 198 238 341 347 354 358 380 382 388
394
```

Timeouts: `147`, `152`. All tests were reached. This local baseline used bounded
ext4 shares with multichannel, SMB2 leases, and durable handles disabled; it
does not replace the Azure or Samba results. Failures include fixture assumptions
and test-observation limits, not only potential client/server defects. See the
full report for every outcome and failure/skip evidence. Samba was restored,
and the temporary ksmbd service and RAM-backed fixtures were shut down/released.

</details>

<details>
<summary>Azure Files: 2026-09-25</summary>

**Results updated**: 2026-09-25. **Test run (UTC)**: 2026-09-24.
These are the completed run's results, not a new September 25 rerun.
Scope: 269 published tests at `1ebff9ed`.

| Result | Azure Files |
| --- | ---: |
| PASS | 201 |
| FAIL | 23 |
| SKIP | 41 |
| TIMEOUT | 3 |
| NOT_RUN | 1 |
| **Total** | **269** |

Failed test IDs (`cifs/` prefix omitted):

```text
001 103 116 120 127 128 133 152 164 178 192 194 202 206 216 238
310 341 351 358 376 388 393
```

Timeouts: `256`, `275`, `311`. Test `168` was deliberately deferred because
its ENOSPC workload would fill approximately 168 GiB. All other tests were
reached. Failures include test/profile assumptions and unsupported operations;
they are not all established Azure defects.

See the [full Azure report](cifs-results-azure-20260924.md) for complete pass/skip
lists, failure evidence, and post-run audit results.

</details>

<details>
<summary>Historical Cross-Backend Results: 2026-03-13</summary>

**Generated**: 2026-03-13

> The tables below are preserved from Samba, Windows Server, and Azure Files
> reruns completed on `2026-03-13`. They do not describe the repaired September code.
>
> `cifs/289` was intentionally excluded on all three backends and is counted as failed by policy for now, due to the known Windows `drop_dir_cache` bug.

### Historical Summary

| Result | Samba | Windows Server | Azure Files |
|---|---|---|---|
| ✅ Passed | **166** | **168** | **150** |
| ⏭️ Skipped | **36** | **33** | **45** |
| ❌ Failed | **8** | **9** | **15** |
| **Total** | **210** | **210** | **210** |

### Historical Environment

| Parameter | Samba | Windows Server | Azure Files |
|---|---|---|---|
| **Client Kernel** | 7.0.0-070000rc3-generic | 7.0.0-070000rc3-generic | 7.0.0-070000rc3-generic |
| **Server** | Samba 4.21.4 (localhost) | Windows Server | Azure Files Premium |
| **Protocol** | SMB3 (auto) | SMB 3.1.1 | SMB 3.1.1 |
| **Multichannel** | No (single NIC) | Yes (3 channels) | Yes (multichannel) |

### Historical Detailed Results

| Test | Samba | Windows | Azure Files |
|---|---|---|---|
| cifs/001 | ✅ 1s | ✅ 2s | ❌ |
| cifs/100 | ✅ 2s | ✅ 2s | ✅ 2s |
| cifs/101 | ✅ 2s | ✅ 2s | ✅ 7s |
| cifs/102 | ✅ 2s | ✅ 2s | ✅ 8s |
| cifs/103 | ✅ 2s | ✅ 2s | ✅ 5s |
| cifs/104 | ✅ 2s | ✅ 2s | ✅ 5s |
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
| cifs/118 | ✅ 1s | ✅ 1s | ✅ 4s |
| cifs/119 | ✅ 2s | ✅ 1s | ✅ 3s |
| cifs/120 | ✅ 2s | ✅ 3s | ❌ |
| cifs/121 | ✅ 2s | ✅ 1s | ✅ 3s |
| cifs/122 | ✅ 1s | ✅ 2s | ✅ 6s |
| cifs/123 | ✅ 2s | ✅ 2s | ✅ 3s |
| cifs/124 | ✅ 34s | ✅ 33s | ✅ 35s |
| cifs/125 | ✅ 16s | ✅ 16s | ✅ 20s |
| cifs/126 | ✅ 13s | ✅ 12s | ❌ |
| cifs/127 | ✅ 34s | ✅ 34s | ✅ 39s |
| cifs/128 | ✅ 2s | ✅ 1s | ✅ 6s |
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
| cifs/146 | ✅ 2s | ❌ | ✅ 12s |
| cifs/147 | ✅ 3s | ✅ 3s | ✅ 4s |
| cifs/148 | ✅ 13s | ✅ 13s | ✅ 18s |
| cifs/149 | ⏭️ | ⏭️ | ⏭️ |
| cifs/150 | ✅ 53s | ✅ 56s | ✅ 65s |
| cifs/151 | ⏭️ | ⏭️ | ⏭️ |
| cifs/152 | ✅ 3s | ✅ 2s | ❌ |
| cifs/153 | ✅ 9s | ✅ 10s | ✅ 26s |
| cifs/154 | ✅ 1s | ✅ 2s | ⏭️ |
| cifs/155 | ✅ 2s | ✅ 2s | ✅ 4s |
| cifs/156 | ⏭️ | ⏭️ | ⏭️ |
| cifs/157 | ✅ 1s | ✅ 2s | ⏭️ |
| cifs/158 | ⏭️ | ⏭️ | ⏭️ |
| cifs/159 | ✅ 2s | ✅ 1s | ⏭️ |
| cifs/160 | ✅ 2s | ✅ 2s | ✅ 3s |
| cifs/161 | ⏭️ | ⏭️ | ⏭️ |
| cifs/162 | ✅ 7s | ✅ 8s | ✅ 9s |
| cifs/163 | ⏭️ | ⏭️ | ⏭️ |
| cifs/164 | ✅ 1s | ✅ 1s | ❌ |
| cifs/165 | ✅ 9s | ✅ 9s | ✅ 26s |
| cifs/166 | ✅ 17s | ✅ 17s | ✅ 284s |
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
| cifs/184 | ✅ 12s | ❌ | ✅ 30s |
| cifs/185 | ⏭️ | ⏭️ | ⏭️ |
| cifs/186 | ✅ 2s | ✅ 1s | ✅ 4s |
| cifs/187 | ✅ 3s | ✅ 7s | ✅ 72s |
| cifs/188 | ✅ 12s | ✅ 12s | ✅ 14s |
| cifs/189 | ⏭️ | ⏭️ | ⏭️ |
| cifs/190 | ✅ 3s | ✅ 3s | ✅ 21s |
| cifs/191 | ❌ | ❌ | ⏭️ |
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
| cifs/206 | ✅ 1s | ⏭️ | ❌ |
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
| cifs/221 | ❌ | ✅ 2s | ✅ 8s |
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
| cifs/275 | ❌ | ❌ | ✅ 3737s |
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
| cifs/289 | ❌ excluded | ❌ excluded | ❌ excluded |
| cifs/290 | ✅ 18s | ✅ 12s | ✅ 14s |
| cifs/291 | ❌ | ❌ | ❌ |
| cifs/292 | ✅ 4s | ✅ 4s | ✅ 5s |
| cifs/293 | ✅ 1s | ✅ 1s | ✅ 4s |
| cifs/294 | ✅ 2s | ✅ 2s | ✅ 3s |
| cifs/295 | ✅ 2s | ✅ 1s | ✅ 2s |
| cifs/296 | ✅ 2s | ✅ 2s | ✅ 6s |
| cifs/297 | ✅ 1s | ✅ 1s | ❌ |
| cifs/298 | ✅ 2s | ✅ 2s | ✅ 4s |
| cifs/299 | ✅ 1s | ✅ 1s | ✅ 3s |
| cifs/300 | ❌ | ❌ | ❌ |
| cifs/301 | ✅ 2s | ✅ 2s | ✅ 5s |
| cifs/302 | ✅ 445s | ✅ 495s | ✅ 473s |
| cifs/303 | ✅ 8s | ✅ 11s | ❌ 11s |
| cifs/304 | ✅ 23s | ✅ 24s | ✅ 218s |
| cifs/305 | ✅ 39s | ✅ 56s | ✅ 640s |
| cifs/306 | ✅ 27s | ✅ 29s | ✅ 59s |
| cifs/307 | ✅ 19s | ✅ 19s | ✅ 404s |
| cifs/308 | ✅ 33s | ✅ 35s | ✅ 97s |
| cifs/310 | ⏭️ | ⏭️ | ⏭️ |
| cifs/311 | ⏭️ | ⏭️ | ⏭️ |
| cifs/312 | ✅ 20s | ✅ 19s | ✅ 283s |

### Historical Failed Tests

`cifs/289` was intentionally excluded from the reruns below and is counted as failed on all backends for now.

| Test | Samba | Windows | Azure Files | Notes |
|---|---|---|---|---|
| cifs/001 | ✅ | ✅ | ❌ | Azure Files: clone not supported |
| cifs/116 | ✅ | ✅ | ❌ | Azure Files: fallocate punch-hole not supported |
| cifs/120 | ✅ | ✅ | ❌ | Azure Files: byte-range lock failed to acquire |
| cifs/126 | ✅ | ✅ | ❌ | Azure Files: mtime did not refresh after actimeo TTL |
| cifs/146 | ✅ | ❌ | ✅ | Windows Server: statfs used delta outside tolerance |
| cifs/152 | ✅ | ✅ | ❌ | Azure Files: long path error mapping differs |
| cifs/164 | ✅ | ✅ | ❌ | Azure Files: hardlinks not supported |
| cifs/178 | ✅ | ⏭️ | ❌ | Azure Files: clone-range semantics still fail |
| cifs/184 | ✅ | ❌ | ✅ | Windows Server: second-half write failed during reconnect test |
| cifs/191 | ❌ | ❌ | ✅ | Samba single-channel workload failed; Windows multichannel gain was below the expected 2x |
| cifs/194 | ❌ | ❌ | ❌ | ⚠️ `mount.cifs` accepted an oversized password value |
| cifs/206 | ✅ | ⏭️ | ❌ | Azure Files: clone operation behavior differs |
| cifs/221 | ❌ | ✅ | ✅ | Samba: mode was not persisted after remount |
| cifs/238 | ❌ | ❌ | ❌ | ⚠️ Client limitation: `IN_CREATE` not delivered via `cifs_atomic_open()` |
| cifs/275 | ❌ | ❌ | ❌ | Directory leases still did not reduce `QueryDirectories` |
| cifs/289 | ❌ | ❌ | ❌ | Excluded from reruns and counted failed for now due to the known Windows `drop_dir_cache` bug |
| cifs/291 | ❌ | ❌ | ❌ | Negative lookup test reported one failing case |
| cifs/300 | ❌ | ❌ | ❌ | Write-beyond-max-offset test still reports failures |
| cifs/303 | ✅ | ✅ | ❌ | Azure Files: git workload failed (`merge failed`, `feature.txt missing after merge`, `expected >=3 commits, got 2`) |

</details>
