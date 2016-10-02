import matplotlib.pyplot as plt
import pandas as pd


def _expand_cd_name(short_cd):
    if pd.isnull(short_cd):
        return short_cd
    short_cd = short_cd.split(':')[0]
    cd_mappings = {'BX': 'Bronx',
                   'BK': 'Brooklyn',
                   'MN': 'Manhattan',
                   'QN': 'Queens',
                   'SI': 'Staten Island'}

    borough = cd_mappings[short_cd[:2]]
    cd_number = str(int(short_cd[2:]))

    return "%s CD %s" % (borough, cd_number)


ship_df = pd.DataFrame.from_csv('data/Furman_Center_SHIP_Properties.csv')
ship_df['CD'] = ship_df.CD.map(_expand_cd_name)
units_by_cd = pd.DataFrame({'total_units': ship_df.groupby('CD')['Unit Count'].sum()}).reset_index()

social_indicators_df = pd.DataFrame.from_csv('data/Social_Indicators_Report_Data_By_Community_District.csv')
poverty_rate_by_cd = social_indicators_df[social_indicators_df.Indicator == 'Poverty Rate: Number of New Yorkers in or Near Poverty (2009-2013 average)']

pop_df = pd.DataFrame.from_csv('data/New_York_City_Population_By_Community_Districts.csv')
pop_df['Borough'] = pop_df.index
pop_df['CD'] = pop_df.apply(lambda row: "%s CD %s" % (row['Borough'], row['CD Number']), axis=1)

merged_df = pd.merge(units_by_cd, poverty_rate_by_cd, on='CD', how='inner')
merged_df = pd.merge(merged_df, pop_df, on='CD', how='inner')
merged_df['ship_units_per_capita'] = merged_df.apply(lambda row: 100 * row['total_units'] / row['2010 Population'], axis=1)
merged_df.index = merged_df['CD']
merged_df['poverty_rate'] = pd.to_numeric(merged_df['2013'])

merged_df[['ship_units_per_capita', 'poverty_rate']].plot(kind='bar')
plt.ylabel('percent')
plt.xlabel('Community District')
plt.show()