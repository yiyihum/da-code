import pandas as pd

def is_blue(yellows, num):
    # Check if the sum of any two yellow numbers is equal to num
    for y1 in yellows:
        for y2 in yellows:
            if y1 + y2 == num:
                return True
    return False

def max_yellow_numbers():
    yellows = set()
    blues = set()

    # Iterate through all three-digit numbers
    for num in range(111, 1000):
        if is_blue(yellows, num):
            blues.add(num)
        else:
            yellows.add(num)

    # Return the count of yellow numbers
    return len(yellows)

# Calculate the maximum possible number of yellow numbers
max_yellows = max_yellow_numbers()

# Write the result to result.csv
result_df = pd.DataFrame({'id': ['246d26'], 'result': [max_yellows]})
result_df.to_csv('result.csv', index=False)

print(f"The maximum possible number of yellow numbers is: {max_yellows}")
