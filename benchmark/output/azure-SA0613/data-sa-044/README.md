## The dataset

| Column                | Description                                                  |
| --------------------- | ------------------------------------------------------------ |
| `id`                  | Unique client identifier                                     |
| `age`                 | Client's age: `0`: 16-15`1`: 26-39`2`: 40-64`3`: 65+         |
| `gender`              | Client's gender: `0`: Female`1`: Male                        |
| `driving_experience`  | Years the client has been driving: `0`: 0-9`1`: 10-19`2`: 20-29`3`: 30+ |
| `education`           | Client's level of education: `0`: No education`1`: High school`2`: University |
| `income`              | Client's income level: `0`: Poverty`1`: Working class`2`: Middle class`3`: Upper class |
| `credit_score`        | Client's credit score (between zero and one)                 |
| `vehicle_ownership`   | Client's vehicle ownership status: `0`: Does not own their vehilce (paying off finance)`1`: Owns their vehicle |
| `vehcile_year`        | Year of vehicle registration: `0`: Before 2015`1`: 2015 or later |
| `married`             | Client's marital status: `0`: Not married`1`: Married        |
| `children`            | Client's number of children                                  |
| `postal_code`         | Client's postal code                                         |
| `annual_mileage`      | Number of miles driven by the client each year               |
| `vehicle_type`        | Type of car: `0`: Sedan`1`: Sports car                       |
| `speeding_violations` | Total number of speeding violations received by the client   |
| `duis`                | Number of times the client has been caught driving under the influence of alcohol |
| `past_accidents`      | Total number of previous accidents the client has been involved in |
| `outcome`             | Whether the client made a claim on their car insurance (response variable): `0`: No claim`1`: Made a claim |