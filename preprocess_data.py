import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import collect_data
from functools import reduce

def preprocess_case_df():
    """
    Preprocess the case_data from sql db and output as a df
    """

    # Accessing data from database
    engine = create_engine('sqlite:///covid.db')
    df = pd.read_sql('SELECT c.*, p.Population FROM case_data c LEFT JOIN pop_data p ON c.locality=p.Locality;',
    engine)

    # change datatype
    df['report_date'] = pd.to_datetime(df.report_date)
    df['total_cases'] = df.total_cases.astype(int)
    df['hospitalizations'] = df.hospitalizations.astype(int)
    df['deaths'] = df.deaths.astype(int)
    df['Population'] = df.Population.astype(int)
    df.replace({'vdh_health_district':"Thomas Jefferson"}, "Blue Ridge", inplace=True)

    # add region
    central=["Chesterfield", "Crater", "Chickahominy","Henrico","Piedmont","Richmond","Southside"]
    eastern = ["Chesapeake", "Eastern Shore", "Hampton", "Norfolk", "Peninsula", "Portsmouth", "Three Rivers",
           "Virginia Beach", "Western Tidewater"]
    northern = ["Alexandria", "Arlington", "Fairfax", "Loudoun", "Prince William"]
    northwest = ["Central Shenandoah", "Lord Fairfax", "Rappahannock", "Rappahannock Rapidan", "Blue Ridge"]
    southwest = ["Alleghany", "Central Virginia", "Cumberland Plateau", "Lenowisco", "Mount Rogers", "New River",
            "Pittsylvania-Danville", "Roanoke", "West Piedmont"]
    region_dict = {"central": central,
                 "eastern": eastern,
                 "northern": northern,
                 "northwest": northwest,
                 "southwest": southwest}
    region_map = {val:key for key, lst in region_dict.items() for val in lst}
    df['region'] = df.vdh_health_district.map(region_map)

    # get daily new nums
    df.sort_values(['region','vdh_health_district', 'locality','report_date'],
              inplace=True,ascending=True,ignore_index=True)
    df[['prev_total_cases','prev_hosp','prev_deaths']] = (df
                                                        .groupby(['region','vdh_health_district','locality'])\
                                                        ['total_cases','hospitalizations','deaths']
                                                        .apply(lambda grp: grp.shift(1)))
    df.fillna(0, inplace=True)
    def get_case_count(row):
        counter = (row['total_cases'] - row['prev_total_cases'])
        if counter < 0:
            return 0
        return counter
    def get_hos_count(row):
        counter = (row['hospitalizations'] - row['prev_hosp'])
        if counter < 0:
            return 0
        return counter
    def get_death_count(row):
        counter = (row['deaths'] - row['prev_deaths'])
        if counter < 0:
            return 0
        return counter
    df['new_cases'] = df.apply(lambda row: get_case_count(row), axis=1 )
    df['new_hosp'] = df.apply(lambda row: get_hos_count(row), axis=1 )
    df['new_deaths'] = df.apply(lambda row: get_death_count(row), axis=1 )

    # get weekly rolling avg
    df['weekly_rolling_avg_cases'] = df.new_cases.rolling(7).mean()

    df['total_cases_rate']=round(df.total_cases / df.Population * 100000).astype(int)
    df['hospitalizations_rate']=round(df.hospitalizations / df.Population * 100000).astype(int)
    df['deaths_rate']=round(df.deaths / df.Population * 100000).astype(int)


    new_df = df[['report_date', 'fips', 'region', 'vdh_health_district', 'locality', 'Population',
                   'total_cases', 'hospitalizations', 'deaths', 'new_cases', 'new_hosp',
                   'new_deaths', 'weekly_rolling_avg_cases', 'total_cases_rate',
                   'hospitalizations_rate','deaths_rate']]
    return new_df

