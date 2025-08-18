
import pandas as pd
from google_play_scraper import app, Sort, reviews_all
import time
import random

def scrape_balanced_reviews(package_name, target_counts):
    """
    Scrape reviews with focus on negative and neutral ratings
    
    Args:
        package_name: App package name (e.g., 'com.jiji.android')
        target_counts: Dict with target counts for each rating
    """
    
    all_reviews = []
    
    # Focus on negative reviews first (1-2 stars)
    for rating in [1, 2]:
        if target_counts.get(rating, 0) > 0:
            print(f"Collecting {rating}-star reviews...")
            
            # Collect reviews for specific rating
            reviews = reviews_all(
                package_name,
                lang='en',  # English reviews
                country='et',  # Ethiopia
                sort=Sort.NEWEST,
                count=target_counts[rating] * 2,  # Get more to filter
                filter_score_with=rating  # Filter by rating
            )
            
            # Filter to exact rating and limit
            filtered_reviews = [r for r in reviews if r['score'] == rating]
            filtered_reviews = filtered_reviews[:target_counts[rating]]
            
            all_reviews.extend(filtered_reviews)
            print(f"Collected {len(filtered_reviews)} {rating}-star reviews")
            
            # Respectful delay
            time.sleep(random.uniform(2, 5))
    
    # Collect neutral reviews (3 stars)
    if target_counts.get(3, 0) > 0:
        print("Collecting 3-star reviews...")
        reviews = reviews_all(
            package_name,
            lang='en',
            country='et', 
            sort=Sort.NEWEST,
            count=target_counts[3] * 2,
            filter_score_with=3
        )
        
        filtered_reviews = [r for r in reviews if r['score'] == 3]
        filtered_reviews = filtered_reviews[:target_counts[3]]
        
        all_reviews.extend(filtered_reviews)
        print(f"Collected {len(filtered_reviews)} 3-star reviews")
        time.sleep(random.uniform(2, 5))
    
    # Only collect positive reviews if needed
    for rating in [4, 5]:
        if target_counts.get(rating, 0) > 0:
            print(f"Collecting {rating}-star reviews...")
            reviews = reviews_all(
                package_name,
                lang='en',
                country='et',
                sort=Sort.NEWEST, 
                count=target_counts[rating] * 2,
                filter_score_with=rating
            )
            
            filtered_reviews = [r for r in reviews if r['score'] == rating]
            filtered_reviews = filtered_reviews[:target_counts[rating]]
            
            all_reviews.extend(filtered_reviews)
            print(f"Collected {len(filtered_reviews)} {rating}-star reviews")
            time.sleep(random.uniform(2, 5))
    
    return all_reviews

def main():
    # Jiji app package name 
    package_name = 'com.combanketh.mobilebanking'  
    
    # Target counts based on  analysis
    target_counts = {
        1: 200,  # 200 1-star reviews
        2: 200,  # 150 2-star reviews  
        3: 400,  # 200 3-star reviews
        4: 200,  # 100 4-star reviews
        5: 200   # 100 5-star reviews
    }
    
    print("Starting balanced review collection...")
    new_reviews = scrape_balanced_reviews(package_name, target_counts)
    
    # Convert to DataFrame
    df_new = pd.DataFrame(new_reviews)
    
    # Save new reviews
    df_new.to_csv('new_balanced_reviews.csv', index=False)
    print(f"Collected {len(new_reviews)} new reviews")
    
    # # Combine with existing data
    # df_existing = pd.read_csv('src/scrape/jiji_play_reviews_all.csv')
    # df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    
    # # Save combined dataset
    # df_combined.to_csv('balanced_playstore_reviews.csv', index=False)
    # print("Combined dataset saved as 'balanced_playstore_reviews.csv'")
    
    # Show new distribution
    # print("\nNew distribution:")
    # score_counts = df_combined['score'].value_counts().sort_index()
    # for score, count in score_counts.items():
    #     percentage = (count / len(df_combined)) * 100
    #     print(f"Score {score}: {count} reviews ({percentage:.1f}%)")

if __name__ == "__main__":
    main()
