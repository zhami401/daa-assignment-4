import os, pathlib, platform, random, statistics, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'Python' / 'source'))
import algorithms as A

SEED = 2026
SIZES = [(500, 50), (1500, 150), (3000, 300)]
RUNS = 3

def oracle(text, pattern):
    out, i = [], text.find(pattern)
    while i != -1:
        out.append(i)
        i = text.find(pattern, i + 1)
    return out

def make(case, n, m, rng):
    if case == 'random':
        text = ''.join(rng.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(n))
        s = rng.randrange(n - m + 1)
        return text, text[s:s + m]
    if case == 'repetitive-nomatch':
        return 'a' * n, 'a' * (m - 1) + 'b'
    if case == 'repetitive-allmatch':
        return 'a' * n, 'a' * m
    raise ValueError(case)

def timed(fn, req):
    t = time.perf_counter_ns()
    fn(req)
    return (time.perf_counter_ns() - t) / 1e6

def ram_gib():
    try:
        with open('/proc/meminfo') as f:
            return round(int(f.readline().split()[1]) / 1048576, 1)
    except Exception:
        return 'unknown (fill in manually)'

env = (f'Python {platform.python_version()} ({platform.python_implementation()}), {platform.platform()}, '
       f'{platform.processor() or platform.machine()}, logical CPUs {os.cpu_count()}, RAM GiB {ram_gib()}')
rows = []
for case in ('random', 'repetitive-nomatch', 'repetitive-allmatch'):
    for n, m in SIZES:
        rng = random.Random(f'{SEED}-{case}-{n}-{m}')
        text, pattern = make(case, n, m, rng)
        req = {'text': text, 'pattern': pattern}
        exp = oracle(text, pattern)
        outs = [A.naive(req)['positions'], A.kmp(req)['positions'], A.rk(req)['positions']]
        assert outs[0] == outs[1] == outs[2] == exp, 'outputs differ'
        for name, fn in (('naive', A.naive), ('kmp', A.kmp), ('rk', A.rk)):
            fn(req)
            t = [timed(fn, req) for _ in range(RUNS)]
            rows.append(f'|{case}|{n}|{m}|seed "{SEED}-{case}-{n}-{m}", random.Random|{name}|'
                        f'{t[0]:.3f}|{t[1]:.3f}|{t[2]:.3f}|{statistics.median(t):.3f}|'
                        f'yes: naive=kmp=rk=str.find oracle, {len(exp)} starts|')
header = ('|Case|n|m|Seed/generator|Algorithm|Run 1 (ms)|Run 2 (ms)|Run 3 (ms)|Median (ms)|Correct outputs checked|\n'
          '|---|---:|---:|---|---|---:|---:|---:|---:|---|')
report = f'Environment: {env}\n\n{header}\n' + '\n'.join(rows) + '\n'
print(report)
pathlib.Path(__file__).with_name('bench_results.md').write_text(report, encoding='utf-8')
