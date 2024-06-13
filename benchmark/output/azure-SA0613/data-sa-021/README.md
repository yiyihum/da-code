### Question

How to analyze and calculate the relationship between the input voltage \( v_{in} \) and the output voltage \( v_{out} \) of an inverting amplifier circuit, and derive the relevant formulas and examples of practical applications using the characteristics of an ideal operational amplifier?

The purpose of this Jupyter notebook is to explain and analyze the working principle of an inverting amplifier circuit. Specific contents include:

1. **Characteristics of an Ideal Operational Amplifier**:

- Two basic rules:

1. No current flows into either input terminal.

2. There is no voltage difference between the two input terminals.

- The behavior of an ideal operational amplifier and its approximation in practical applications are explained through diagrams and explanations.

2. **Inverting Amplifier Circuit**:

- A schematic diagram of an inverting amplifier circuit is provided.


3. **Example**:
- Given a specific input voltage \( v_{in} = 5 \sin(3t) \) mV, resistance \( R_1 = 4.7 \) kΩ and \( R_f = 47 \) kΩ, further calculate the output voltage by substituting these values.
# Calculate the input voltage and output voltage at specific time points
time_points = [0, 1, 2, 3, 4, 5] # For example: t = 0, 1, 2, 3, 4, 5 seconds