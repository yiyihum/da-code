def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def sparkle(n):
    return factorial(sum(int(digit) for digit in str(n)))

def is_special(n):
    seen = set()
    while n not in seen:
        seen.add(n)
        n = sparkle(n)
        if n >= 6:
            return False
    return True

# Since the maximum sum of digits for a 36-digit number is 9*36 = 324,
# and 324! is an extremely large number, we can assume that any number
# with a sum of digits greater than or equal to 6 is not special.
# Therefore, we only need to check numbers with a sum of digits less than 6.

special_numbers_count = 0
for n in range(1, 10**36):
    if sum(int(digit) for digit in str(n)) < 6 and is_special(n):
        special_numbers_count += 1

# Write the result to result.csv
with open('result.csv', 'w') as file:
    file.write('id,answer\n')
    file.write('2fc4ad,{}\n'.format(special_numbers_count))
