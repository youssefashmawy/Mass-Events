import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import re


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    data.loc[:, "location"] = data.loc[:, "location"].str[0]
    data.loc[:, "date"] = data.loc[:, "date"].str[0]
    data.loc[:, "event_name"] = data.loc[:, "event_name"].str[0]
    data[["date", "Time"]] = data.date.str.split("|", n=1, expand=True)
    data.rename(columns={"location": "venue_name"}, inplace=True)
    data.venue_name = data.venue_name.str.normalize("NFKD")
    return data


def simplify_dates(df: pd.DataFrame, date_column="date"):
    """
    Simplify date ranges by extracting just the first/start date.
    Returns DataFrame with standardized dates in YYYY-MM-DD format.
    """

    def extract_first_date(date_str: str):
        """Extract just the first/start date from any pattern"""
        if not isinstance(date_str, str) or not date_str.strip():
            return date_str

        # 29 sep or sep 29
        # from x to y return x
        day_match = re.search(r"(\d+)(?:st|nd|rd|th)*", date_str)
        month_match = re.search(
            r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*",
            date_str,
            re.IGNORECASE,
        )

        if day_match and month_match:
            day = int(day_match.group(1))
            month_name = month_match.group(0)

            # Layali Marrasi, known date

            if month_name == "Marassi":
                return datetime(2025, 9, 20).strftime("%Y-%m-%d")
            month_num = datetime.strptime(month_name[:3], "%b").month

            year_match = re.search(r"\b(20\d{2})\b", date_str)
            year = int(year_match.group(1)) if year_match else datetime.now().year

            try:
                return datetime(year, month_num, day).strftime("%Y-%m-%d")
            except ValueError:
                return date_str

        return date_str

    # Apply the extraction function
    df["date_parsed"] = df[date_column].apply(extract_first_date)

    return df


def mapping(data: pd.DataFrame) -> pd.DataFrame:
    ref = pd.read_csv(
        r"E:\youssef ashmawy\programming projects\Python\Nokia Task\output\referance.csv"
    )
    ref.city = ref.city.str.lower()
    venue_mapping = ref.set_index("venue_name")["venue_address"].to_dict()
    city_mapping = ref.set_index("venue_name")["city"].to_dict()
    data["venue_coordinates"] = data["venue_name"].map(venue_mapping)
    data["city"] = data["venue_name"].map(city_mapping)
    data = simplify_dates(data)
    return data


def main():
    data = pd.read_json(
        r"E:\youssef ashmawy\programming projects\Python\Nokia Task\Mass_Event\events_meetup.json"
    )
    data = clean_data(data)
    data = mapping(data)
    data.to_csv(
        r"E:\youssef ashmawy\programming projects\Python\Nokia Task\Mass_Event\Mass_Event\analysis\TicketsMarche\ticketMarche_test.csv",
        index=False,
    )


if __name__ == "__main__":
    main()
