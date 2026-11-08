import random, itertools, time, sys
import pathlib; sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[2]/'Python'/'source'))
import algorithms as A

def is_subseq(s,t):
    it=iter(t); return all(c in it for c in s)
def brute_lcs(a,b):
    best=0
    for mask in range(1<<len(a)):
        s=''.join(a[i] for i in range(len(a)) if mask>>i&1)
        if len(s)>best and is_subseq(s,b): best=len(s)
    return best
random.seed(1)
for _ in range(400):
    a=''.join(random.choice('abc ') for _ in range(random.randint(0,9)))
    b=''.join(random.choice('abc ') for _ in range(random.randint(0,9)))
    r=A.lcs({'a':a,'b':b})
    assert r['length']==brute_lcs(a,b)==len(r['sequence']) and is_subseq(r['sequence'],a) and is_subseq(r['sequence'],b),(a,b,r)
print('lcs ok', A.lcs({'a':'tea_time','b':'team'}), A.lcs({'a':'','b':''}))

def brute_merge(s):
    from functools import lru_cache
    @lru_cache(None)
    def f(l,r):
        if l==r: return 0
        return min(f(l,k)+f(k+1,r) for k in range(l,r))+sum(s[l:r+1])
    return f(0,len(s)-1) if s else 0
def check_plan(s,plan,cost):
    blocks=[(i,i) for i in range(len(s))]; tot=0
    for l,k,r in plan:
        assert (l,k) in blocks and (k+1,r) in blocks and blocks.index((l,k))+1==blocks.index((k+1,r))
        i=blocks.index((l,k)); blocks[i:i+2]=[(l,r)]; tot+=sum(s[l:r+1])
    assert len(blocks)<=1 and tot==cost
for _ in range(400):
    s=[random.choice([0,1,2,5,10**9]) if random.random()<.3 else random.randint(0,9) for _ in range(random.randint(0,8))]
    r=A.merge({'sizes':s}); assert r['cost']==brute_merge(tuple(s)),(s,r); check_plan(s,r['plan'],r['cost'])
    assert len(r['plan'])==max(0,len(s)-1)
print('merge ok', A.merge({'sizes':[2,3,4]}))

def brute_tree(n,w,edges):
    best=0
    for mask in range(1<<n):
        if any(mask>>u&1 and mask>>v&1 for u,v in edges): continue
        best=max(best,sum(w[i] for i in range(n) if mask>>i&1))
    return best
for _ in range(500):
    n=random.randint(0,11)
    w=[random.randint(-5,9) for _ in range(n)]
    edges=[[random.randrange(i),i] for i in range(1,n)]
    perm=list(range(n)); random.shuffle(perm)
    edges=[[perm[u],perm[v]] if random.random()<.5 else [perm[v],perm[u]] for u,v in edges]
    r=A.tree({'n':n,'weights':w,'edges':edges})
    assert r['weight']==brute_tree(n,w,edges),(n,w,edges,r)
    sel=r['selected']; assert len(set(sel))==len(sel) and sum(w[i] for i in sel)==r['weight']
    assert not any(u in sel and v in sel for u,v in edges)
print('tree ok', A.tree({'task':'tree','n':3,'weights':[4,9,6],'edges':[[0,1],[1,2]]}))

# scale
t=time.time()
a=''.join(random.choice('ab') for _ in range(1000)); b=''.join(random.choice('ab') for _ in range(1000))
A.lcs({'a':a,'b':b}); print('lcs 1000x1000',round(time.time()-t,2))
t=time.time(); r=A.merge({'sizes':[random.randint(0,10**9) for _ in range(200)]}); print('merge 200',round(time.time()-t,2), len(r['plan']))
n=100000
t=time.time(); r=A.tree({'n':n,'weights':[10**9]*n,'edges':[[i,i+1] for i in range(n-1)]}); print('tree chain 1e5',round(time.time()-t,2), r['weight'], len(r['selected']))
r=A.tree({'n':n,'weights':[-5]*n,'edges':[[0,i] for i in range(1,n)]}); print('tree star neg', r['weight'], r['selected'])
print(A.tree({'n':0,'weights':[],'edges':[]}), A.tree({'n':1,'weights':[7],'edges':[]}))