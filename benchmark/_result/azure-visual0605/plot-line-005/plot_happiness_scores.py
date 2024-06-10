import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define the regions and their abbreviations as provided in Region.md
regions = {
    "Australia and New Zealand": "ANZ",
    "North America": "NA",
    "Western Europe": "WEU",
    "Latin America and Caribbean": "LAC",
    "Eastern Asia": "EA",
    "Southeastern Asia": "SEA",
    "Central and Eastern Europe": "CEE",
    "Middle East and Northern Africa": "MENA",
    "Southern Asia": "SA",
    "Sub-Saharan Africa": "SSA"
}

# Initialize a dictionary to hold the average happiness scores for each region
average_scores = {abbr: [] for abbr in regions.values()}

# Create a mapping of countries to regions using the 2016 data
country_region_mapping = pd.read_csv("2016.csv")[['Country', 'Region']].set_index('Country').to_dict()['Region']

# Process the CSV files for the years 2015 to 2019
for year in range(2015, 2020):
    # Read the CSV file for the current year
    if year < 2018:
        df = pd.read_csv(f"{year}.csv")
    else:
        df = pd.read_csv(f"{year}.csv").rename(columns={'Score': 'Happiness Score', 'Country or region': 'Country'})
        df['Region'] = df['Country'].apply(lambda x: country_region_mapping.get(x))

    # In 2017, the column names changed, so we need to handle that
    if year == 2017:
        df.rename(columns={'Happiness.Score': 'Happiness Score', 'Happiness.Rank': 'Happiness Rank'}, inplace=True)
    
    # Calculate the average happiness score for each region
    for region, abbr in regions.items():
        if 'Region' in df.columns:
            region_df = df[df['Region'] == region]
            average_score = region_df['Happiness Score'].mean()
        else:
            average_score = np.nan
        average_scores[abbr].append(average_score)

# Plot the line graph
plt.figure(figsize=(12, 6))
for abbr, scores in average_scores.items():
    # Replace NaN values with None for plotting
    scores = [score if not np.isnan(score) else None for score in scores]
    plt.plot(range(2015, 2020), scores, label=abbr)

plt.title("Happiness Scores in 2015-2019")
plt.xlabel("Year")
plt.ylabel("Average Happiness Score")
plt.legend()
plt.savefig("result.png")
