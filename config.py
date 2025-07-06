import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fashion-blog-secret-key-2024'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///fashion_blog.db'
    
    # Blog settings
    POSTS_PER_PAGE = 12
    DAILY_POSTS_TARGET = 20
    
    # Fashion keywords for content generation
    FASHION_CATEGORIES = [
        'fashion trends', 'style tips', 'outfit ideas', 'designer fashion',
        'street style', 'runway fashion', 'fashion week', 'fashion accessories',
        'seasonal fashion', 'fashion inspiration', 'luxury fashion', 'affordable fashion',
        'sustainable fashion', 'vintage fashion', 'fashion colors', 'fashion patterns',
        'fashion brands', 'fashion influencers', 'fashion photography', 'fashion styling'
    ]
    
    # Trending keywords settings
    TRENDING_KEYWORDS_COUNT = 10
    CONTENT_GENERATION_ENABLED = True
    
    # OpenAI settings (optional for enhanced content generation)
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # Scheduler settings
    DAILY_GENERATION_TIME = "08:00"  # 8 AM daily
    
    # App settings
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))