### Summons Number
- **Description:** Unique identifier for each parking violation.
- **Data Type:** Numeric
- **Constraint:** The length of the violation_location value must be 4 characters.

### Plate ID
- **Description:** License plate identifier of the vehicle.
- **Data Type:** Alphanumeric
- **Constraint:** ---\d{4}$

### Registration State
- **Description:** State where the vehicle is registered.
- **Data Type:** Alphabetic (State abbreviation)
- **Constraint:** US State Abbreviations

### Plate Type
- **Description:** Type of license plate.
- **Data Type:** Alphanumeric
- **Constraint:** [PAS, SAF]

### Issue Date
- **Description:** Date when the parking violation was issued.
- **Data Type:** Date (YYYY-MM-DD)
- **Constraint:** MM/DD/YYYY

### Violation Code
- **Description:** Code indicating the type of parking violation.
- **Data Type:** Numeric
- **Constraint:** ^[1-9][0-9]$

### Vehicle Body Type
- **Description:** Type of vehicle body.
- **Data Type:** Alphabetic
- **Constraint:** All P-U (pick-up truck) values in the vehicle_body_type column should use a general TRK value.  Replace NULL values with the string Unknown.

### Vehicle Make
- **Description:** Make or manufacturer of the vehicle.
- **Data Type:** Alphabetic
- **Constraint:** ^[A-Z]$

### Issuing Agency
- **Description:** Agency that issued the parking violation.
- **Data Type:** Alphabetic

### Street Code1, Street Code2, Street Code3
- **Description:** Codes representing street information.
- **Data Type:** Alphanumeric
- **Constraint** \d{5}

### Vehicle Expiration Date
- **Description:** Expiration date of the vehicle registration.
- **Data Type:** Date (YYYY-MM-DD)
- **Constraint:** \d{2}/\d{2}/\d{4}

### Violation Location
- **Description:** Location where the violation occurred.
- **Data Type:** Alphanumeric
- **Constraint:** \d+

### Violation Precinct
- **Description:** Precinct associated with the violation.
- **Data Type:** Numeric
- **Constraint:** \d+

### Issuer Precinct
- **Description:** Precinct of the issuing officer.
- **Data Type:** Numeric

### Issuer Code
- **Description:** Code associated with the issuing officer.
- **Data Type:** Numeric

### Issuer Command
- **Description:** Command of the issuing officer.
- **Data Type:** Alphanumeric

### Issuer Squad
- **Description:** Squad of the issuing officer.
- **Data Type:** Alphanumeric

### Violation Time
- **Description:** Time when the violation occurred.
- **Data Type:** HH:MM AM/PM

### Time First Observed
- **Description:** Time when the violation was first observed.
- **Data Type:** HH:MM AM/PM

### Violation County
- **Description:** County where the violation occurred.
- **Data Type:** Alphabetic

### Violation In Front Of Or Opposite
- **Description:** Indicates if the violation occurred in front of or opposite a location.
- **Data Type:** Alphabetic

### House Number
- **Description:** House number associated with the violation.
- **Data Type:** Alphanumeric

### Street Name
- **Description:** Name of the street where the violation occurred.
- **Data Type:** Alphanumeric

### Intersecting Street
- **Description:** Name of the intersecting street.
- **Data Type:** Alphanumeric

### Date First Observed
- **Description:** Date when the violation was first observed.
- **Data Type:** Date (YYYY-MM-DD)

### Law Section
- **Description:** Section of the law associated with the violation.
- **Data Type:** Alphanumeric

### Sub Division
- **Description:** Subdivision related to the violation.
- **Data Type:** Alphanumeric

### Violation Legal Code
- **Description:** Legal code associated with the violation.
- **Data Type:** Alphanumeric

### Days Parking In Effect
- **Description:** Days of the week when parking regulations are in effect.
- **Data Type:** Alphabetic (e.g., "Mon, Tue, Wed")

### From Hours In Effect, To Hours In Effect
- **Description:** Time range when parking regulations are in effect.
- **Data Type:** HH:MM AM/PM

### Vehicle Color
- **Description:** Color of the vehicle.
- **Data Type:** Alphabetic
- **Constraint:** Unified color expression, such as GRAY, GREY, GRAY are all GRAY.


### Unregistered Vehicle?
- **Description:** Indicates if the vehicle is unregistered.
- **Data Type:** Boolean (Yes/No)

### Vehicle Year
- **Description:** Year of the vehicle.
- **Data Type:** Numeric

### Meter Number
- **Description:** Number associated with parking meter.
- **Data Type:** Alphanumeric

### Feet From Curb
- **Description:** Distance of the vehicle from the curb.
- **Data Type:** Numeric

### Violation Post Code
- **Description:** Postal code associated with the violation.
- **Data Type:** Alphanumeric

### Violation Description
- **Description:** Description of the parking violation.
- **Data Type:** Alphanumeric

### No Standing or Stopping Violation, Hydrant Violation, Double Parking Violation
- **Description:** Flags indicating specific types of violations.
- **Data Type:** Boolean (Yes/No)

