import json

# The calculated correlation results
correlation_results = {
    "Correlation between Population Density and Life Expectancy": [0.1511181717012949],
    "Correlation between Population Density and GDP": [0.015928539060090133]
}

# Save the output to a JSON file
output_file = '/workspace/correlation_results.json'
with open(output_file, 'w') as file:
    json.dump(correlation_results, file)

print(output_file)
