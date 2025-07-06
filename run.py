#!/usr/bin/env python3
"""
Fashion Forward Blog - Main Application Runner

A modern fashion blog with automated content generation powered by trending keywords.
Features:
- Automated daily content generation (20 posts per day)
- Trending keywords from Google Trends and fashion websites
- Modern responsive web design
- Admin dashboard for monitoring and manual content generation
- SQLite database for easy deployment

Usage:
    python run.py                    # Start web server with scheduler
    python run.py --no-scheduler     # Start web server without scheduler
    python run.py --generate-now     # Generate content immediately and exit
"""

import sys
import argparse
from app import create_app
from pipeline.scheduler import start_content_scheduler, stop_content_scheduler, manual_content_generation
from config import Config

def main():
    parser = argparse.ArgumentParser(description='Fashion Forward Blog Application')
    parser.add_argument('--no-scheduler', action='store_true', 
                       help='Start web server without the automated content scheduler')
    parser.add_argument('--generate-now', action='store_true',
                       help='Generate content immediately and exit')
    parser.add_argument('--host', default=Config.HOST,
                       help=f'Host to bind to (default: {Config.HOST})')
    parser.add_argument('--port', type=int, default=Config.PORT,
                       help=f'Port to bind to (default: {Config.PORT})')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Create Flask application
    app = create_app()
    
    if args.generate_now:
        # Generate content immediately and exit
        print("=" * 60)
        print("FASHION FORWARD BLOG - CONTENT GENERATION")
        print("=" * 60)
        
        with app.app_context():
            try:
                result = manual_content_generation()
                print(f"\n✓ Content generation completed successfully!")
                print(f"  Posts created: {result.get('posts_created', 0)}")
                print(f"  Keywords processed: {result.get('keywords_processed', 0)}")
            except Exception as e:
                print(f"\n✗ Content generation failed: {e}")
                sys.exit(1)
        
        sys.exit(0)
    
    # Print startup banner
    print("\n" + "=" * 60)
    print("FASHION FORWARD BLOG - STARTING UP")
    print("=" * 60)
    print(f"🌐 Web Server: http://{args.host}:{args.port}")
    print(f"📊 Admin Dashboard: http://{args.host}:{args.port}/admin")
    print(f"⚡ Auto-Generation: {'Enabled' if not args.no_scheduler else 'Disabled'}")
    print(f"🔧 Debug Mode: {'Enabled' if args.debug else 'Disabled'}")
    print("=" * 60)
    
    # Start content scheduler if enabled
    if not args.no_scheduler:
        try:
            print("🚀 Starting content scheduler...")
            start_content_scheduler()
            print("✓ Content scheduler started successfully")
            print("📅 Daily content generation scheduled for 8:00 AM")
        except Exception as e:
            print(f"⚠️  Warning: Could not start content scheduler: {e}")
            print("   The web server will still work, but content won't be auto-generated")
    
    try:
        # Start the web server
        print(f"\n🌟 Fashion Forward Blog is now running!")
        print(f"   Visit http://{args.host}:{args.port} to see your fashion blog")
        print(f"   Press Ctrl+C to stop the server\n")
        
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug or Config.DEBUG,
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down Fashion Forward Blog...")
        
        if not args.no_scheduler:
            print("   Stopping content scheduler...")
            stop_content_scheduler()
            print("   ✓ Content scheduler stopped")
        
        print("   ✓ Web server stopped")
        print("   👋 Goodbye!")
        
    except Exception as e:
        print(f"\n💥 Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()