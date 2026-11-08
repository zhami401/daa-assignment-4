"""Own tests for naive / kmp / rk. The oracle uses str.find, written independently of the algorithms."""
import pathlib, random, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'Python' / 'source'))
import algorithms as A

def oracle(text, pattern):
    if pattern == '':
        return list(range(len(text) + 1))
    out, i = [], text.find(pattern)
    while i != -1:
        out.append(i)
        i = text.find(pattern, i + 1)
    return out

def all_three(text, pattern):
    req = {'text': text, 'pattern': pattern}
    return A.naive(req)['positions'], A.kmp(req)['positions'], A.rk(req)['positions']

random.seed(7)
for _ in range(3000):
    alpha = random.choice(['ab', 'abc', 'a', 'aB .!', 'abdj'])
    text = ''.join(random.choice(alpha) for _ in range(random.randint(0, 25)))
    pat = ''.join(random.choice(alpha) for _ in range(random.randint(0, 6)))
    exp = oracle(text, pat)
    got = all_three(text, pat)
    assert got[0] == got[1] == got[2] == exp, (text, pat, exp, got)

assert all_three('aaaaa', 'aaa') == ([0, 1, 2],) * 3
assert all_three('abababa', 'aba') == ([0, 2, 4],) * 3
assert all_three('abc', '') == ([0, 1, 2, 3],) * 3
assert all_three('', '') == ([0],) * 3
assert all_three('', 'a') == ([],) * 3
assert all_three('ab', 'abc') == ([],) * 3
assert all_three('Ab ab', 'ab') == ([3],) * 3
h = lambda s: __import__('functools').reduce(lambda a, c: (a * 31 + ord(c)) % 101, s, 0)
assert h('ab') == h('dj') == 75
assert all_three('abdj', 'ab') == ([0],) * 3
assert all_three('abdjdjab', 'dj') == ([2, 4],) * 3
assert all_three('zzzzzabzzz', 'zzab') == ([3],) * 3
print('small/boundary ok')

t = time.time(); r = A.rk({'text': 'a' * 10000, 'pattern': 'a' * 2000}); print('rk all-candidates', round(time.time() - t, 2), len(r['positions']))
t = time.time(); r = A.naive({'text': 'a' * 3000, 'pattern': 'a' * 1500}); print('naive worst', round(time.time() - t, 2), len(r['positions']))
big = ''.join(random.choice('ab') for _ in range(200000)); p = big[1000:1000 + 100000]
t = time.time(); r = A.kmp({'text': big, 'pattern': p}); print('kmp 2e5/1e5', round(time.time() - t, 2), r['positions'][:3])
assert r['positions'] == oracle(big, p)
t = time.time(); r = A.kmp({'text': 'a' * 200000, 'pattern': 'a' * 100000}); print('kmp dense', round(time.time() - t, 2), len(r['positions']))
t = time.time(); r = A.kmp({'text': 'a' * 200000, 'pattern': ''}); print('kmp empty pattern', round(time.time() - t, 2), len(r['positions']))
