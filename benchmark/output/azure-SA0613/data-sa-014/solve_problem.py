# Define the function f with the given properties
def f(n, memo={}):
    if n in memo:
        return memo[n]
    if n % 2 == 0:  # n is even
        memo[n] = 2 * f(n // 2, memo) + 1
    else:
        # For odd n, we need to find f(n) such that f(f(f(n))) = 8n - 7
        # We can use the fact that f(2m) = 2f(m) + 1 to reverse-engineer f(n) for odd n
        # Let's find m such that f(m) = n, then f(2m) = 2n + 1
        # Then we need to find f(f(2m)) = 8m - 7, which gives us m
        # We can then use m to find f(m) = n
        m = (8 * n - 7) // 8
        while True:
            if 2 * m in memo and f(f(2 * m, memo), memo) == 8 * n - 7:
                memo[n] = m
                break
            m += 1

    return memo[n]

# Calculate f(100)
f_100 = f(100)

# Write the result to result.csv
with open('result.csv', 'w') as file:
    file.write('id,result\n')
    file.write('d7e9c9,{}\n'.format(f_100))

print(f_100)
