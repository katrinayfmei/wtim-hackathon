import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as geopd

# Load crime data 
crime_data = pd.read_csv("crimedata.csv")

# Load map
heatmap = geopd.read_file("Police_Divisions.shp")

# Only incidents from downtown Toronto in 2021, no Category column (too vague)
crime_data_2021 = crime_data[crime_data["ReportedYear"] == 2021]
crime_data_2021 = crime_data_2021.drop(["Category", "ReportedYear"], axis = 1)
regions = crime_data_2021["GeoDivision"].unique().tolist()

MAX_SEVERITY = 1240
severities = np.array([4, 4, 2, 3, 3, 3, 3, 4, 3, 3, 3, 3, 5, 2, 1])

def get_plots():

    plots = {}

    for crime_type in crime_data_2021["Subtype"].unique().tolist():

        region_data = crime_data_2021[crime_data_2021["Subtype"] == crime_type]

        # Get number of crimes committed in each region
        region_counts = {}
        for region in regions:
            region_counts[region] = region_data[region_data["GeoDivision"] == region]["Count_"].sum()

        # Plot occurences
        crime_occurences_by_region = pd.DataFrame({"Regions" : region_counts.keys(), "Occurrences" : region_counts.values()})
        plot = sns.barplot(data = crime_occurences_by_region, x = "Regions", y = "Occurrences", color = "#014DA1")

        plt.title("Occurences of crime " + crime_type + " by region")
        plt.tick_params(labelsize = 6)

        plots[crime_type] = plot

    return plots

def get_region_score(region):
    crimes = sorted(crime_data_2021["Subtype"].unique().tolist())
    score = 0
    for i in range(len(crimes)):
        crime = crimes[i]
        severity = severities[i]
        score += severity * crime_data_2021[crime_data_2021["Subtype"] == crime][crime_data_2021["GeoDivision"] == region]["Count_"].sum()
    return score

def calculate_color(region):
    MAX_SEVERITY = 61750
    region_score = get_region_score(region)
    return region_score * 255 / MAX_SEVERITY

get_plots()