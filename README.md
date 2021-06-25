# Exploring the Vax Potential

Real-Time Dashboard for Virginia COVID-19 Report and Vaccination

Metis engineering project

## Abstract

The goal of this project built an end-to-end data storage and processing pipeline that created a dashboard to visualize Virginia COVID-19 case reports and vaccinations with real-time data. The impact of this project is to provide a user-friendly interactive dashboard that allows users to visualize both real-time COVID-19 case reports and vaccinations. The pipeline created was able to collect data from API, store data in SQL database and preprocess data, and was automated with cron job for real-time data. The data were then used to build a Dash dashboard app. The web app dashboard consists of two main components: **State overview** and **County summary**. The dashboard is live and can be view [here](https://vaxcovid.herokuapp.com/).

## Design

As the Delta variant of COVID-19 spread looming over US, CDC and healthcare experts are warning poorly vaccinated regions to be prepared for the renewed danger. Upon researching for my current state Virginia's status, I realized there are mostly cases surveillance dashboard. Although there are a few vaccination dashboard, they are separated from the cases surveillance, which can be inconvinient for users if they want to explore the relationship between cases and vaccinations. 

So the goal of this project is to **build a pipeline for a dashboard to visualize Viriginia COVID-19 case reports and vaccinations with real-time data.**

## Data

* The Virginia [Vaccine Administered dataset](https://data.virginia.gov/dataset/VDH-COVID-19-PublicUseDataset-Vaccines-DosesAdmini/28k2-x2rj) (267,000 data points) and [COVID cases dataset](https://data.virginia.gov/Government/VDH-COVID-19-PublicUseDataset-Cases/bre9-aqqr) (60,600 data points) from Virginia Open Data. The data are updated every day so the database is constantly growing.
* Cense data for Virginia counties population

## Methodology

#### Data Engineering Workflow:

| Purpose                 | Connects        | Main script                                                  | Function libary                                              |
| ----------------------- | --------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Update content database | API -> Database | [preprocess_data.py](https://github.com/crystal-ctrl/engineering_project/blob/main/preprocess_data.py) | [collect_data.py](https://github.com/crystal-ctrl/engineering_project/blob/main/collect_data.py) |
| Launch Dash app         | Database -> App | [index.py](https://github.com/crystal-ctrl/engineering_project/blob/main/index.py) | [app.py](https://github.com/crystal-ctrl/engineering_project/blob/main/app.py)<br />[state.py](https://github.com/crystal-ctrl/engineering_project/blob/main/apps/state.py)<br />[county.py](https://github.com/crystal-ctrl/engineering_project/blob/main/apps/county.py) |
| Deploy app on Heroku    | App -> Web      | [Procfile](https://github.com/crystal-ctrl/engineering_project/blob/main/Procfile) | [requirements.txt](https://github.com/crystal-ctrl/engineering_project/blob/main/requirements.txt) |

- API calling daily to update the dashboard with cron job

#### Data Visualization & Application Production:

- Plotly, Dash

![](https://github.com/crystal-ctrl/engineering_project/blob/main/dashboard.png)

* Deployed the Dash app on Heroku

## Techonologies

- SODA API
- SQL, sqlachemy
- Python(pandas,numpy)
- Dash
- Heroku

## Communications

In addition to the [presentation slides](https://github.com/crystal-ctrl/engineering_project/blob/main/Presentation.pdf), you can check out the app [here](https://vaxcovid.herokuapp.com/).

Notebooks can be found [here](https://github.com/crystal-ctrl/engineering_project/tree/main/Notebooks).

