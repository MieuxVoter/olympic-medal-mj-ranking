import requests
import pandas as pd
from datetime import datetime, timedelta
from flag_utils import country_acronym_to_flag
import os

PATH = os.path.dirname(os.path.abspath(__file__)) + '/../data'


def scrap_olympic_data():
    # Step 1: Fetch the JSON data from the URL
    url = "https://olympics.com/OG2024/data/CIS_MedalNOCs~lang=ENG~comp=OG2024.json"
    session = requests.Session()
    session.headers.update(
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'})

    try:
        response = session.get(url, timeout=80)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        data = response.json()       # Parse JSON if request was successful
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something went wrong with the request:", err)
    else:
        # Step 2: Convert JSON data to a DataFrame if no exceptions were raised
        df = pd.DataFrame(data)
        print(df.head())  # Display the first few rows of the DataFrame to verify

    # Step 2: Parse the JSON data
    # The relevant part of the JSON is under the key 'medalNOC'
    medal_data = data['medalNOC']

    # Step 3: Create a DataFrame from the parsed data
    df = pd.DataFrame(medal_data)

    print(df.head())

    # Step 4: Normalize nested columns (if needed)
    # 'organisation' column is nested, so we'll normalize it
    organisation_df = pd.json_normalize(df['organisation'])
    organisation_df.columns = [f'organisation.{col}' for col in organisation_df.columns]
    df = df.drop(columns=['organisation']).join(organisation_df)

    print(df.head())
    # keep gender == TOT
    df = df[df["gender"] == "TOT"]
    df = df[df["sport"] == "GLO"]

    df["Country"] = df["org"].apply(lambda x: f"{x} {country_acronym_to_flag(x)}")
    df["Gold"] = df["gold"]
    df["Silver"] = df["silver"]
    df["Bronze"] = df["bronze"]
    df["Total"] = df["gold"] + df["silver"] + df["bronze"]
    df["lexicographic_order"] = df["sortRankTotal"]

    # drop unnecessary columns
    columns = ["gold", "silver", "bronze", "gender", "sport"]
    df = df.drop(columns=columns)

    # reoganize columns by total amount of medals
    df = df.sort_values(by=["Total"], ascending=False)

    # Step 5: Save the DataFrame to a CSV file
    time_date_suffix_canadian_time = datetime.now().strftime("%Y%m%d_%Hh")
    # add 6 hours
    time_date_suffix_french_time = (datetime.now() + timedelta(hours=6)).strftime("%Y%m%d_%Hh")

    df.to_csv(f"{PATH}/medal_data_{time_date_suffix_french_time}.csv", index=False)

    print("CSV file has been created successfully.")

    return df, time_date_suffix_french_time
