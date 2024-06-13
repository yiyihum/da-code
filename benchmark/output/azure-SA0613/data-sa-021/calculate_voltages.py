import csv
import math

# Given values
R1 = 4.7e3  # Resistance R1 in ohms
Rf = 47e3   # Resistance Rf in ohms
time_points = [0, 1, 2, 3, 4, 5]  # Time points in seconds

# Function to calculate v_in
def calculate_vin(t):
    return 5 * math.sin(3 * t)

# Function to calculate v_out
def calculate_vout(vin, R1, Rf):
    return -(Rf / R1) * vin

# Calculate voltages and write to CSV
with open('/workspace/inverting_amplifier_output.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['Time (s)', 'Input Voltage (mV)', 'Output Voltage (mV)'])
    
    # Write the data
    for t in time_points:
        vin = calculate_vin(t)
        vout = calculate_vout(vin, R1, Rf)
        writer.writerow([t, vin, vout])

print("Calculation and CSV writing completed.")
