"""Implement algorithm bodies. See docs/guide/CONTRACTS.md; inputs and outputs are dictionaries."""
def lcs(request):
    """Prefix DP: dp[i][j] = LCS length of a[:i] and b[:j]."""
    a, b = request['a'], request['b']
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        prev, row, ai = dp[i - 1], dp[i], a[i - 1]
        for j in range(1, m + 1):
            if ai == b[j - 1]:
                row[j] = prev[j - 1] + 1
            else:
                row[j] = prev[j] if prev[j] >= row[j - 1] else row[j - 1]
    out = []
    i, j = n, m
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return {'length': dp[n][m], 'sequence': ''.join(reversed(out))}

def merge(request):
    """Interval DP: cost[l][r] = min over k of cost[l][k] + cost[k+1][r] + sum(l..r)."""
    sizes = request['sizes']
    n = len(sizes)
    if n <= 1:
        return {'cost': 0, 'plan': []}
    pre = [0] * (n + 1)
    for i, s in enumerate(sizes):
        pre[i + 1] = pre[i] + s
    cost = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for l in range(0, n - length + 1):
            r = l + length - 1
            total = pre[r + 1] - pre[l]
            best, best_k = None, l
            row_l = cost[l]
            for k in range(l, r):
                c = row_l[k] + cost[k + 1][r]
                if best is None or c < best:
                    best, best_k = c, k
            cost[l][r] = best + total
            split[l][r] = best_k
    plan = []
    stack = [(0, n - 1, False)]
    while stack:
        l, r, done = stack.pop()
        if l == r:
            continue
        k = split[l][r]
        if done:
            plan.append([l, k, r])
        else:
            stack.append((l, r, True))
            stack.append((k + 1, r, False))
            stack.append((l, k, False))
    return {'cost': cost[0][n - 1], 'plan': plan}

def tree(request):
    """Take/skip tree DP in postorder; iterative to survive deep chains."""
    n = request['n']
    if n == 0:
        return {'weight': 0, 'selected': []}
    w = request['weights']
    adj = [[] for _ in range(n)]
    for u, v in request['edges']:
        adj[u].append(v)
        adj[v].append(u)
    parent = [-1] * n
    order = []
    stack = [0]
    seen = [False] * n
    seen[0] = True
    while stack:
        v = stack.pop()
        order.append(v)
        for c in adj[v]:
            if not seen[c]:
                seen[c] = True
                parent[c] = v
                stack.append(c)
    take = [w[v] for v in range(n)]
    skip = [0] * n
    for v in reversed(order):
        p = parent[v]
        if p >= 0:
            take[p] += skip[v]
            skip[p] += take[v] if take[v] > skip[v] else skip[v]
    taken = [False] * n
    selected = []
    for v in order: 
        p = parent[v]
        if (p < 0 or not taken[p]) and take[v] > skip[v]:
            taken[v] = True
            selected.append(v)
    return {'weight': max(take[0], skip[0]), 'selected': selected}

def naive(request):
    """Establish a simple exact-search baseline against which the other two searches can be checked. Implement naive according to docs/guide/CONTRACTS.md."""
    raise NotImplementedError("TODO naive")

def kmp(request):
    """Reuse information about matched prefixes to avoid restarting the search after every mismatch. Implement kmp according to docs/guide/CONTRACTS.md."""
    raise NotImplementedError("TODO kmp")

def rk(request):
    """Reject windows with unequal fingerprints and verify every equal-hash candidate. Implement rk according to docs/guide/CONTRACTS.md."""
    raise NotImplementedError("TODO rk")

def suffix(request):
    """Order the text suffixes and use adjacent common prefixes to find repeated substrings. Implement suffix according to docs/guide/CONTRACTS.md."""
    raise NotImplementedError("TODO suffix")

def aho(request):
    """Build one dictionary automaton and count its patterns in several independent texts. Implement aho according to docs/guide/CONTRACTS.md."""
    raise NotImplementedError("TODO aho")