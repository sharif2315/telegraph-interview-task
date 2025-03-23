import pandas as pd
import random
import datetime

def create_sample_data(file_path, num_users=10, num_visits=50):
    """Generate a sample hitlog.csv file with fake data, ensuring a user registers only once per journey."""
    articles = [f'/articles/article{i}' for i in range(1, 6)]
    users = [f'user{i}' for i in range(1, num_users + 1)]
    data = []
    registered_users = set()  # Track users who have already registered
    
    for _ in range(num_visits):
        user = random.choice(users)
        journey = random.sample(articles, k=random.randint(1, 4))  # Use sample() to avoid duplicates
        
        # Ensure registration appears only once in the journey and only if user hasn't registered before
        if user not in registered_users and random.random() > 0.5:
            journey.append('/register')  # Add registration at the end
            registered_users.add(user)  # Mark user as registered

        timestamp = datetime.datetime.now()
        for page in journey:
            data.append({
                'page_name': page.split('/')[-1] if page.startswith('/articles/') else 'register',
                'page_url': page,
                'user_id': user,
                'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })
    
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    print(f"Sample data saved to {file_path}")

# Example usage
create_sample_data('hitlog.csv')
