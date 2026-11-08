Environment: Python 3.14.5 (CPython), macOS-27.0.1-arm64-arm-64bit-Mach-O, arm, logical CPUs 8, RAM GiB unknown (fill in manually)

|Case|n|m|Seed/generator|Algorithm|Run 1 (ms)|Run 2 (ms)|Run 3 (ms)|Median (ms)|Correct outputs checked|
|---|---:|---:|---|---|---:|---:|---:|---:|---|
|random|500|50|seed "2026-random-500-50", random.Random|naive|0.022|0.021|0.021|0.021|yes: naive=kmp=rk=str.find oracle, 1 starts|
|random|500|50|seed "2026-random-500-50", random.Random|kmp|0.022|0.021|0.021|0.021|yes: naive=kmp=rk=str.find oracle, 1 starts|
|random|500|50|seed "2026-random-500-50", random.Random|rk|0.054|0.054|0.054|0.054|yes: naive=kmp=rk=str.find oracle, 1 starts|
|random|1500|150|seed "2026-random-1500-150", random.Random|naive|0.068|0.067|0.067|0.067|yes: naive=kmp=rk=str.find oracle, 1 starts|
|random|1500|150|seed "2026-random-1500-150", random.Random|kmp|0.064|0.064|0.064|0.064|yes: naive=kmp=rk=str.find oracle, 1 starts|
|random|1500|150|seed "2026-random-1500-150", random.Random|rk|0.163|0.162|0.162|0.162|yes: naive=kmp=rk=str.find oracle, 1 starts|
|random|3000|300|seed "2026-random-3000-300", random.Random|naive|0.134|0.135|0.134|0.134|yes: naive=kmp=rk=str.find oracle, 1 starts|
|random|3000|300|seed "2026-random-3000-300", random.Random|kmp|0.130|0.128|0.128|0.128|yes: naive=kmp=rk=str.find oracle, 1 starts|
|random|3000|300|seed "2026-random-3000-300", random.Random|rk|0.323|0.313|0.313|0.313|yes: naive=kmp=rk=str.find oracle, 1 starts|
|repetitive-nomatch|500|50|seed "2026-repetitive-nomatch-500-50", random.Random|naive|0.733|0.728|0.740|0.733|yes: naive=kmp=rk=str.find oracle, 0 starts|
|repetitive-nomatch|500|50|seed "2026-repetitive-nomatch-500-50", random.Random|kmp|0.048|0.048|0.048|0.048|yes: naive=kmp=rk=str.find oracle, 0 starts|
|repetitive-nomatch|500|50|seed "2026-repetitive-nomatch-500-50", random.Random|rk|0.046|0.046|0.046|0.046|yes: naive=kmp=rk=str.find oracle, 0 starts|
|repetitive-nomatch|1500|150|seed "2026-repetitive-nomatch-1500-150", random.Random|naive|5.995|5.851|5.679|5.851|yes: naive=kmp=rk=str.find oracle, 0 starts|
|repetitive-nomatch|1500|150|seed "2026-repetitive-nomatch-1500-150", random.Random|kmp|0.121|0.122|0.122|0.122|yes: naive=kmp=rk=str.find oracle, 0 starts|
|repetitive-nomatch|1500|150|seed "2026-repetitive-nomatch-1500-150", random.Random|rk|0.121|0.120|0.121|0.121|yes: naive=kmp=rk=str.find oracle, 0 starts|
|repetitive-nomatch|3000|300|seed "2026-repetitive-nomatch-3000-300", random.Random|naive|23.279|22.620|22.843|22.843|yes: naive=kmp=rk=str.find oracle, 0 starts|
|repetitive-nomatch|3000|300|seed "2026-repetitive-nomatch-3000-300", random.Random|kmp|0.274|0.265|0.263|0.265|yes: naive=kmp=rk=str.find oracle, 0 starts|
|repetitive-nomatch|3000|300|seed "2026-repetitive-nomatch-3000-300", random.Random|rk|0.241|0.245|0.242|0.242|yes: naive=kmp=rk=str.find oracle, 0 starts|
|repetitive-allmatch|500|50|seed "2026-repetitive-allmatch-500-50", random.Random|naive|0.636|0.627|0.626|0.627|yes: naive=kmp=rk=str.find oracle, 451 starts|
|repetitive-allmatch|500|50|seed "2026-repetitive-allmatch-500-50", random.Random|kmp|0.041|0.040|0.040|0.040|yes: naive=kmp=rk=str.find oracle, 451 starts|
|repetitive-allmatch|500|50|seed "2026-repetitive-allmatch-500-50", random.Random|rk|0.671|0.653|0.653|0.653|yes: naive=kmp=rk=str.find oracle, 451 starts|
|repetitive-allmatch|1500|150|seed "2026-repetitive-allmatch-1500-150", random.Random|naive|5.689|5.684|5.663|5.684|yes: naive=kmp=rk=str.find oracle, 1351 starts|
|repetitive-allmatch|1500|150|seed "2026-repetitive-allmatch-1500-150", random.Random|kmp|0.130|0.129|0.129|0.129|yes: naive=kmp=rk=str.find oracle, 1351 starts|
|repetitive-allmatch|1500|150|seed "2026-repetitive-allmatch-1500-150", random.Random|rk|5.815|5.804|5.853|5.815|yes: naive=kmp=rk=str.find oracle, 1351 starts|
|repetitive-allmatch|3000|300|seed "2026-repetitive-allmatch-3000-300", random.Random|naive|22.708|22.680|22.807|22.708|yes: naive=kmp=rk=str.find oracle, 2701 starts|
|repetitive-allmatch|3000|300|seed "2026-repetitive-allmatch-3000-300", random.Random|kmp|0.285|0.284|0.284|0.284|yes: naive=kmp=rk=str.find oracle, 2701 starts|
|repetitive-allmatch|3000|300|seed "2026-repetitive-allmatch-3000-300", random.Random|rk|23.109|23.161|23.107|23.109|yes: naive=kmp=rk=str.find oracle, 2701 starts|
