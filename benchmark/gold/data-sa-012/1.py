import math

# Dynamic Programming
def count_numbers(n, s):
    # Initialize a 2D array to store the number of numbers with each sum and number of digits
    dp = [[0 for _ in range(s + 1)] for _ in range(n + 1)]
    
    # There is exactly one way to form a number with 0 digits and sum 0
    dp[0][0] = 1

    # Iterate over the number of digits
    for i in range(1, n + 1):
        # Iterate over the possible sums
        for sum_ in range(s + 1):
            # Iterate over the possible values of the current digit
            for digit in range(10):
                if sum_ >= digit:
                    dp[i][sum_] += dp[i - 1][sum_ - digit]

    return dp[n][s]

def sparkle(x):
    x = sum(int(i) for i in str(x))
    return math.factorial(x)


max_threshold = 6
total_digit = 36

first_items = []
for i in range(1, max_threshold+1):
    if math.factorial(i) >= max_threshold:
        break
    first_items.append(i)

special_items = []
for x in first_items:
    seen = set([x])
    next_x = x
    while next_x < max_threshold:
        next_x = sparkle(next_x)
        if next_x in seen:
            special_items.append(x)
            break
        seen.add(next_x)

answer = sum(count_numbers(total_digit, i) for i in special_items)

print(f"answer = {answer}")