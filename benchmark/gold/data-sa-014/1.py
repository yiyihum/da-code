def compute_f_third(n):
    return 8 * n - 7

def compute_f(n, memo, memo_third_reverse):
    if n in memo:
        return memo[n]

    if n % 2 == 0:
        value = 2 * compute_f(n // 2, memo, memo_third_reverse) + 1
    elif n in memo_third_reverse:
        value = compute_f(memo_third_reverse[n], memo, memo_third_reverse)
        if value != -1:
            value = compute_f_third(value)
    else:
        value = -1  # or not exists

    if value > 0:
        memo[n] = value
        
    return value


def create_memo(n):
    memo = {1:1}
    value = 1
    while value < n:
        new_value = 2*value
        memo[new_value] = 2*memo[value] + 1
        value = new_value
    return memo

def create_memo_third_reverse(n, compute_f_third):
    memo_third_reverse = {1:1}
    value = 1
    while value < n:
        new_value = value + 1
        y = compute_f_third(new_value)
        memo_third_reverse[y] = new_value
        value = new_value
    return memo_third_reverse


# Assumption f(1) = 1

n = 100
memo = create_memo(n)
memo_third_reverse = create_memo_third_reverse(n, compute_f_third)

answer = compute_f(100, memo, memo_third_reverse)

print(f"answer = {answer}")