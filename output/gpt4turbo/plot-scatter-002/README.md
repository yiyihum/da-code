
# Data Science Jobs Salaries Dataset

## About Dataset

### Overview

This dataset comprises job postings and salary information related to data science roles in California, USA, sourced from SimplyHired. The dataset was scraped on 17 December 2021 and includes four CSV files. These files provide insights into job titles, companies, locations, salaries, qualifications, and benefits associated with data science positions.

### Contents

#### work_year

The year during which the salary was paid, categorized as either a specific year (e.g., 2020) or estimated (e.g., 2021e).

#### experience_level

The experience level of the job, classified as EN (Entry-level / Junior), MI (Mid-level / Intermediate), SE (Senior-level / Expert), or EX (Executive-level / Director).

#### employment_type

The type of employment for the role: PT (Part-time), FT (Full-time), CT (Contract), or FL (Freelance).

#### job_title

The specific role held during the year.

#### salary

The total gross salary amount paid.

#### salary_currency

The currency of the salary, represented as an ISO 4217 currency code.

#### salary_in_usd

The salary converted to USD, calculated using FX rates from fxdata.foorilla.com.

#### employee_residence

The primary country of residence of the employee during the work year, specified as an ISO 3166 country code.

#### remote_ratio

The percentage of work conducted remotely, categorized as 0 (No remote work), 50 (Partially remote), or 100 (Fully remote).

#### company_location

The country where the employer's main office or contracting branch is located, indicated by an ISO 3166 country code.

#### company_size

The average number of employees at the company during the year, categorized as S (less than 50 employees), M (50 to 250 employees), or L (more than 250 employees).

### Source and Acknowledgements

The dataset was obtained from SimplyHired and processed for analysis. The cleaning and scraping scripts used are available on GitHub for reference.

### Potential Uses

This dataset is valuable for tasks such as data cleaning exercises, exploratory data analysis, and building predictive models related to data science job trends and salaries in California.
