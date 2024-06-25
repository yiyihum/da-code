# Permit Data Schema

This document describes the schema for the permit data table, including details about each column's name, description, and data type.

## Table: Permits

This table contains information about permits including details like permit number, type, status, dates, cost, and location.

### Columns

- **Permit Number**
  - **Description**: The unique identifier for the permit.
  - **Data Type**: integer

- **Permit Type**
  - **Description**: The type of permit issued.
  - **Data Type**: integer

- **Permit Type Definition**
  - **Description**: Description of the permit type.
  - **Data Type**: string

- **Permit Creation Date**
  - **Description**: The date the permit was created.
  - **Data Type**: date

- **Block**
  - **Description**: The block number where the permit is issued.
  - **Data Type**: string

- **Lot**
  - **Description**: The lot number where the permit is issued.
  - **Data Type**: string

- **Street Number**
  - **Description**: The street number of the location where the permit is issued.
  - **Data Type**: string

- **Street Number Suffix**
  - **Description**: The suffix for the street number.
  - **Data Type**: string

- **Street Name**
  - **Description**: The name of the street where the permit is issued.
  - **Data Type**: string

- **Street Suffix**
  - **Description**: The suffix for the street name (e.g., St, Ave).
  - **Data Type**: string

- **Unit**
  - **Description**: The unit number of the location.
  - **Data Type**: string

- **Unit Suffix**
  - **Description**: The suffix for the unit number.
  - **Data Type**: string

- **Description**
  - **Description**: A detailed description of the permit.
  - **Data Type**: string

- **Current Status**
  - **Description**: The current status of the permit.
  - **Data Type**: string

- **Current Status Date**
  - **Description**: The date when the current status was recorded.
  - **Data Type**: date

- **Filed Date**
  - **Description**: The date when the permit was filed.
  - **Data Type**: date

- **Issued Date**
  - **Description**: The date when the permit was issued.
  - **Data Type**: date

- **Completed Date**
  - **Description**: The date when the work was completed.
  - **Data Type**: date

- **First Construction Document Date**
  - **Description**: The date of the first construction document.
  - **Data Type**: date

- **Structural Notification**
  - **Description**: Notification related to structural changes.
  - **Data Type**: boolean

- **Number of Existing Stories**
  - **Description**: The number of existing stories in the building.
  - **Data Type**: integer

- **Number of Proposed Stories**
  - **Description**: The number of proposed stories in the building.
  - **Data Type**: integer

- **Fire Only Permit**
  - **Description**: Indicates if the permit is for fire-related work only.
  - **Data Type**: boolean

- **Permit Expiration Date**
  - **Description**: The date when the permit expires.
  - **Data Type**: date

- **Estimated Cost**
  - **Description**: The estimated cost of the work.
  - **Data Type**: float

- **Revised Cost**
  - **Description**: The revised cost of the work.
  - **Data Type**: float

- **Existing Use**
  - **Description**: The existing use of the building.
  - **Data Type**: string

- **Existing Units**
  - **Description**: The number of existing units in the building.
  - **Data Type**: integer

- **Proposed Use**
  - **Description**: The proposed use of the building.
  - **Data Type**: string

- **Proposed Units**
  - **Description**: The number of proposed units in the building.
  - **Data Type**: integer

- **Plansets**
  - **Description**: The number of plansets submitted.
  - **Data Type**: integer


- **Existing Construction Type**
  - **Description**: The type of existing construction.
  - **Data Type**: string

- **Existing Construction Type Description**
  - **Description**: Description of the existing construction type.
  - **Data Type**: string

- **Proposed Construction Type**
  - **Description**: The type of proposed construction.
  - **Data Type**: string

- **Proposed Construction Type Description**
  - **Description**: Description of the proposed construction type.
  - **Data Type**: string

- **Site Permit**
  - **Description**: Indicates if it is a site permit.
  - **Data Type**: boolean

- **Supervisor District**
  - **Description**: The supervisor district where the permit is issued.
  - **Data Type**: integer

- **Neighborhoods - Analysis Boundaries**
  - **Description**: The neighborhood where the permit is issued.
  - **Data Type**: string

- **Zipcode**
  - **Description**: The zipcode of the permit location.
  - **Data Type**: string

- **Location**
  - **Description**: The geographic location coordinates.
  - **Data Type**: string

- **Record ID**
  - **Description**: The unique record identifier.
  - **Data Type**: string
