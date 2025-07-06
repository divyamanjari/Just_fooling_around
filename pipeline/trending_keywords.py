import requests
from pytrends.request import TrendReq
import sqlite3
from datetime import datetime, timedelta
import random
import time
from bs4 import BeautifulSoup
from config import Config

class TrendingKeywordsFetcher:
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.fashion_categories = Config.FASHION_CATEGORIES
        
    def get_db_connection(self):
        """Get database connection"""
        conn = sqlite3.connect('fashion_blog.db')
        conn.row_factory = sqlite3.Row
        return conn
    
    def fetch_google_trends(self, keyword, timeframe='today 1-m'):
        """Fetch trending data from Google Trends"""
        try:
            self.pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo='US', gprop='')
            interest_over_time = self.pytrends.interest_over_time()
            
            if not interest_over_time.empty:
                # Get average interest over the time period
                avg_interest = interest_over_time[keyword].mean()
                return int(avg_interest) if avg_interest > 0 else 1
            return 1
            
        except Exception as e:
            print(f"Error fetching Google Trends for '{keyword}': {e}")
            return 1
    
    def get_fashion_related_keywords(self):
        """Get fashion-related trending keywords"""
        try:
            # Build payload for fashion category
            self.pytrends.build_payload(['fashion'], cat=172, timeframe='today 1-m', geo='US')
            
            # Get related queries
            related_queries = self.pytrends.related_queries()
            trending_keywords = []
            
            if 'fashion' in related_queries and related_queries['fashion']['rising'] is not None:
                rising_queries = related_queries['fashion']['rising']['query'].tolist()
                trending_keywords.extend(rising_queries[:10])
            
            if 'fashion' in related_queries and related_queries['fashion']['top'] is not None:
                top_queries = related_queries['fashion']['top']['query'].tolist()
                trending_keywords.extend(top_queries[:10])
                
            return list(set(trending_keywords))  # Remove duplicates
            
        except Exception as e:
            print(f"Error fetching fashion trends: {e}")
            return []
    
    def scrape_fashion_blogs_for_trends(self):
        """Scrape popular fashion websites for trending topics"""
        trending_topics = []
        
        # Fashion blog URLs and their trending sections
        fashion_sources = [
            {
                'url': 'https://www.harpersbazaar.com/fashion/',
                'selectors': ['h2', 'h3', '.headline']
            },
            {
                'url': 'https://www.vogue.com/fashion',
                'selectors': ['h2', 'h3', '.headline']
            }
        ]
        
        for source in fashion_sources:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                response = requests.get(source['url'], headers=headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    for selector in source['selectors']:
                        elements = soup.find_all(selector)
                        for element in elements[:5]:  # Limit to first 5 elements
                            text = element.get_text().strip()
                            if len(text) > 10 and len(text) < 100:  # Reasonable length
                                trending_topics.append(text)
                
                # Be respectful with requests
                time.sleep(2)
                
            except Exception as e:
                print(f"Error scraping {source['url']}: {e}")
                continue
        
        return trending_topics[:15]  # Return top 15 topics
    
    def generate_fashion_keywords(self):
        """Generate fashion keywords based on current trends and seasonal factors"""
        base_keywords = []
        
        # Current month-based keywords
        current_month = datetime.now().month
        seasonal_keywords = {
            1: ['winter fashion', 'cozy outfits', 'layering styles', 'wool trends'],
            2: ['valentine\'s day fashion', 'red outfits', 'romantic styles'],
            3: ['spring fashion', 'light layers', 'pastel colors', 'fresh styles'],
            4: ['spring trends', 'floral patterns', 'light fabrics', 'easter outfits'],
            5: ['summer prep', 'light colors', 'versatile pieces'],
            6: ['summer fashion', 'beach styles', 'vacation outfits', 'lightweight fabrics'],
            7: ['summer trends', 'bright colors', 'vacation wear', 'sun dresses'],
            8: ['late summer fashion', 'back to school style', 'transitional pieces'],
            9: ['fall fashion', 'autumn colors', 'layering pieces', 'cozy styles'],
            10: ['fall trends', 'halloween fashion', 'warm layers', 'earth tones'],
            11: ['winter prep', 'thanksgiving outfits', 'warm fashion', 'holiday style'],
            12: ['holiday fashion', 'party outfits', 'glam styles', 'winter trends']
        }
        
        base_keywords.extend(seasonal_keywords.get(current_month, []))
        
        # Add trending fashion terms
        trending_terms = [
            'sustainable fashion', 'vintage style', 'minimalist fashion',
            'street style', 'boho chic', 'athleisure', 'oversized clothing',
            'color blocking', 'metallic fashion', 'textured fabrics',
            'statement accessories', 'bold patterns', 'neutral tones',
            'fashion week trends', 'designer collaborations', 'affordable luxury'
        ]
        
        base_keywords.extend(random.sample(trending_terms, 8))
        
        return base_keywords
    
    def fetch_all_trending_keywords(self):
        """Fetch trending keywords from all sources"""
        all_keywords = []
        
        print("Fetching trending keywords...")
        
        # 1. Get Google Trends fashion keywords
        try:
            google_trends = self.get_fashion_related_keywords()
            all_keywords.extend(google_trends)
            print(f"Found {len(google_trends)} keywords from Google Trends")
        except Exception as e:
            print(f"Error with Google Trends: {e}")
        
        # 2. Scrape fashion blogs
        try:
            scraped_topics = self.scrape_fashion_blogs_for_trends()
            all_keywords.extend(scraped_topics)
            print(f"Found {len(scraped_topics)} topics from fashion blogs")
        except Exception as e:
            print(f"Error scraping fashion blogs: {e}")
        
        # 3. Add generated seasonal keywords
        seasonal_keywords = self.generate_fashion_keywords()
        all_keywords.extend(seasonal_keywords)
        print(f"Added {len(seasonal_keywords)} seasonal keywords")
        
        # 4. Add base fashion categories
        all_keywords.extend(self.fashion_categories)
        
        # Remove duplicates and filter
        unique_keywords = list(set([kw.lower().strip() for kw in all_keywords if len(kw.strip()) > 3]))
        
        # Score and save keywords
        self.save_keywords_to_db(unique_keywords)
        
        return unique_keywords[:Config.TRENDING_KEYWORDS_COUNT * 2]  # Return more than needed
    
    def save_keywords_to_db(self, keywords):
        """Save trending keywords to database"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        for keyword in keywords:
            try:
                # Get trend score (simulated or from Google Trends)
                trend_score = self.fetch_google_trends(keyword)
                
                # Insert or update keyword
                cursor.execute('''
                    INSERT OR REPLACE INTO trending_keywords 
                    (keyword, search_volume, trend_score, category, fetched_at, used_for_content)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (keyword, trend_score, float(trend_score), 'fashion', datetime.now(), False))
                
                # Small delay to avoid rate limiting
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Error saving keyword '{keyword}': {e}")
                continue
        
        conn.commit()
        conn.close()
        print(f"Saved {len(keywords)} keywords to database")
    
    def get_unused_keywords(self, limit=20):
        """Get unused keywords from database for content generation"""
        conn = self.get_db_connection()
        
        keywords = conn.execute('''
            SELECT * FROM trending_keywords 
            WHERE used_for_content = 0 
            ORDER BY trend_score DESC, fetched_at DESC
            LIMIT ?
        ''', (limit,)).fetchall()
        
        conn.close()
        return [dict(row) for row in keywords]
    
    def mark_keyword_as_used(self, keyword_id):
        """Mark a keyword as used for content generation"""
        conn = self.get_db_connection()
        
        conn.execute('''
            UPDATE trending_keywords 
            SET used_for_content = 1 
            WHERE id = ?
        ''', (keyword_id,))
        
        conn.commit()
        conn.close()

if __name__ == "__main__":
    fetcher = TrendingKeywordsFetcher()
    keywords = fetcher.fetch_all_trending_keywords()
    print(f"Fetched {len(keywords)} trending keywords:")
    for kw in keywords[:10]:
        print(f"- {kw}")