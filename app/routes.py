from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app import get_db_connection
from datetime import datetime, timedelta
import sqlite3

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Homepage with latest blog posts"""
    page = request.args.get('page', 1, type=int)
    per_page = 12
    offset = (page - 1) * per_page
    
    conn = get_db_connection()
    
    # Get total count for pagination
    total_posts = conn.execute('SELECT COUNT(*) FROM blog_posts WHERE published = 1').fetchone()[0]
    
    # Get posts for current page
    posts = conn.execute('''
        SELECT * FROM blog_posts 
        WHERE published = 1 
        ORDER BY created_at DESC 
        LIMIT ? OFFSET ?
    ''', (per_page, offset)).fetchall()
    
    # Get featured posts (latest 3)
    featured_posts = conn.execute('''
        SELECT * FROM blog_posts 
        WHERE published = 1 
        ORDER BY created_at DESC 
        LIMIT 3
    ''').fetchall()
    
    conn.close()
    
    # Calculate pagination
    total_pages = (total_posts + per_page - 1) // per_page
    has_prev = page > 1
    has_next = page < total_pages
    
    return render_template('home.html', 
                         posts=posts, 
                         featured_posts=featured_posts,
                         page=page,
                         total_pages=total_pages,
                         has_prev=has_prev,
                         has_next=has_next)

@main_bp.route('/post/<int:post_id>')
def blog_post(post_id):
    """Individual blog post page"""
    conn = get_db_connection()
    
    # Get the post
    post = conn.execute('''
        SELECT * FROM blog_posts 
        WHERE id = ? AND published = 1
    ''', (post_id,)).fetchone()
    
    if not post:
        conn.close()
        return "Post not found", 404
    
    # Update view count
    conn.execute('UPDATE blog_posts SET views = views + 1 WHERE id = ?', (post_id,))
    
    # Get related posts (same category)
    related_posts = conn.execute('''
        SELECT * FROM blog_posts 
        WHERE category = ? AND id != ? AND published = 1
        ORDER BY created_at DESC 
        LIMIT 4
    ''', (post['category'], post_id)).fetchall()
    
    conn.commit()
    conn.close()
    
    return render_template('blog_post.html', post=post, related_posts=related_posts)

@main_bp.route('/category/<category>')
def category_posts(category):
    """Posts by category"""
    page = request.args.get('page', 1, type=int)
    per_page = 12
    offset = (page - 1) * per_page
    
    conn = get_db_connection()
    
    # Get total count for pagination
    total_posts = conn.execute('''
        SELECT COUNT(*) FROM blog_posts 
        WHERE category = ? AND published = 1
    ''', (category,)).fetchone()[0]
    
    # Get posts for current page
    posts = conn.execute('''
        SELECT * FROM blog_posts 
        WHERE category = ? AND published = 1 
        ORDER BY created_at DESC 
        LIMIT ? OFFSET ?
    ''', (category, per_page, offset)).fetchall()
    
    conn.close()
    
    # Calculate pagination
    total_pages = (total_posts + per_page - 1) // per_page
    has_prev = page > 1
    has_next = page < total_pages
    
    return render_template('category.html', 
                         posts=posts, 
                         category=category,
                         page=page,
                         total_pages=total_pages,
                         has_prev=has_prev,
                         has_next=has_next)

@main_bp.route('/search')
def search():
    """Search blog posts"""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = 12
    offset = (page - 1) * per_page
    
    if not query:
        return redirect(url_for('main.home'))
    
    conn = get_db_connection()
    
    search_term = f'%{query}%'
    
    # Get total count for pagination
    total_posts = conn.execute('''
        SELECT COUNT(*) FROM blog_posts 
        WHERE (title LIKE ? OR content LIKE ? OR keywords LIKE ?) AND published = 1
    ''', (search_term, search_term, search_term)).fetchone()[0]
    
    # Get posts for current page
    posts = conn.execute('''
        SELECT * FROM blog_posts 
        WHERE (title LIKE ? OR content LIKE ? OR keywords LIKE ?) AND published = 1
        ORDER BY created_at DESC 
        LIMIT ? OFFSET ?
    ''', (search_term, search_term, search_term, per_page, offset)).fetchall()
    
    conn.close()
    
    # Calculate pagination
    total_pages = (total_posts + per_page - 1) // per_page
    has_prev = page > 1
    has_next = page < total_pages
    
    return render_template('search_results.html', 
                         posts=posts, 
                         query=query,
                         total_posts=total_posts,
                         page=page,
                         total_pages=total_pages,
                         has_prev=has_prev,
                         has_next=has_next)

@main_bp.route('/admin')
def admin_dashboard():
    """Admin dashboard"""
    conn = get_db_connection()
    
    # Get statistics
    total_posts = conn.execute('SELECT COUNT(*) FROM blog_posts').fetchone()[0]
    published_posts = conn.execute('SELECT COUNT(*) FROM blog_posts WHERE published = 1').fetchone()[0]
    total_views = conn.execute('SELECT SUM(views) FROM blog_posts').fetchone()[0] or 0
    
    # Get recent posts
    recent_posts = conn.execute('''
        SELECT * FROM blog_posts 
        ORDER BY created_at DESC 
        LIMIT 10
    ''').fetchall()
    
    # Get generation log
    generation_log = conn.execute('''
        SELECT * FROM generation_log 
        ORDER BY created_at DESC 
        LIMIT 10
    ''').fetchall()
    
    conn.close()
    
    return render_template('admin.html', 
                         total_posts=total_posts,
                         published_posts=published_posts,
                         total_views=total_views,
                         recent_posts=recent_posts,
                         generation_log=generation_log)

@main_bp.route('/api/generate-content', methods=['POST'])
def generate_content_api():
    """API endpoint to manually trigger content generation"""
    from pipeline.content_generator import generate_daily_content
    
    try:
        result = generate_daily_content()
        return jsonify({
            'success': True,
            'message': f'Generated {result["posts_created"]} new blog posts',
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500