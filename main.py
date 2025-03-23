import pandas as pd
from collections import Counter


def load_hitlog(file_path: str):
    """Load the hitlog CSV file into a pandas DataFrame."""
    return pd.read_csv(file_path)


def filter_user_journeys(df: pd.DataFrame):
    """Filter out only articles and registration visits, then group by user_id."""

    df = df[df['page_url'].str.startswith('/articles/') | (df['page_url'] == '/register')]
    
    user_journeys = df.groupby('user_id')['page_url'].apply(list).reset_index()
    return user_journeys


def count_article_influence(user_journeys: pd.DataFrame):
    """Count articles that appear in user journeys leading to registration."""
    article_counter = Counter()

    for _, journey in user_journeys.iterrows():
        if '/register' in journey['page_url']:
            # Find the first occurrence of '/register'
            register_index = journey['page_url'].index('/register')
            # Consider only articles before the first '/register'
            articles_before_register = journey['page_url'][:register_index]
            # Filter only articles and update the counter
            articles = [url for url in articles_before_register if url.startswith('/articles/')]
            article_counter.update(articles)
    
    return article_counter



def get_top_articles(article_counter: Counter, top_n: int=3):
    """Return the top N influential articles as a DataFrame."""
    top_articles = article_counter.most_common(top_n)
    return pd.DataFrame(top_articles, columns=['page_url', 'total'])


def save_results(df: pd.DataFrame, output_file: str):
    """Save the resulting DataFrame to a CSV file."""
    df.to_csv(output_file, index=False)


def main():
    file_path = 'hitlog.csv'  # Change to your actual file path
    output_file = 'top_articles.csv'
    
    df = load_hitlog(file_path)
    user_journeys = filter_user_journeys(df)
    article_counter = count_article_influence(user_journeys)
    top_articles_df = get_top_articles(article_counter)
    save_results(top_articles_df, output_file)
    
    print(f"Top articles saved to {output_file}")


if __name__ == "__main__":
    main()
