# Fashion Forward Blog 💫

A modern, AI-powered fashion blog that automatically generates and publishes 20 trending fashion articles daily. Built with Flask, featuring beautiful responsive design and automated content creation using Google Trends and web scraping.

![Fashion Forward](https://img.shields.io/badge/Fashion-Forward-pink?style=for-the-badge&logo=sparkles)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3+-green?style=for-the-badge&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-orange?style=for-the-badge&logo=sqlite)

## ✨ Features

### 🤖 Automated Content Generation
- **Daily Content Creation**: Automatically generates 20 high-quality fashion blog posts every day
- **Trending Keywords**: Fetches trending fashion keywords from Google Trends and popular fashion websites
- **Smart Categorization**: Automatically categorizes content into trends, style tips, seasonal fashion, accessories, and more
- **Seasonal Awareness**: Adapts content based on current month and fashion seasons

### 🎨 Modern Web Design
- **Responsive Design**: Beautiful, mobile-first design that works on all devices
- **Modern UI**: Clean, elegant interface with smooth animations and hover effects
- **Typography**: Professional typography using Playfair Display and Inter fonts
- **Visual Appeal**: Automatic placeholder images for all blog posts

### 📊 Admin Dashboard
- **Real-time Statistics**: Monitor total posts, views, and generation logs
- **Manual Generation**: Trigger content generation manually when needed
- **Content Management**: View and manage all blog posts from a central dashboard
- **Generation History**: Track all automated content generation activities

### 🔍 User Features
- **Advanced Search**: Full-text search across all blog content
- **Category Filtering**: Browse posts by fashion categories
- **Pagination**: Smooth pagination for better user experience
- **Social Sharing**: Built-in social media sharing buttons
- **Related Posts**: Intelligent related post suggestions

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd fashion-blog
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python run.py
```

4. **Access the blog**
- **Website**: http://localhost:5000
- **Admin Dashboard**: http://localhost:5000/admin

## 🛠️ Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
# Optional: OpenAI API key for enhanced content generation
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Custom settings
SECRET_KEY=your_secret_key_here
DEBUG=false
HOST=0.0.0.0
PORT=5000
```

### Custom Configuration
Edit `config.py` to customize:

- **Daily post target** (default: 20 posts)
- **Generation schedule** (default: 8:00 AM daily)
- **Fashion categories**
- **Trending keywords count**

## 📖 Usage

### Starting the Application

#### Standard Mode (with auto-generation)
```bash
python run.py
```

#### Without Auto-generation
```bash
python run.py --no-scheduler
```

#### Generate Content Immediately
```bash
python run.py --generate-now
```

#### Custom Host/Port
```bash
python run.py --host 0.0.0.0 --port 8080
```

#### Debug Mode
```bash
python run.py --debug
```

### Content Generation

The system automatically:
1. **Fetches trending keywords** from Google Trends and fashion websites
2. **Generates blog posts** with compelling titles and comprehensive content
3. **Categorizes content** appropriately
4. **Publishes posts** to the website
5. **Logs activities** for monitoring

### Admin Dashboard

Access the admin dashboard at `/admin` to:
- View real-time statistics
- Monitor content generation logs
- Manually trigger content generation
- Browse all blog posts
- Check system status

## 🏗️ Architecture

### Project Structure
```
fashion-blog/
├── app/                    # Flask application
│   ├── __init__.py        # App factory
│   └── routes.py          # Web routes
├── pipeline/              # Content generation pipeline
│   ├── __init__.py
│   ├── trending_keywords.py  # Keyword fetching
│   ├── content_generator.py  # Blog post generation
│   └── scheduler.py       # Automated scheduling
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── home.html         # Homepage
│   ├── blog_post.html    # Individual post
│   ├── admin.html        # Admin dashboard
│   ├── category.html     # Category pages
│   └── search_results.html  # Search results
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── run.py               # Main application runner
└── README.md            # This file
```

### Data Flow
1. **Keyword Fetching**: Retrieves trending fashion keywords from multiple sources
2. **Content Generation**: Creates comprehensive blog posts based on keywords
3. **Database Storage**: Stores posts, keywords, and generation logs in SQLite
4. **Web Interface**: Serves content through Flask web application
5. **Automation**: Schedules daily content generation

## 🎯 Content Categories

The system generates content across multiple fashion categories:

- **Fashion Trends** 🔥 - Latest runway and street style trends
- **Style Tips** 💡 - Expert styling advice and tutorials
- **Seasonal Fashion** 🍂 - Season-appropriate fashion guidance
- **Accessories** 💎 - Jewelry, bags, shoes, and styling accessories
- **Sustainable Fashion** ♻️ - Eco-friendly and ethical fashion choices
- **Outfit Ideas** 👗 - Complete outfit inspirations
- **Color & Patterns** 🎨 - Color theory and pattern mixing

## 🔧 Customization

### Adding New Categories
Edit `config.py` and add to `FASHION_CATEGORIES`:
```python
FASHION_CATEGORIES = [
    'your new category',
    # ... existing categories
]
```

### Modifying Content Templates
Edit templates in `pipeline/content_generator.py`:
- Blog title templates
- Content structure
- Style tips and advice

### Changing Generation Schedule
Modify `DAILY_GENERATION_TIME` in `config.py`:
```python
DAILY_GENERATION_TIME = "09:30"  # 9:30 AM daily
```

## 📊 API Endpoints

### Web Routes
- `GET /` - Homepage with latest posts
- `GET /post/<id>` - Individual blog post
- `GET /category/<category>` - Category-filtered posts
- `GET /search` - Search results
- `GET /admin` - Admin dashboard

### API Endpoints
- `POST /api/generate-content` - Manually trigger content generation

## 🚨 Troubleshooting

### Common Issues

**Content not generating automatically**
- Check if scheduler is enabled (`--no-scheduler` not used)
- Verify internet connectivity for Google Trends
- Check logs in admin dashboard

**Database errors**
- Ensure SQLite database is writable
- Check file permissions in project directory

**Missing dependencies**
- Reinstall requirements: `pip install -r requirements.txt`
- Update pip: `pip install --upgrade pip`

**Port already in use**
- Use custom port: `python run.py --port 8080`
- Find and stop conflicting process

### Debug Mode
Run with debug mode for detailed error information:
```bash
python run.py --debug
```

## 🛡️ Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### Environment Setup
- Set `DEBUG=false` in production
- Use strong `SECRET_KEY`
- Configure proper firewall rules
- Set up SSL/TLS certificate

### Database Backup
Regular SQLite database backups:
```bash
cp fashion_blog.db fashion_blog.db.backup
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Trends API** for trending keyword data
- **Bootstrap** for responsive web components
- **Font Awesome** for beautiful icons
- **Picsum Photos** for placeholder images
- **Flask** framework for web application foundation

## 📞 Support

For support, questions, or feature requests:
- Open an issue on GitHub
- Check the troubleshooting section
- Review the configuration options

---

**Fashion Forward Blog** - Bringing you the latest in fashion trends, powered by AI 💫✨
