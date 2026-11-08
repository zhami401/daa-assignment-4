"""Own tests for suffix (sa, lcp, repeated) and aho. Oracles are brute force and independent of the algorithms."""
import pathlib, random, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'Python' / 'source'))
import algorithms as A

def brute_sa(t):
    return sorted(range(len(t)), key=lambda i: t[i:])
def common(a, b):
    k = 0
    while k < min(len(a), len(b)) and a[k] == b[k]:
        k += 1
    return k
def longest_repeat_len(t):
    best = 0
    for i in range(len(t)):
        for j in range(i + 1, len(t)):
            best = max(best, common(t[i:], t[j:]))
    return best

random.seed(11)
for _ in range(1500):
    alpha = random.choice(['a', 'ab', 'abc', 'ab .', 'abcdefgh'])
    t = ''.join(random.choice(alpha) for _ in range(random.randint(0, 14)))
    r = A.suffix({'text': t})
    sa = brute_sa(t)
    assert r['sa'] == sa, (t, r, sa)
    exp_lcp = ([0] if t else []) + [common(t[sa[i - 1]:], t[sa[i]:]) for i in range(1, len(t))]
    assert r['lcp'] == exp_lcp, (t, r, exp_lcp)
    L = longest_repeat_len(t)
    rep = r['repeated']
    assert len(rep) == L, (t, rep, L)
    if L: 
        starts = [i for i in range(len(t) - L + 1) if t[i:i + L] == rep]
        assert len(starts) >= 2, (t, rep)
assert A.suffix({'text': 'banana'}) == {'sa': [5, 3, 1, 0, 4, 2], 'lcp': [0, 1, 3, 0, 0, 2], 'repeated': 'ana'}
assert A.suffix({'text': ''}) == {'sa': [], 'lcp': [], 'repeated': ''}
assert A.suffix({'text': 'x'}) == {'sa': [0], 'lcp': [0], 'repeated': ''}
assert A.suffix({'text': 'abcd'})['repeated'] == ''
assert A.suffix({'text': 'aaaa'}) == {'sa': [3, 2, 1, 0], 'lcp': [0, 1, 2, 3], 'repeated': 'aaa'}
print('suffix small ok')

def brute_aho(patterns, texts):
    out = []
    for t in texts:
        row = []
        for p in patterns:
            row.append(sum(1 for i in range(len(t) - len(p) + 1) if t[i:i + len(p)] == p))
        out.append(row)
    return out
for _ in range(1500):
    alpha = random.choice(['a', 'ab', 'abc', 'aB .'])
    pats = [''.join(random.choice(alpha) for _ in range(random.randint(1, 5))) for _ in range(random.randint(0, 6))]
    texts = [''.join(random.choice(alpha) for _ in range(random.randint(0, 14))) for _ in range(random.randint(0, 4))]
    got = A.aho({'patterns': pats, 'texts': texts})['counts']
    assert got == brute_aho(pats, texts), (pats, texts, got)
assert A.aho({'patterns': ['he', 'she', 'he'], 'texts': ['sheshe', 'sheshe', '']}) == {'counts': [[2, 2, 2], [2, 2, 2], [0, 0, 0]]}
assert A.aho({'patterns': [], 'texts': ['abc', '']}) == {'counts': [[], []]}
assert A.aho({'patterns': ['a'], 'texts': []}) == {'counts': []}
assert A.aho({'patterns': ['a'], 'texts': ['aa']}) == {'counts': [[2]]}
assert A.aho({'patterns': ['b'], 'texts': ['aa']}) == {'counts': [[0]]}
print('aho small ok')

def timed(name, f):
    t = time.time(); r = f(); print(name, round(time.time() - t, 2), 's'); return r
n = 50000
t_rand = ''.join(random.choice('ab') for _ in range(n))
r = timed('suffix random ab 50000', lambda: A.suffix({'text': t_rand}))
assert sorted(r['sa']) == list(range(n))
assert all(t_rand[r['sa'][i - 1]:r['sa'][i - 1] + 300] <= t_rand[r['sa'][i]:r['sa'][i] + 300] for i in range(1, n))
r = timed('suffix all a 50000', lambda: A.suffix({'text': 'a' * n})); assert r['repeated'] == 'a' * (n - 1)
r = timed('suffix abab.. 50000', lambda: A.suffix({'text': 'ab' * (n // 2)})); assert len(r['repeated']) == n - 2
r = timed('suffix printable 50000', lambda: A.suffix({'text': ''.join(chr(random.randint(32, 126)) for _ in range(n))}))

pats = ['a' * k for k in range(1, 447)]
r = timed('aho dense 1 text 200000', lambda: A.aho({'patterns': pats, 'texts': ['a' * 200000]}))
assert r['counts'][0][0] == 200000 and r['counts'][0][445] == 200000 - 446 + 1
pats2 = [''.join(random.choice('abc') for _ in range(10)) for _ in range(10000)]
texts2 = [''.join(random.choice('abc') for _ in range(2000)) for _ in range(100)]
timed('aho 10000 patterns x 100 texts', lambda: A.aho({'patterns': pats2, 'texts': texts2}))
pats3 = ['a' * 100000]
timed('aho one long pattern', lambda: A.aho({'patterns': pats3, 'texts': ['a' * 200000] }))
res = A.aho({'patterns': pats2[:50], 'texts': texts2[:3]})['counts']
assert res == brute_aho(pats2[:50], texts2[:3])
print('scale ok')
