# Define the function f with the given properties
def f(n):
    # Initialize a dictionary to store computed values of f
    computed_values = {1: 1}  # Base case: f(1) must be 1

    # Compute f(n) for n up to 100 using the given properties
    for i in range(2, 101):
        if i % 2 == 0:  # n is even
            computed_values[i] = 2 * computed_values[i // 2] + 1
        else:
            # For odd n, we need to find f(n) such that f(f(f(n))) = 8n - 7
            # We can use the fact that f(2m) = 2f(m) + 1 to reverse-engineer f(n) for odd n
            # Let's find m such that f(m) = n, then f(2m) = 2n + 1
            # Then we need to find f(f(2m)) = 8m - 7, which gives us m
            # We can then use m to find f(m) = n
            m = (8 * i - 7) // 8
            while True:
                if 2 * m in computed_values and computed_values[2 * m] == 2 * n + 1:
                    computed_values[i] = m
                    break
                m += 1

    return computed_values[100]

# Calculate f(100)
f_100 = f(100)

# Write the result to result.csv
with open('result.csv', 'w') as file:
    file.write('id,result\n')
    file.write('d7e9c9,{}\n'.format(f_100))

print(f_100)
