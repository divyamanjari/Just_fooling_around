#!/usr/bin/env python3
"""
Fashion Forward Blog - Setup Test Script

This script verifies that all dependencies are installed correctly
and that the basic functionality works as expected.

Usage:
    python test_setup.py
"""

import sys
import os

def test_imports():
    """Test that all required packages can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import flask
        print(f"  ✓ Flask {flask.__version__}")
    except ImportError as e:
        print(f"  ✗ Flask not found: {e}")
        return False
    
    try:
        import sqlite3
        print(f"  ✓ SQLite3 available")
    except ImportError as e:
        print(f"  ✗ SQLite3 not found: {e}")
        return False
    
    try:
        import requests
        print(f"  ✓ Requests {requests.__version__}")
    except ImportError as e:
        print(f"  ✗ Requests not found: {e}")
        return False
    
    try:
        import bs4
        print(f"  ✓ BeautifulSoup4 available")
    except ImportError as e:
        print(f"  ✗ BeautifulSoup4 not found: {e}")
        return False
    
    try:
        import pytrends
        print(f"  ✓ PyTrends available")
    except ImportError as e:
        print(f"  ✗ PyTrends not found: {e}")
        return False
    
    try:
        import schedule
        print(f"  ✓ Schedule {schedule.__version__}")
    except ImportError as e:
        print(f"  ✗ Schedule not found: {e}")
        return False
    
    return True

def test_database():
    """Test database creation and basic operations"""
    print("\n🗄️  Testing database...")
    
    try:
        from app import init_database, get_db_connection
        
        # Initialize database
        init_database()
        print("  ✓ Database initialized")
        
        # Test connection
        conn = get_db_connection()
        
        # Test table creation
        tables = ['blog_posts', 'trending_keywords', 'generation_log']
        for table in tables:
            result = conn.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'").fetchone()
            if result:
                print(f"  ✓ Table '{table}' exists")
            else:
                print(f"  ✗ Table '{table}' missing")
                return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"  ✗ Database test failed: {e}")
        return False

def test_keyword_fetching():
    """Test keyword fetching functionality"""
    print("\n🔍 Testing keyword fetching...")
    
    try:
        from pipeline.trending_keywords import TrendingKeywordsFetcher
        
        fetcher = TrendingKeywordsFetcher()
        
        # Test seasonal keyword generation
        keywords = fetcher.generate_fashion_keywords()
        if keywords and len(keywords) > 0:
            print(f"  ✓ Generated {len(keywords)} seasonal keywords")
            print(f"    Examples: {', '.join(keywords[:3])}")
        else:
            print("  ⚠️  No seasonal keywords generated")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Keyword fetching test failed: {e}")
        return False

def test_content_generation():
    """Test content generation functionality"""
    print("\n📝 Testing content generation...")
    
    try:
        from pipeline.content_generator import FashionContentGenerator
        
        generator = FashionContentGenerator()
        
        # Test title generation
        title = generator.generate_blog_title("spring fashion")
        if title:
            print(f"  ✓ Generated title: {title[:50]}...")
        else:
            print("  ✗ Failed to generate title")
            return False
        
        # Test content generation
        content = generator.generate_blog_content("spring fashion", title)
        if content and len(content) > 100:
            print(f"  ✓ Generated content ({len(content)} characters)")
        else:
            print("  ✗ Failed to generate content")
            return False
        
        # Test categorization
        category = generator.categorize_content("spring fashion")
        if category:
            print(f"  ✓ Categorized as: {category}")
        else:
            print("  ✗ Failed to categorize")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ✗ Content generation test failed: {e}")
        return False

def test_flask_app():
    """Test Flask application creation"""
    print("\n🌐 Testing Flask application...")
    
    try:
        from app import create_app
        
        app = create_app()
        
        if app:
            print("  ✓ Flask app created successfully")
            
            # Test basic routes exist
            with app.app_context():
                from flask import url_for
                routes = ['main.home', 'main.admin_dashboard']
                for route in routes:
                    try:
                        url = url_for(route)
                        print(f"  ✓ Route '{route}' available")
                    except Exception as e:
                        print(f"  ✗ Route '{route}' failed: {e}")
                        return False
        else:
            print("  ✗ Failed to create Flask app")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ✗ Flask app test failed: {e}")
        return False

def main():
    print("=" * 60)
    print("FASHION FORWARD BLOG - SETUP TEST")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Run all tests
    tests = [
        test_imports,
        test_database,
        test_keyword_fetching,
        test_content_generation,
        test_flask_app
    ]
    
    for test in tests:
        if not test():
            all_tests_passed = False
    
    print("\n" + "=" * 60)
    
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED!")
        print("\nYour Fashion Forward Blog is ready to run!")
        print("\nNext steps:")
        print("  1. Run: python run.py")
        print("  2. Visit: http://localhost:5000")
        print("  3. Check admin: http://localhost:5000/admin")
        print("\nFor immediate content generation:")
        print("  python run.py --generate-now")
    else:
        print("❌ SOME TESTS FAILED!")
        print("\nPlease fix the issues above before running the blog.")
        print("\nCommon solutions:")
        print("  1. Install missing dependencies: pip install -r requirements.txt")
        print("  2. Check Python version (3.8+ required)")
        print("  3. Ensure internet connectivity for external APIs")
        return 1
    
    print("\n" + "=" * 60)
    return 0

if __name__ == '__main__':
    sys.exit(main())