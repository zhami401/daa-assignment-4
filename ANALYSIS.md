# Assignment 4 — analysis

## Environment and commands

- Language/runtime: Python **[FILL: output of `python --version`]**.
- OS / CPU / RAM: **[FILL: e.g. Windows 11, CPU model, N logical cores, N GiB RAM]** (the benchmark script prints this line too).
- Build: none (interpreted). Startup check: `python tools/run.py --setup`.
- Run one request file: `python tools/run.py --input examples/kmp.jsonl` (or `python Python/source/main.py < examples/kmp.jsonl`).
- Public checks: `python tools/run.py --check` — **[FILL: paste the final result, e.g. all 44 public cases and the repeated batch pass]**.
- Own tests (from the repository root):
  `python tests/student/test_dp.py`, `python tests/student/test_search.py`, `python tests/student/test_suffix_aho.py`.
- Search benchmark: `python tests/student/bench_search.py`.
- Final commit URL (with the full 40-character SHA) is recorded in Moodle.

## Algorithm explanations

All code is in `Python/source/algorithms.py`. `main.py` is the supplied JSON Lines driver; every call receives a fresh request dictionary and no module-level state is kept, so consecutive requests cannot interfere.

### lcs
- **State.** `dp[i][j]` is the length of the longest common subsequence of `a[:i]` and `b[:j]`; `i` and `j` are prefix lengths.
- **Transition / base.** `dp[0][j] = dp[i][0] = 0`. If `a[i-1] == b[j-1]`, then `dp[i][j] = dp[i-1][j-1] + 1`; otherwise `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`.
- **Order.** Row by row, left to right; each cell needs only the cell above, left and diagonal, which are already computed.
- **Correctness.** If the last characters match, some optimal subsequence can use them as its last pair (exchange argument), so the answer is the diagonal plus one. If they differ, at least one of them is unused, so the optimum is the better of the two shorter prefixes.
- **Reconstruction.** Walk from `(n, m)`: on a match take the character and move diagonally; otherwise move to the neighbour with the larger value (ties go up). The characters are collected in reverse and then reversed. Any optimal sequence is accepted, so tie handling does not matter.
- **Cost.** Time and memory O((n+1)(m+1)) for input sizes n=|a|, m=|b|; the output is at most min(n, m) characters.
- **Boundary test.** `a="tea_time", b="team"` → length 4: it detects confusing a subsequence with a substring. Empty inputs return length 0 and `""`.

### merge
- **State.** `cost[l][r]` is the minimum total cost of merging original blocks `l..r` into one block; `split[l][r]` is the split `k` achieving it.
- **Transition / base.** `cost[i][i] = 0`; for `l < r`, `cost[l][r] = min over k in [l, r-1] of cost[l][k] + cost[k+1][r] + sum(l..r)`. The sum comes from prefix sums. The last merge joins `[l,k]` and `[k+1,r]`, and its price is the whole interval sum.
- **Order.** By increasing interval length, so both sub-intervals are shorter and already known.
- **Correctness.** Merges must be adjacent, so every merge tree is a binary tree over the ordered blocks; the root merge fixes the split `k`, and the two subtrees are independent optimal sub-problems.
- **Reconstruction.** Postorder over `split`: emit `[l, k, r]` after both child intervals, i.e. children before the parent, because the parent's blocks only exist once the children are merged. Implemented with an explicit stack. For `n <= 1` the plan is `[]`; otherwise it has exactly n−1 merges.
- **Cost.** O(n³) time, O(n²) auxiliary memory (n ≤ 200); the plan has n−1 entries. Python integers hold costs exactly (up to about 2·10¹¹ here).
- **Boundary test.** `[2,3,4]` → 14 (the other order costs 16); it detects choosing non-optimal splits. `[]` and `[x]` → cost 0, no plan.

### tree
- **State.** For vertex `v` rooted at 0: `take[v]` is the best weight in the subtree of `v` if `v` is selected, `skip[v]` the best if it is not.
- **Transition / base.** `take[v] = w[v] + sum(skip[c])`; `skip[v] = sum(max(take[c], skip[c]))` over children `c`. A leaf has `take = w`, `skip = 0`. The answer is `max(take[root], skip[root])`; since `skip >= 0`, the empty set is always available and all-negative inputs return 0.
- **Order.** A stack-based traversal gives an order where each parent precedes its children; processing it in reverse is a postorder, so children are final before their parent uses them. No recursion is used, so a chain of 100 000 vertices is safe.
- **Correctness.** Choosing `v` forbids exactly its children; not choosing `v` leaves every child free. Subtrees are independent given the state of their root.
- **Reconstruction.** Process vertices top-down: a vertex is selected only if its parent is not selected and `take[v] > skip[v]`. This respects the parent's decision, so no two adjacent vertices are chosen and each vertex appears at most once.
- **Cost.** O(n+1) time and auxiliary memory (adjacency lists, arrays of size n); output is the selected list.
- **Boundary test.** All-negative weights → weight 0, `selected=[]` (detects forcing a non-empty set); n=0 and n=1; a 100 000-vertex chain (detects recursion failure).

