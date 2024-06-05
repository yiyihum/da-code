import numpy as np

hyp_np = np.array(
    [
        [1, 2],
        [4, 3],
        [5, 2],
        [1, 3]
    ]
)

hyp_np = np.sort(hyp_np, axis=0).reshape(hyp_np.shape)
print(hyp_np)
print(hyp_np[1])