case_df = preprocess_case_df()
case_df.to_csv('data/cases.csv', index=False)
###############################################################################
def preprocess_vax_df():
    """
    Preprocess the case_data from sql db and output as 3 dfs
    """
    # Access dataset from SQL db
    engine = create_engine('sqlite:///covid.db')
    df = pd.read_sql('SELECT v.*, p.Population FROM vaccine_data v LEFT JOIN pop_data p ON v.locality=p.Locality;'
                         ,engine)

    # Convert Datetime
    df['administration_date'] = pd.to_datetime(df.administration_date)
    df['vaccine_doses_administered'] = df.vaccine_doses_administered.astype(int)
    df.Population.fillna(0, inplace=True)
    df['Population'] = df.Population.astype(int)

    # Add Region column
    central=["Chesterfield", "Crater", "Chickahominy","Henrico","Piedmont","Richmond","Southside"]
    eastern = ["Chesapeake", "Eastern Shore", "Hampton", "Norfolk", "Peninsula", "Portsmouth", "Three Rivers",
           "Virginia Beach", "Western Tidewater"]
    northern = ["Alexandria", "Arlington", "Fairfax", "Loudoun", "Prince William"]
    northwest = ["Central Shenandoah", "Lord Fairfax", "Rappahannock", "Rappahannock Rapidan", "Blue Ridge"]
    southwest = ["Alleghany", "Central Virginia", "Cumberland Plateau", "Lenowisco", "Mount Rogers", "New River",
            "Pittsylvania-Danville", "Roanoke", "West Piedmont"]
    other = ["Not Reported", "Out of State"]

    region_dict = {"central": central,
                 "eastern": eastern,
                 "northern": northern,
                 "northwest": northwest,
                 "southwest": southwest,
                 "other": other}
    region_map = {val:key for key, lst in region_dict.items() for val in lst}
    df['region'] = df.health_district.map(region_map)

    # separate out the federal doses
    other_df = df[df.Population == 0]
    county_df = df[df.Population != 0]

    # dose in population percentage
    county_df['pop_perc'] = county_df.vaccine_doses_administered / county_df.Population *100

    # weekly rolling avg doses
    county_df.sort_values(['region','health_district', 'locality','administration_date'],
              inplace=True,ascending=True,ignore_index=True)
    county_df['weekly_rolling_avg_dose'] = county_df.vaccine_doses_administered.rolling(7).mean()

    county_df = county_df[['administration_date',  'fips', 'region','health_district','locality', 'Population',
                           'facility_type', 'vaccine_manufacturer', 'dose_number', 'vaccine_doses_administered',
                           'pop_perc','weekly_rolling_avg_dose']]

    #dfs for county map
    one_dose = county_df[county_df.dose_number =="1"].groupby(['fips','locality','Population']).vaccine_doses_administered.sum().reset_index()
    one_dose.columns = ['fips','locality','population','One_dose']
    full_vax = county_df[(county_df.dose_number =="2")|((county_df.dose_number =="1") & (county_df.vaccine_manufacturer =='J&J'))].groupby(['fips','locality','Population']).vaccine_doses_administered.sum().reset_index()
    full_vax.columns = ['fips','locality','population','Fully_vaccinated']
    total_dose = county_df.groupby(['fips','locality','Population']).vaccine_doses_administered.sum().reset_index()
    total_dose.columns = ['fips','locality','population','Total_doses']

    #merge dfs
    data_frames = [total_dose, one_dose, full_vax]
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['fips','locality','population'],
                                            how='left'), data_frames)

    df_merged['Total_doses_rate'] = round(df_merged.Total_doses / df_merged.population * 100000).astype(int)
    df_merged['One_dose_rate'] = round(df_merged.One_dose / df_merged.population * 100000).astype(int)
    df_merged['Fully_vaccinated_rate'] = round(df_merged.Total_doses / df_merged.population * 100000).astype(int)

    return df, county_df, other_df, df_merged

df, county_df, other_df, df_merged= preprocess_vax_df()
df.to_csv('data/vax.csv', index=False)
county_df.to_csv('data/county_vax.csv', index=False)
other_df.to_csv('data/other_vax.csv',index=False)
df_merged.to_csv('data/vax_map.csv',index=False)