### naive
- **Invariant.** For start `i`, the first `j` characters of the window equal `pattern[:j]`.
- **Method.** Try every start `0..n−m`, compare characters left to right, stop at the first mismatch; report `i` if all `m` match. No built-in search is used.
- **Base cases.** Empty pattern → starts `0..n` (n+1 positions, including the final boundary); pattern longer than text → empty loop → `[]`.
- **Correctness.** Every start is tried and checked exactly, so all occurrences, including overlapping ones, are found in increasing order.
- **Cost.** O(n·m + n + 1) time in the worst case, O(1) auxiliary memory, O(z+1) output (z = number of starts).
- **Boundary test.** `aaaaa`/`aaa` → `[0,1,2]` (detects skipping overlaps or missing the last start).

### kmp
- **State.** `pi[i]` is the length of the longest proper prefix of `pattern[:i+1]` that is also its suffix. During the scan, `k` is the length of the pattern prefix currently matched ending at the current text position.
- **Transition.** On mismatch with `k > 0`, set `k = pi[k-1]` (the next-longest border) and retry; on match increment `k`. After a full match (`k == m`) record `i−m+1` and, at the next character, fall back with `k = pi[k-1]` — this keeps overlapping matches.
- **Base cases.** Empty pattern returns `0..n` before any pattern indexing; `pi[0] = 0`.
- **Correctness.** Any matched prefix that can still extend after a mismatch must be a border of the current matched prefix, and borders are visited longest first, so no occurrence is skipped.
- **Cost.** Each text step increases `k` by at most 1 and each fallback decreases it, so the total fallbacks ≤ total increments: O(n + m + z + 1) time, O(m + 1) auxiliary memory, O(z + 1) output.
- **Boundary test.** `abababa`/`aba` → `[0,2,4]` (detects restarting from 0 after a full match and losing overlaps).

### rk
- **Hash.** `H(s) = (s[0]·31^(m−1) + … + s[m−1]) mod 101` with ASCII codes; the leftmost character has the highest power.
- **Rolling update.** `H' = ((H − code(left)·31^(m−1))·31 + code(new)) mod 101`. Python's `%` is non-negative, which normalizes negative remainders (other languages need `+ mod` first).
- **Verification.** Equal hashes are only candidates: the code compares the actual characters before reporting a start. The known collision `ab` and `dj` both hash to 75, so `abdj` with pattern `ab` yields only `[0]`.
- **Base cases.** Empty pattern → `0..n`; `m > n` → `[]`, both handled before any window is formed.
- **Correctness.** Equal strings have equal hashes, so no real match is skipped; every reported start passed a character comparison, so no false match is reported.
- **Cost.** O(n + m + c·m) time where c is the number of equal-hash candidate windows (for a match each candidate costs up to m). With the deliberately small modulus 101 many windows collide, and the worst case is O(n·m) (for example `a…a` against `a…a`: every window is a candidate). It is not linear in the worst case. Memory O(1) auxiliary besides the output.
- **Boundary test.** `abdj`/`ab` (collision), and an empty pattern on empty text → `[0]`.

