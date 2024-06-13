from math import factorial

def nCr(n, r):
    return factorial(n) // (factorial(r) * factorial(n - r))

def count_ways_to_sum(sum_of_digits, length):
    # We need to distribute 'sum_of_digits' into 'length' parts where each part can be 0 to 9
    # This is a problem of distributing 'sum_of_digits' indistinguishable items into 'length' distinguishable bins
    # with each bin having a maximum capacity of 9 (since each digit can't be more than 9)
    ways = 0
    for i in range((sum_of_digits // 10) + 1):
        # i is the number of bins that are filled to capacity (with 10)
        # We need to distribute the remaining sum_of_digits - 10*i into the remaining bins
        remaining_sum = sum_of_digits - 10 * i
        remaining_bins = length - i
        if remaining_bins < 0 or remaining_sum < 0:
            continue
        # Calculate the number of ways using stars and bars method
        # We add 1 to remaining_bins because we need to choose remaining_bins - 1 "bars" positions out of remaining_sum + remaining_bins - 1 positions
        ways += (-1)**i * nCr(length, i) * nCr(remaining_sum + remaining_bins - 1, remaining_bins - 1)
    return ways

# Calculate the number of special numbers
special_numbers_count = 0
for sum_of_digits in range(1, 6):
    for length in range(1, 37):  # Number of digits
        special_numbers_count += count_ways_to_sum(sum_of_digits, length)

# Write the result to result.csv
with open('result.csv', 'w') as file:
    file.write('id,answer\n')
    file.write('2fc4ad,{}\n'.format(special_numbers_count))
