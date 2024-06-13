import math

def is_divisible_by(base, divisor):
    """Check if base squared is exactly divisible by divisor."""
    if divisor == 0:  # Avoid division by zero
        return False
    return (base**2 // divisor) * divisor == base**2

def is_perfect_square(number):
    """Check if a number is a perfect square."""
    root = math.isqrt(number)  # Integer square root of the number
    return root * root == number

def find_values():
    min_value, max_value = 10, 100
    
    for third_value in range(min_value, max_value):
        for first_value in range(min_value, third_value):
            if is_divisible_by(third_value, first_value):
                fifth_value = third_value**2 // first_value
                if fifth_value < max_value:
                    forth_value_square = third_value * fifth_value
                    second_value_square = third_value * first_value
                    if is_perfect_square(forth_value_square) and is_perfect_square(second_value_square):
                        second_value = math.isqrt(second_value_square)
                        forth_value = math.isqrt(forth_value_square)
                        # Print the values
                        return [first_value, second_value, third_value, forth_value, fifth_value]

answer_list = find_values()
answer = sum(answer_list)
print(f"answer = {answer}")