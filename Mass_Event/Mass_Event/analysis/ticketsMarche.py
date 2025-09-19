import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    data.loc[:, "location"] = data.loc[:, "location"].str[0]
    data.loc[:, "date"] = data.loc[:, "date"].str[0]
    data.loc[:, "event_name"] = data.loc[:, "event_name"].str[0]
    data[["date", "Time"]] = data.date.str.split("|", n=1, expand=True)
    data.rename(columns={"location": "venue_name"}, inplace=True)
    data.venue_name = data.venue_name.str.normalize("NFKD")
    return data


def mapping(data: pd.DataFrame) -> pd.DataFrame:
    ref = pd.read_csv(
        r"E:\youssef ashmawy\programming projects\Python\Nokia Task\output\referance.csv"
    )
    ref.city = ref.city.str.lower()
    venue_mapping = ref.set_index("venue_name")["venue_address"].to_dict()
    city_mapping = ref.set_index("venue_name")["city"].to_dict()
    data["venue_coordinates"] = data["venue_name"].map(venue_mapping)
    data["city"] = data["venue_name"].map(city_mapping)
    return data


def main():
    data = pd.read_json(
        r"E:\youssef ashmawy\programming projects\Python\Nokia Task\Mass_Event\events_meetup.json"
    )
    data = clean_data(data)
    data = mapping(data)
    data.to_csv(r"E:\youssef ashmawy\programming projects\Python\Nokia Task\Mass_Event\Mass_Event\analysis\TicketsMarche\ticketMarche_test.csv",index=False)


if __name__ == "__main__":
    main()
