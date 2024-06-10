import matplotlib.pyplot as plt

# Data for plotting
categories = [
    "cama_mesa_banho", "esporte_lazer", "moveis_decoracao", "beleza_saude",
    "utilidades_domesticas", "automotivo", "informatica_acessorios",
    "brinquedos", "relogios_presentes", "telefonia"
]
counts = [3029, 2867, 2657, 2444, 2335, 1900, 1639, 1411, 1329, 1134]

# Create bar chart
plt.figure(figsize=(12, 8))
plt.bar(categories, counts)
plt.title('Top 10 Product Categories by Count')
plt.xlabel('Product Category')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')  # Rotate labels to fit and align right

# Save the plot as a PNG file
plt.savefig('/workspace/result.png', bbox_inches='tight')