### suffix
- **Prefix doubling.** `rank[i]` orders suffixes by their first `k` characters (initially their first character). In each round the key of suffix `i` is the pair `(rank[i], rank[i+k])`, with −1 (encoded as 0) when `i+k ≥ n`; sorting by this pair orders suffixes by their first `2k` characters, then `k` doubles. Ties get equal new ranks. The loop ends when all ranks are distinct, after at most ⌈log₂ n⌉ rounds. The pair is packed into one integer so the comparison sort is fast. No sentinel and no empty suffix are added, and no suffix strings are built.
- **Cost of doubling.** O(log n) rounds × O(n log n) comparison sort = O(n log² n) time, O(n) memory.
- **Kasai.** With `rank` as the inverse of `sa`, `lcp[rank[i]]` is the common prefix of suffix `i` and its predecessor in `sa`. Visiting `i = 0..n−1` and keeping `h`, after moving from suffix `i` to `i+1` the common prefix with the predecessor decreases by at most 1, so `h` is decremented once per step and only grows by character comparisons. Total increments ≤ 2n: O(n) time. `lcp[0] = 0` and `lcp[i]` compares `sa[i−1]` with `sa[i]`.
- **Longest repeat.** Two distinct starts sharing a prefix of length L give two suffixes with LCP ≥ L; every suffix between them in sorted order also shares that prefix, so some adjacent pair has LCP ≥ L. Hence the longest repeated substring has length `max(lcp)` and is `text[sa[i] : sa[i] + max(lcp)]` for any maximizing `i`. Overlaps are allowed. If `max(lcp) = 0`, `repeated = ""`.
- **Boundary tests.** `banana` → `sa=[5,3,1,0,4,2]`, `lcp=[0,1,3,0,0,2]`, `repeated="ana"` (overlapping occurrences); empty text → `[]`, `[]`, `""`; `aaaa` (all equal, needs several doubling rounds); one character.
- **Memory.** O(n + 1) auxiliary and output.

### aho
- **Trie.** All patterns are inserted into one trie (dictionary-based children, 95 printable ASCII characters). `term[idx]` is the state where dictionary position `idx` ends; duplicate patterns end in the same state but keep separate positions, so they get equal counts.
- **Failure links.** `fail[v]` is the state of the longest proper suffix of the string of `v` that is also a trie prefix. They are computed breadth-first: for child `v` of `u` by character `ch`, follow `fail` from `u` until a state with child `ch` exists (or the root).
- **Matching.** For each text the state is reset to the root, and visit counts are initialized to 0 (independent texts, no stale counts). For each character, follow failure links until a transition exists, move, and increment `visits[state]`.
- **Counting suffix patterns.** After the text, process states in reverse BFS order and add `visits[v]` to `visits[fail[v]]`. A state visited `c` times means the strings of all its failure ancestors also occurred `c` times (they are suffixes of it), so a pattern's count is the final value at its terminal state. This counts overlaps and suffix patterns (`he` inside `she`) without iterating over individual matches.
- **Output.** One row per text in `texts` order; columns follow the original dictionary positions; an empty dictionary gives an empty row per text; an empty `texts` gives `[]`; an empty text gives zeros.
- **Cost.** Construction O(L + p) with dictionary children (at most O(95·S) if a full table were used; L = total pattern length, p = number of patterns, S = states). Matching one text takes O(|text|) amortized for the failure-link walks, and the propagation plus reading counts take O(S + p), so O(|text| + S + p) per text. Memory O(S + p) for the trie plus O(q·p) for the output.
- **Boundary tests.** `["he","she","he"]` on `["sheshe","sheshe",""]` → `[[2,2,2],[2,2,2],[0,0,0]]`; empty dictionary; empty texts array; two requests in a row with different patterns (detects state kept between requests).

## Own tests

All three files compare against independent brute-force oracles (subset/subsequence enumeration, exhaustive interval and independent-set search, sorting of actual suffixes, `str.find` counting) and are run from the repository root. **[FILL: confirm that you ran each command on your machine and edit the "Actual result" column if anything differs.]**

