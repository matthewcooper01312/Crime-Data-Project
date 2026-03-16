#import libraries
import pandas as pd
import matplotlib.pyplot as mp
import seaborn as sb
import os

#compile data
data_path = r"C:\Users\matth\PycharmProjects\JupyterProject\crimestuff"
all_data = []

for folder in os.listdir(data_path):
    folder_path = os.path.join(data_path, folder)
    if os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            if file.endswith(".csv"):
                file_path = os.path.join(folder_path, file)
                df = pd.read_csv(file_path)
                all_data.append(df)

#preprocessing
crime_df = pd.concat(all_data, ignore_index=True)
crime_df.head()
crime_df.info()
crime_df = crime_df.drop_duplicates()
crime_df["Month"] = pd.to_datetime(crime_df["Month"])
crime_df.to_csv("processedcrime.csv", index=False)


# trends
crime_df["Force_clean"] = crime_df["Falls within"].str.replace(
    r"\b(Police|Constabulary|Service)\b", "", regex=True
).str.strip()
crimebyforce = pd.crosstab(crime_df["Force_clean"], crime_df["Crime type"])
crimebyforce.plot(kind="bar", stacked=True, figsize=(12,7))
mp.title("Crime Types per Police Force")
mp.ylabel("Number of Crimes")
mp.xlabel("Police Force")
mp.show()


herts_df = crime_df[crime_df["Falls within"] == "Hertfordshire Constabulary"]
hertscrimebymonth = herts_df.groupby("Month").size().sort_index()
herts_df["Year"] = herts_df["Month"].dt.year
herts_df["Month_number"] = herts_df["Month"].dt.month
hertscrimebymonth.plot()
mp.title("Monthly Crime Trend – Hertfordshire (2024–2026)")
mp.xlabel("Month")
mp.ylabel("Number of Crimes")
mp.show()

hertscrimeno = herts_df["Crime type"].value_counts().head(10)
mp.figure(figsize=(10,6))
sb.barplot(x=hertscrimeno.values, y=hertscrimeno.index)
mp.title("Top 10 Crime Types – Hertfordshire (2024-2026")
mp.xlabel("Number of Crimes")
mp.ylabel("Crime Type")
mp.show()

beds_df = crime_df[crime_df["Falls within"] == "Bedfordshire Police"]

bedscrimebymonth = beds_df.groupby("Month").size().sort_index()
beds_df["Year"] = beds_df["Month"].dt.year
beds_df["Month_number"] = beds_df["Month"].dt.month
bedscrimebymonth.plot()
mp.title("Monthly Crime Trend – Bedfordshire (2024–2026)")
mp.xlabel("Month")
mp.ylabel("Number of Crimes")
mp.show()

bedscrimeno = beds_df["Crime type"].value_counts().head(10)
mp.figure(figsize=(10,6))
sb.barplot(x=bedscrimeno.values, y=bedscrimeno.index)
mp.title("Top 10 Crime Types – Bedfordshire (2024-2026")
mp.xlabel("Number of Crimes")
mp.ylabel("Crime Type")
mp.show()