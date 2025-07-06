import schedule
import time
import threading
from datetime import datetime
from pipeline.content_generator import generate_daily_content
from config import Config

class ContentScheduler:
    def __init__(self):
        self.is_running = False
        self.scheduler_thread = None
        
    def daily_job(self):
        """Job that runs daily to generate content"""
        try:
            print(f"Starting scheduled content generation at {datetime.now()}")
            result = generate_daily_content()
            print(f"Scheduled generation completed: {result['posts_created']} posts created")
            
        except Exception as e:
            print(f"Error in scheduled content generation: {e}")
    
    def start_scheduler(self):
        """Start the scheduler in a separate thread"""
        if self.is_running:
            print("Scheduler is already running")
            return
            
        # Schedule daily content generation
        schedule.every().day.at(Config.DAILY_GENERATION_TIME).do(self.daily_job)
        
        # Also run immediately if no posts exist
        self.check_and_run_initial_generation()
        
        self.is_running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        print(f"Content scheduler started. Daily generation at {Config.DAILY_GENERATION_TIME}")
    
    def check_and_run_initial_generation(self):
        """Check if we need to run initial content generation"""
        import sqlite3
        
        try:
            conn = sqlite3.connect('fashion_blog.db')
            cursor = conn.cursor()
            
            # Check if we have any blog posts
            post_count = cursor.execute('SELECT COUNT(*) FROM blog_posts').fetchone()[0]
            
            if post_count == 0:
                print("No blog posts found. Running initial content generation...")
                self.daily_job()
            else:
                print(f"Found {post_count} existing blog posts")
                
            conn.close()
            
        except Exception as e:
            print(f"Error checking initial content: {e}")
    
    def _run_scheduler(self):
        """Internal method to run the scheduler loop"""
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                print(f"Error in scheduler loop: {e}")
                time.sleep(60)
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.is_running = False
        schedule.clear()
        
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=5)
        
        print("Content scheduler stopped")
    
    def get_next_run_time(self):
        """Get the next scheduled run time"""
        jobs = schedule.get_jobs()
        if jobs:
            return jobs[0].next_run
        return None
    
    def run_manual_generation(self):
        """Manually trigger content generation"""
        print("Manual content generation triggered")
        return self.daily_job()

# Global scheduler instance
content_scheduler = ContentScheduler()

def start_content_scheduler():
    """Start the content scheduler"""
    content_scheduler.start_scheduler()

def stop_content_scheduler():
    """Stop the content scheduler"""
    content_scheduler.stop_scheduler()

def manual_content_generation():
    """Manually trigger content generation"""
    return content_scheduler.run_manual_generation()

if __name__ == "__main__":
    # Run scheduler as standalone script
    print("Starting Fashion Blog Content Scheduler...")
    
    try:
        start_content_scheduler()
        
        # Keep the script running
        while True:
            next_run = content_scheduler.get_next_run_time()
            if next_run:
                print(f"Next scheduled run: {next_run}")
            time.sleep(3600)  # Print status every hour
            
    except KeyboardInterrupt:
        print("\nShutting down scheduler...")
        stop_content_scheduler()
        print("Scheduler stopped")