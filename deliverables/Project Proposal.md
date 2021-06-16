# Project Proposal

#### Question/need:

- **What is the framing question of your analysis, or the purpose of the model/system you plan to build?**

  Is there a relationship between the vaccine administered count and COVID case number in Viriginia, US?

- **Who benefits from exploring this question or building this model/system?**

  Virginia Department of Health, general public, medical experts

#### Data Description:

- **What dataset(s) do you plan to use, and how will you obtain the data?**

  The datasets I will be using are the Virginia [Vaccine Administered dataset](https://data.virginia.gov/dataset/VDH-COVID-19-PublicUseDataset-Vaccines-DosesAdmini/28k2-x2rj) (252,000 data points) and [COVID cases dataset](https://data.virginia.gov/Government/VDH-COVID-19-PublicUseDataset-Cases/bre9-aqqr) (60,600 data points) from Virginia Open Data. The options to access these datasets are straightforward downloading the csv files as well as SODA API. I plan on using API to obtain the datasets so the datasets can be refreshed periodiotically in the future.

- **What is an individual sample/unit of analysis in this project? What characteristics/features do you expect to work with?**

  - <u>Vaccine dataset</u> - Each row represents the daily count of COVID-19 vaccine doses administered in Virginia by date of vaccine administration, locality, administering facility type, manufacturer, and dose number

    | Column names                     | Description                                |
    | -------------------------------- | ------------------------------------------ |
    | Administration Date              | Date when the vaccine dose is administered |
    | FIPS                             | 5-digit code for the locality              |
    | Locality                         | city or county in Viriginia                |
    | Health District                  | Health District name                       |
    | Facility Type                    | facility type of vaccine administration    |
    | Vaccine Manufacturer             | Moderna, Pfizer, or J&J                    |
    | Dose Number                      | 1st or 2nd dose                            |
    | Vaccine Doses Administered Count | total number of vaccine doses administered |

  - <u>Case dataset</u> - Each row represents the overall count of COVID-19 cases, hospitalizations, deaths for each locality in Virginia by report date since reporting began

    | Column names        | Description                            |
    | ------------------- | -------------------------------------- |
    | Report Date         | Date                                   |
    | FIPS                | 5-digit code for the locality          |
    | Locality            | city or county in Viriginia            |
    | VDH Health District | Health District name                   |
    | Total cases         | total number of COVID cases            |
    | Hospitalization     | total number of COVID hospitalizations |
    | Deaths              | total number of COVID deaths           |

- If modeling, what will you predict as your target?

  If there's a strong relationship between vaccine adminstered count and case count, I'll use vaccine count to predict case count.

#### Tools:

- SODA API - data acquisition
- SQL - data storage
- Matplotlib, seaborn for visualization
- Streamlit or Flask for application production
- Considering using scheduling tool that updates the datasets periodically

#### MVP Goal:

Priliminary Analysis on vaccine adminstered count and case/hospitalization/death counts in Virginia over time. 