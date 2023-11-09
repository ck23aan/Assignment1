# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt


def barplot(df, column, title):
    """Develops bar chart over all years available in dataset and writes to a file.

    Parameters:
        - df (dataframe) : Data Frame
        - column (string): Data Frame Header
        - title (string) : Chart Title
    Example:
        >>> barplot(covidDataset, deathsPerYear, "Deaths Breakdown into years"])

    Returns:
        None
    """

    plt.figure(figsize=(12, 12))

    plt.bar(df["date"], column)

    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel("No of Individuals")

    plt.savefig("barchart" + str(title) + ".png")
    plt.show()

    return


def linechart(df, headers):
    """create a line graph with male vs female lines over all years.

    Parameters:
        - df (Pandas DataFrame): Data Frame
        - headers (string []): list of Data Frame Headers

    Example:
        >>> linechart(sucideDataset, [male_suicides, female_suicides])

    Returns:
        None
    """

    plt.figure(figsize=(12, 12))

    for head in headers:
        plt.plot(df["year"], df[head], label=head)

    plt.xlabel("Year")
    plt.ylabel("No of Sucides")

    # removing white space left and right. Both standard and pandas min/max
    # can be used
    plt.xlim(min(df["year"]), df["year"].max())

    plt.legend()
    plt.title("No of Sucides in male/female individuals in UK: 1985-2015.")
    plt.savefig("lineplot.png")
    plt.show()

    return


def piechart(df, year):
    """Develops pie graph over all years available in dataset and saves \
       it in a file.

    Parameters:
        - df (dataframe): Data Frame
        - year (integer): year

    Example:
        >>> linechart(spotify_dataset, [no_of_users, no of songs])

    Returns:
        None
    """

    plt.figure(figsize=(6, 6))

    row_index = df.loc[df["year"] == (year)].index[0]

    total_Suicides = df.loc[row_index, "male"] + df.loc[row_index, "female"]

    percentValues = [
        (df.loc[row_index, "male"] / total_Suicides) * 100,
        (df.loc[row_index, "female"] / total_Suicides) * 100,
    ]

    plt.pie(
        percentValues,
        labels=["male", "female"],
        colors=["skyblue", "orange"],
        autopct="%1.1f%%",
        shadow=True,
        startangle=140,
    )
    plt.legend()
    plt.title("sucides : " + str(year))
    plt.savefig("piechart" + str(year) + ".png")
    plt.show()

    return


path = "SucideData.csv"
df = pd.read_csv(path)
df = df[df["country"] == "United Kingdom"]
summary_year = df.groupby(["year", "sex"])\
    [["suicides_no"]].sum().reset_index()
summary_year = summary_year.pivot(
    index="year", columns="sex", values="suicides_no"
).reset_index()


linechart(summary_year, ["male", "female"])

piechart(summary_year, 1985)
piechart(summary_year, 2015)

new_path = "worldometer_coronavirus_daily_data.csv"
df_covid19 = pd.read_csv(new_path)
df_covid19["date"] = df_covid19["date"].str.split("-").str[0]
df_covid19 = df_covid19[df_covid19["country"] == "UK"]
df_covid19 = (
    df_covid19.groupby("date")[["daily_new_cases", "daily_new_deaths"]]
    .sum()
    .fillna(0)
    .reset_index()
)
barplot(df_covid19, df_covid19["daily_new_cases"], "New Cases Breakdown")
barplot(df_covid19, df_covid19["daily_new_deaths"], "New Deaths BreakDown")