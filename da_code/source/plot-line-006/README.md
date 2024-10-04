
## About Dataset

### Context

This dataset was created to provide a comprehensive and easy-to-read list of international football matches, which was not readily available. The collection includes detailed results for various matches for reference and analysis.

### Content

This dataset contains **47,126** results of international football matches from the first official match in 1872 up to 2024. The matches range from FIFA World Cup to FIFI Wild Cup to regular friendly matches. The dataset strictly includes men's full internationals and excludes Olympic Games or matches involving a nation's B-team, U-23, or league select teams.

`results.csv` includes the following columns:

* `date` - Date of the match
* `home_team` - Name of the home team
* `away_team` - Name of the away team
* `home_score` - Full-time home team score, including extra time but excluding penalty shootouts
* `away_score` - Full-time away team score, including extra time but excluding penalty shootouts
* `tournament` - Name of the tournament
* `city` - City where the match was played
* `country` - Country where the match was played
* `neutral` - TRUE/FALSE indicating whether the match was played at a neutral venue

`shootouts.csv` includes the following columns:

* `date` - Date of the match
* `home_team` - Name of the home team
* `away_team` - Name of the away team
* `winner` - Winner of the penalty shootout
* `first_shooter` - Team that went first in the shootout

`goalscorers.csv` includes the following columns:

* `date` - Date of the match
* `home_team` - Name of the home team
* `away_team` - Name of the away team
* `team` - Name of the team scoring the goal
* `scorer` - Name of the player scoring the goal
* `own_goal` - Indicates if the goal was an own-goal
* `penalty` - Indicates if the goal was a penalty

Note on team and country names: The current name of the team is used for home and away teams. For instance, the team known as Ireland in 1882 is referred to as Northern Ireland in this dataset because the current team of Northern Ireland is the successor of the 1882 Ireland team. This allows easier tracking of teams' histories and statistics.

For country names, the name at the time of the match is used. For example, when Ghana played in Accra, Gold Coast in the 1950s, it is considered a home match for Ghana, even though the country name at that time was Gold Coast. This is indicated by the `neutral` column, which states FALSE for those matches, meaning they were not at a neutral venue.

### Acknowledgements

The data is gathered from several sources, including Wikipedia, rsssf.com, and individual football associations' websites.

### Inspiration

Possible directions for exploring the data:

* Determining the best team of all time
* Analyzing which teams dominated different eras of football
* Identifying trends in international football, such as home advantage, total goals scored, and distribution of teams' strengths
* Exploring the impact of geopolitics on football fixtures, including changes in the number of countries and preferred matchups
* Identifying countries that host the most matches without their own participation
* Assessing the impact of hosting major tournaments on a country's performance
* Investigating the most active teams in playing friendlies and friendly tournaments, and the impact on their performance

The dataset provides numerous opportunities for analysis and insights into international football.
