from inspect import signature

def example_func(a, b, c=3, d=4, *args, **kwargs):
    return a + b + c + d

func_sig = signature(example_func)
print("Function Signature:", func_sig)
args = (2, 1,4,5,10)
kwargs = {'e': 6}
params = func_sig.bind(*args, **kwargs)
print("Bound Arguments (before applying defaults):", params.arguments)
params.apply_defaults()

print("Bound Arguments (after applying defaults):", params.arguments)

print(type(params.arguments))
result = example_func(*params.args, **params.kwargs)
print("Result:", result)