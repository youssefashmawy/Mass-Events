# Mass Events Analysis

A web scraping and data processing tool that collects event information from TicketsMarche and processes it for mass events analysis in Egypt.

## Overview

This project scrapes event data from TicketsMarche, cleans and standardizes the information, then generates attendance estimates for events in major Egyptian cities. The system provides insights for event organizers and venue managers.

## Features

- Automated event data scraping from TicketsMarche
- Intelligent date parsing for complex date formats
- Venue mapping with GPS coordinates for Egyptian venues
- City classification and filtering (Cairo, Giza, Alexandria)
- Data processing and export to Excel format

## Installation

First, install the required packages from the requirements file:

```bash
pip install -r requirements.txt
```

Then install Playwright browsers for JavaScript rendering:

```bash
playwright install chromium
```

## Usage

### 1. Data Collection

Run the Scrapy spider to collect event data:

```bash
cd Mass_Event
scrapy crawl gather_ticketsmarche -o Mass_Event/analysis/TicketsMarche/events_meetup_test.json
```

### 2. Data Processing

Process the collected data:

```bash
cd Mass_Event/analysis
python ticketsMarche.py
```

This will generate the main output file: **attends_estimate_test.xlsx**

## Output

The primary output is `attends_estimate_test.xlsx`, which contains:

- Filtered events based on specified criteria
- Standardized event dates (YYYY-MM-DD format)
- Venue information with GPS coordinates
- City classifications
- Processed data ready for analysis

## Configuration

You can modify the filtering parameters in `ticketsMarche.py`:

```python
# Filter by cities and date range
filters(_data, ["cairo", "giza"], "2025-10-01", "2025-12-31")
```

## Data Sources

- TicketsMarche API for event listings
- Reference CSV file for venue mapping and coordinates
- Custom venue database for Egyptian locations

## Technical Notes

- Handles Arabic text and special characters through Unicode normalization
- Uses Playwright for JavaScript-heavy website scraping
- Processes complex date formats including date ranges
- Includes error handling for network failures and data parsing issues

## Project Structure

The main components are:

- `Mass_Event/spiders/gather.py` - Web scraping spider
- `Mass_Event/analysis/ticketsMarche.py` - Data processing script
- `output/referance.csv` - Venue reference data
- `attends_estimate_test.xlsx` - Main output file