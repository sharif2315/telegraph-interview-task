import unittest
from unittest.mock import patch
import pandas as pd
from collections import Counter
from main import (
    load_hitlog, filter_user_journeys, count_article_influence, 
    get_top_articles, save_results)


class TestArticleInfluence(unittest.TestCase):

    @patch('pandas.read_csv')
    def test_load_hitlog(self, mock_read_csv):
        """Test the load_hitlog function."""
        # Mock the DataFrame returned by pd.read_csv
        mock_df = pd.DataFrame({
            'page_name': ['article1', 'article2', 'article3', 'register',  # User 1 visits articles and then registers
                        'article4', 'article5', 'register',  # User 2 visits articles and then registers
                        'article1', 'article2', 'register'],  # User 3 visits articles and then registers
            'page_url': ['/articles/article1', '/articles/article2', '/articles/article3', '/register',
                        '/articles/article4', '/articles/article5', '/register',
                        '/articles/article1', '/articles/article2', '/register'],
            'user_id': [1, 1, 1, 1, 2, 2, 2, 3, 3, 3],
            'timestamp': ['2025-03-23 14:30:44', '2025-03-23 14:32:10', '2025-03-23 14:35:00', '2025-03-23 14:36:30',  # User 1 timestamps
                        '2025-03-23 14:40:12', '2025-03-23 14:42:18', '2025-03-23 14:43:50',  # User 2 timestamps
                        '2025-03-23 14:45:30', '2025-03-23 14:46:20', '2025-03-23 14:47:40']  # User 3 timestamps
        })

        mock_read_csv.return_value = mock_df
        
        # Call the function
        df = load_hitlog('fake_path.csv')
        
        # Assertions
        mock_read_csv.assert_called_once_with('fake_path.csv')
        pd.testing.assert_frame_equal(df, mock_df)


    def x_test_filter_user_journeys_old(self):
        """Test the filter_user_journeys function."""
        data = {
            'user_id': [1, 1, 2, 2, 3],
            'page_url': ['/articles/article1', '/register', '/articles/article2', '/articles/article3', '/register'],
            'timestamp': ['2021-01-01'] * 5
        }
        df = pd.DataFrame(data)
        
        expected_result = pd.DataFrame({
            'user_id': [1, 2, 3],
            'page_url': [
                ['/articles/article1', '/register'],
                ['/articles/article2', '/articles/article3'],
                ['/register']
            ]
        })
        
        user_journeys = filter_user_journeys(df)
        
        pd.testing.assert_frame_equal(user_journeys, expected_result)


    def test_filter_user_journeys(self):
        """Test the filter_user_journeys function."""
        # Mock data based on realistic user journeys
        data = {
            'user_id': [1, 1, 1, 2, 2, 2, 3, 3, 3],
            'page_url': [
                '/articles/article1', '/articles/article2', '/register',  # User 1 visits articles and registers
                '/articles/article3', '/articles/article4', '/register',  # User 2 visits articles and registers
                '/articles/article1', '/articles/article2', '/register'   # User 3 visits articles and registers
            ],
            'timestamp': [
                '2025-03-23 14:30:44', '2025-03-23 14:32:10', '2025-03-23 14:35:00',  # User 1 timestamps
                '2025-03-23 14:40:12', '2025-03-23 14:42:18', '2025-03-23 14:43:50',  # User 2 timestamps
                '2025-03-23 14:45:30', '2025-03-23 14:46:20', '2025-03-23 14:47:40'   # User 3 timestamps
            ]
        }
        
        df = pd.DataFrame(data)

        # Expected result after filtering only articles and registers, and grouping by user_id
        expected_result = pd.DataFrame({
            'user_id': [1, 2, 3],
            'page_url': [
                ['/articles/article1', '/articles/article2', '/register'],  # User 1 journey
                ['/articles/article3', '/articles/article4', '/register'],  # User 2 journey
                ['/articles/article1', '/articles/article2', '/register']   # User 3 journey
            ]
        })
        
        # Apply the filter_user_journeys function
        user_journeys = filter_user_journeys(df)
        
        # Assert if the result matches the expected output
        pd.testing.assert_frame_equal(user_journeys, expected_result)



    def test_count_article_influence(self):
        """Test the count_article_influence function."""
        # Mock data simulating realistic user journeys where articles are visited before registration
        data = {
            'user_id': [1, 1, 2, 2, 2, 3, 3, 3],
            'page_url': [
                '/articles/article1', '/register',  # User 1 visits article1 and then registers
                '/articles/article2', '/articles/article3', '/register',  # User 2 visits article2 and article3, then registers
                '/articles/article3', '/articles/article4', '/register'   # User 3 visits article3 and article4, then registers
            ],
            'timestamp': [
                '2025-03-23 14:30:44', '2025-03-23 14:35:00',  # User 1 timestamps
                '2025-03-23 14:40:12', '2025-03-23 14:42:18', '2025-03-23 14:43:50',  # User 2 timestamps
                '2025-03-23 14:45:30', '2025-03-23 14:46:20', '2025-03-23 14:46:31'   # User 3 timestamps
            ]
        }

        df = pd.DataFrame(data)
        user_journeys = filter_user_journeys(df)

        # Call the count_article_influence function
        article_counter = count_article_influence(user_journeys)

        # Check the count of each article visited before registering
        self.assertEqual(article_counter['/articles/article1'], 1)  # Article1 visited by User 1
        self.assertEqual(article_counter['/articles/article2'], 1)  # Article2 visited by User 2
        self.assertEqual(article_counter['/articles/article3'], 2)  # Article3 visited by User 2 and User 3
        self.assertEqual(article_counter['/articles/article4'], 1)  # Article4 visited by User 3


    def test_get_top_articles(self):
        """Test the get_top_articles function."""
        article_counter = Counter({
            '/articles/article1': 3,
            '/articles/article2': 2,
            '/articles/article3': 1
        })
        
        top_articles_df = get_top_articles(article_counter, top_n=2)
        
        # Check if the DataFrame has the expected top articles
        self.assertEqual(len(top_articles_df), 2)
        self.assertEqual(top_articles_df.iloc[0]['page_url'], '/articles/article1')
        self.assertEqual(top_articles_df.iloc[1]['page_url'], '/articles/article2')


    @patch('pandas.DataFrame.to_csv')
    def test_save_results(self, mock_to_csv):
        """Test the save_results function."""
        data = {
            'page_url': ['/articles/article1', '/articles/article2'],
            'total': [3, 2]
        }
        df = pd.DataFrame(data)
        
        save_results(df, 'output.csv')
        
        # Check if to_csv was called correctly
        mock_to_csv.assert_called_once_with('output.csv', index=False)

if __name__ == "__main__":
    unittest.main()
 