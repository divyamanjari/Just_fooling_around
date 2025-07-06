from flask import Flask
import sqlite3
import os
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Initialize database
    init_database()
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app

def init_database():
    """Initialize the SQLite database with required tables"""
    db_path = 'fashion_blog.db'
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create blog posts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blog_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            summary TEXT,
            category TEXT,
            keywords TEXT,
            author TEXT DEFAULT 'Fashion Editor',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            published BOOLEAN DEFAULT 1,
            views INTEGER DEFAULT 0,
            featured_image TEXT,
            tags TEXT
        )
    ''')
    
    # Create trending keywords table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trending_keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            search_volume INTEGER,
            trend_score REAL,
            category TEXT,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            used_for_content BOOLEAN DEFAULT 0
        )
    ''')
    
    # Create generation log table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generation_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            posts_generated INTEGER,
            keywords_fetched INTEGER,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('fashion_blog.db')
    conn.row_factory = sqlite3.Row
    return conn