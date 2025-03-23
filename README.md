# Article Influence Analysis

This project analyzes user journeys to determine the most influential articles that lead to user registrations.

## Installation

Ensure you have Python 3 installed. Then, install the required dependencies:

```sh
pip3 install -r requirements.txt
```

## Usage

To process the hitlog data and get the top articles leading to registration, run:

```sh
python3 main.py
```

This will generate a CSV file containing the top influential articles.

## Running Tests

To run the unit tests and verify the implementation, use:

```sh
python3 -m unittest test_article_influence.py
```

This will execute the test suite and validate the filtering and counting logic.

## Project Overview

The key functions in this project include:
- `load_hitlog(file_path)`: Loads the hitlog data from a CSV file.
- `filter_user_journeys(df)`: Filters the data to keep only articles and registration visits, grouping them by user.
- `count_article_influence(user_journeys)`: Counts how often each article appears in journeys leading to registration.
- `get_top_articles(article_counter, top_n)`: Extracts the most influential articles based on occurrences.
- `save_results(df, output_file)`: Saves the results to a CSV file.
