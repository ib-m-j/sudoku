import itertools

a=[[1,2]]
b=[[3,4]]
print(a+b)


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(1,len(s)+1))


for x in itertools.combinations([1,2,3],2):
    print(x)

y = itertools.chain.from_iterable(itertools.combinations([1,2,3],2))
print(y)

a = [ d for d in powerset([1,2,3])]
print(a)

for z in powerset([1,2,3]):
    print(set(z))

for p in itertools.chain('abc', 'def', 'gghi'):
    print(p)
