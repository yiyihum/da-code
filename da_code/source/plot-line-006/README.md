## About Dataset

---

### Overview

This dataset provides comprehensive climate change data compiled by Berkeley Earth, affiliated with Lawrence Berkeley National Laboratory. It aggregates 1.6 billion temperature reports from 16 pre-existing archives, offering a well-packaged resource for analyzing long-term climate trends.

### Content

The dataset includes several files:

* **GlobalTemperatures.csv**:

  - Date: Starting from 1750 for average land temperature and 1850 for max and min land temperatures, global ocean, and land temperatures.
  - LandAverageTemperature: Global average land temperature in Celsius.
  - LandAverageTemperatureUncertainty: 95% confidence interval around the average land temperature.
  - LandMaxTemperature: Global average maximum land temperature in Celsius.
  - LandMaxTemperatureUncertainty: 95% confidence interval around the maximum land temperature.
  - LandMinTemperature: Global average minimum land temperature in Celsius.
  - LandMinTemperatureUncertainty: 95% confidence interval around the minimum land temperature.
  - LandAndOceanAverageTemperature: Global average land and ocean temperature in Celsius.
  - LandAndOceanAverageTemperatureUncertainty: 95% confidence interval around the global average land and ocean temperature.
* Other files:

  - GlobalLandTemperaturesByCountry.csv: Global average land temperature by country.
  - GlobalLandTemperaturesByState.csv: Global average land temperature by state.
  - GlobalLandTemperaturesByMajorCity.csv: Global land temperatures by major city.
  - GlobalLandTemperaturesByCity.csv: Global land temperatures by city.

The data sources and transformation methods are transparently documented, allowing for slicing the dataset into various subsets for detailed analysis.
