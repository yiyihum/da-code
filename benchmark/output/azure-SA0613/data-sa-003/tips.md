The weather column contains different groups, weather (

1: clear, few clouds, partly cloudy, partly cloudy

2: fog + cloudy, fog + broken clouds, fog + few clouds, fog

3: light snow, light rain + thunderstorm + scattered clouds, light rain + scattered clouds

4: heavy rain + hail + thunderstorm + fog, snow + fog

)
Perform `Kruskal-Wallis test`, if p value > 0.05 -> fail to reject the null hypothesis, and p value < 0.05 reject the null hypothesis. Fill the results in `weather.csv` in the given format.

## weather.csv Output result format

```
Test Type: Test type, specifically "Non Parametric".
Kruskal Statistic: Kruskal-Wallis test statistic.
P-Value: P value of the test result.
Hypothesis: Whether to reject the null hypothesis, the value is "Strong Evidence to Reject Null Hypothesis" or "No Evidence to Reject Null Hypothesis".
Comment: Comments on the results, the value is "Different distributions" or "No evidence of different distributions".
```
