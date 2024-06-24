
## About Dataset

### Context

The dataset comprises experimental data used for creating regression models to predict appliances' energy use in a low-energy building.

### Content

The data is recorded at 10-minute intervals over a period of approximately 4.5 months. Temperature and humidity within the house were monitored using a ZigBee wireless sensor network, with each node transmitting data every 3.3 minutes. The wireless data was averaged over 10-minute periods. Energy consumption data was logged every 10 minutes using m-bus energy meters. Weather data from the nearest airport weather station (Chievres Airport, Belgium) was obtained from a public dataset and merged with the experimental data based on date and time columns. Two random variables were included for testing regression models and filtering out non-predictive attributes.

### Acknowledgements

Luis Candanedo, luismiguel.candanedoibarra '@' umons.ac.be, University of Mons (UMONS)

Luis M. Candanedo, Veronique Feldheim, Dominique Deramaix, Data driven prediction models of energy use of appliances in a low-energy house, Energy and Buildings, Volume 140, 1 April 2017, Pages 81-97, ISSN 0378-7788.

### Inspiration

The dataset includes measurements from temperature and humidity sensors in a wireless network, weather data from a nearby airport station, and recorded energy consumption of appliances. The process involves filtering data to remove non-predictive parameters and ranking features to enhance model accuracy. Various statistical models can be developed using this dataset.

Key Points:

- Prediction of appliances' energy consumption in a low-energy house.
- Weather data significantly improves prediction accuracy.
- Parameters like pressure, air temperature, and wind speed are crucial for predictions.
- Data from specific areas within the house (kitchen, laundry, living room) are particularly important.