|Command|Input or fixture path|Expected result|Actual result / log|What it checks|
|---|---|---|---|---|
|`python tests/student/test_dp.py`|400 random pairs a,b over `abc ` (≤9 chars); `tea_time`/`team`; empty strings|length equals brute-force LCS, sequence is a subsequence of both|prints `lcs ok`|LCS value and witness; subsequence vs substring|
|same|400 random block lists incl. zeros and 10⁹; `[2,3,4]`; 200 random blocks|cost equals brute-force interval DP; plan is chronological, adjacent, n−1 merges, sums to cost|prints `merge ok`; 200 blocks well under 1 s|merge value, plan validity, scale|
|same|500 random trees n≤11 with random labels, negative weights; chain of 100 000; star with all negative|weight equals brute force over all subsets; selected has no adjacent or repeated vertices and sums to weight|prints `tree ok`; chain in about 0.1 s|tree value, witness, deep chain|
|`python tests/student/test_search.py`|3000 random (text, pattern) pairs over alphabets incl. `abdj`, spaces and punctuation; fixed cases|naive = kmp = rk = `str.find` oracle|prints `small/boundary ok`|overlaps, empty pattern/text, long pattern, case sensitivity, `ab`/`dj` collision|
|same|`a`×10000 vs `a`×2000; `a`×200000 vs `a`×100000|correct positions; completes well within 20 s|about 1 s for rk worst case; kmp ≈ 0.04 s|RK candidate-heavy worst case; KMP limits|
|`python tests/student/test_suffix_aho.py`|1500 random texts ≤14 chars|`sa` equals sorting of real suffixes; `lcp` equals direct comparison; `repeated` length equals brute-force longest repeat and occurs twice|prints `suffix small ok`|SA, Kasai, repeat witness, empty/one/all-equal|
|same|texts of 50 000 characters (random, all `a`, `abab…`, printable ASCII)|valid permutation, sorted order spot-checked|each ≈ 0.1–0.2 s|scale of prefix doubling|
|same|1500 random dictionaries × texts; `she/he/she`; empty dictionary; empty texts|counts equal brute-force occurrence counting|prints `aho small ok`|overlaps, suffix patterns, duplicates, empties, no stale state|
|same|`a`×1…446 on `a`×200 000; 10 000 patterns × 100 texts|expected counts; completes within limit|about 0.02 s and 0.2 s|dense matches, large dictionaries|
|`python tools/run.py --check`|44 public cases + repeated mixed batch|all pass|**[FILL: paste final line(s)]**|contract schema, state reset between batches|

## Search comparison

Paste the output of `python tests/student/bench_search.py` below (it also saves `tests/student/bench_results.md`). The script uses the same `(text, pattern)` for naive, KMP and exact RK; first checks that the three outputs are identical and equal to a `str.find` oracle; then does one untimed warm-up call and three timed runs per algorithm/size/case.

- Common domain: n, m ≤ 3000, sizes (n, m) = (500, 50), (1500, 150), (3000, 300).
- Generators (seeded `random.Random`, seed string shown in the table): `random` — uniform lowercase text, pattern is a random substring of it (at least one match); `repetitive-nomatch` — `a`ⁿ against `a`^(m−1)`b` (naive does about (n−m+1)·m comparisons, no matches); `repetitive-allmatch` — `a`ⁿ against `a`^m (every window matches, so RK verifies every window).
- Timing scope: only the algorithm call on an already parsed request dictionary (no JSON parsing, no process start, no generation); `time.perf_counter_ns`, milliseconds. Python has no JIT; the warm-up is one untimed call. Compilation is not involved.
- Commands: `python tests/student/bench_search.py` from the repository root.

**[PASTE the environment line and the Markdown table from the script output here.]**

### Observations

**[CHECK against your own table and edit the wording to match what you measured.]**

- On `random` text naive is not slower than KMP, because mismatches are usually found at the first character of a window, so it does only about n comparisons. RK pays for computing a hash for every window, so its constant is higher in Python.
- On `repetitive-nomatch` naive grows roughly with n·m (compare your 500/1500/3000 rows: n and m grow together, so the time grows much faster than linearly), while KMP and RK stay close to linear in n.
- On `repetitive-allmatch` RK is as slow as naive: every window is an equal-hash candidate and is verified in O(m). This shows the c·m term in O(n + m + c·m); KMP stays linear plus output.
- Wall-clock times on one machine do not prove an asymptotic bound; they are consistent with, but do not establish, the stated complexities. Times of a few tenths of a millisecond are close to timer and interpreter noise, so use the medians and the larger sizes for comparison.
- Modulus 101 effect: with only 101 possible hash values, unequal windows collide with probability about 1/101 for random-like data, so verification runs on a noticeable fraction of windows, and in the worst case on all windows. This conclusion is about this assignment's deliberately small modulus, not about production hash implementations with a large modulus or randomized base. The known collision `ab`/`dj` (both 75) is kept as a correctness test (`test_search.py` and the public case `rk-collision`).

## Sources and AI assistance

- Course materials: the supplied assignment specification (`docs/guide/CONTRACTS.md`, `RUBRIC.md`, `TESTING.md`) and the Week 8–10 lecture material.
- AI assistance: **[FILL IN HONESTLY]** Claude (Anthropic) generated the first versions of the implementations in `Python/source/algorithms.py`, the own tests in `tests/student/`, the benchmark script, and a draft of this document. My own contribution and verification: **[FILL: e.g. I ran `python tools/run.py --check` and all three own test files on my machine, ran the benchmark and pasted its real output, read and traced each algorithm on the examples, and can explain them.]** Edit these sentences so they describe exactly what you did.
