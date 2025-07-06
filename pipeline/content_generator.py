import sqlite3
import random
from datetime import datetime
import os
from pipeline.trending_keywords import TrendingKeywordsFetcher
from config import Config

class FashionContentGenerator:
    def __init__(self):
        self.keyword_fetcher = TrendingKeywordsFetcher()
        self.fashion_categories = Config.FASHION_CATEGORIES
        
    def get_db_connection(self):
        """Get database connection"""
        conn = sqlite3.connect('fashion_blog.db')
        conn.row_factory = sqlite3.Row
        return conn
    
    def generate_blog_title(self, keyword):
        """Generate engaging blog post titles based on keyword"""
        title_templates = [
            "The Ultimate Guide to {keyword}: Everything You Need to Know",
            "How to Master {keyword} Like a Fashion Pro",
            "10 Stunning Ways to Style {keyword} This Season",
            "{keyword}: The Trend That's Taking Over Fashion",
            "Why {keyword} is the Must-Have Look Everyone's Talking About",
            "From Runway to Street: How to Wear {keyword}",
            "The Complete {keyword} Style Guide for Every Occasion",
            "Trending Now: {keyword} Looks That Will Elevate Your Wardrobe",
            "Fashion Forward: The Rise of {keyword} in Modern Style",
            "Effortless {keyword}: Simple Ways to Nail This Trend",
            "{keyword} Done Right: Celebrity Inspired Looks",
            "The {keyword} Revolution: How to Style This Game-Changing Trend",
            "Sustainable {keyword}: Eco-Friendly Ways to Embrace This Style",
            "Budget-Friendly {keyword}: Designer Looks for Less",
            "{keyword} Through the Seasons: Year-Round Styling Tips"
        ]
        
        template = random.choice(title_templates)
        title = template.format(keyword=keyword.title())
        
        # Ensure title is not too long
        if len(title) > 80:
            title = f"{keyword.title()}: The Complete Style Guide"
            
        return title
    
    def generate_blog_content(self, keyword, title):
        """Generate comprehensive blog post content"""
        
        # Introduction paragraphs
        intros = [
            f"Fashion is constantly evolving, and {keyword} has emerged as one of the most captivating trends of the season. Whether you're a style novice or a fashion veteran, understanding how to incorporate {keyword} into your wardrobe can completely transform your look.",
            f"In the ever-changing world of fashion, {keyword} stands out as a trend that perfectly balances style and versatility. This comprehensive guide will help you navigate the exciting world of {keyword} and show you how to make it work for your unique aesthetic.",
            f"From the runways of Paris to the streets of New York, {keyword} has captured the attention of fashion enthusiasts worldwide. If you've been wondering how to embrace this trend, you're in the right place."
        ]
        
        # Style tips sections
        style_tips = [
            f"**Start Small with Accessories**: If you're new to {keyword}, begin by incorporating small accessories that feature this trend. This allows you to experiment without committing to a complete wardrobe overhaul.",
            f"**Mix High and Low**: Combine affordable pieces with investment items to create a balanced look that showcases {keyword} without breaking the bank.",
            f"**Consider Your Body Type**: {keyword} can be adapted to flatter any figure. Focus on pieces that highlight your best features while embracing this trendy aesthetic.",
            f"**Play with Proportions**: The key to mastering {keyword} is understanding how different proportions work together to create visually appealing outfits.",
            f"**Color Coordination**: When working with {keyword}, pay attention to color palettes that complement both the trend and your skin tone."
        ]
        
        # Occasion-based styling
        occasions = [
            f"**Work-Appropriate {keyword}**: Professional settings require a subtle approach. Opt for tailored pieces that incorporate {keyword} elements without being too bold.",
            f"**Weekend Casual**: For relaxed days, embrace the more playful side of {keyword} with comfortable yet stylish pieces.",
            f"**Evening Elegance**: Transform {keyword} for formal occasions by choosing sophisticated silhouettes and luxurious fabrics.",
            f"**Date Night Ready**: Create romantic looks using {keyword} as your inspiration, focusing on feminine details and flattering cuts."
        ]
        
        # Seasonal considerations
        seasonal_content = [
            f"**Spring Styling**: As the weather warms up, lighter fabrics and brighter colors make {keyword} perfect for spring wardrobes.",
            f"**Summer Vibes**: Embrace breathable materials and vibrant hues to make {keyword} work for hot weather styling.",
            f"**Fall Transition**: Layer smartly to carry {keyword} into cooler months, mixing textures and weights for visual interest.",
            f"**Winter Warmth**: Don't abandon {keyword} when temperatures drop. Cozy knits and warm outerwear can incorporate this trend beautifully."
        ]
        
        # Shopping tips
        shopping_tips = [
            f"**Quality Over Quantity**: When investing in {keyword} pieces, prioritize well-made items that will last beyond the trend cycle.",
            f"**Versatility is Key**: Look for pieces that can be styled multiple ways, ensuring you get maximum wear from your {keyword} investments.",
            f"**Budget-Conscious Shopping**: Explore secondhand stores and rental services to experiment with {keyword} without the high price tag.",
            f"**Sustainable Choices**: Consider the environmental impact of your fashion choices by supporting brands that prioritize sustainability."
        ]
        
        # Build the complete content
        content = f"""
{random.choice(intros)}

## Understanding {keyword.title()}

{keyword.title()} represents more than just a fleeting fashion moment—it's a reflection of how modern style continues to evolve and adapt to contemporary lifestyles. This trend has gained momentum because it offers both aesthetic appeal and practical wearability.

## Styling Tips for {keyword.title()}

{random.choice(style_tips)}

{random.choice(style_tips)}

{random.choice(style_tips)}

## Occasion-Based Styling

{random.choice(occasions)}

{random.choice(occasions)}

## Seasonal Adaptation

{random.choice(seasonal_content)}

{random.choice(seasonal_content)}

## Shopping Smart

{random.choice(shopping_tips)}

{random.choice(shopping_tips)}

## Celebrity Inspiration

Fashion icons and celebrities have been spotted embracing {keyword} in innovative ways. From red carpet appearances to casual street style moments, these influential figures demonstrate the versatility and appeal of this trend.

## Conclusion

Incorporating {keyword} into your wardrobe doesn't have to be intimidating. Start with one or two key pieces and gradually build your collection as you become more comfortable with the aesthetic. Remember, the best fashion choices are those that make you feel confident and authentic.

Whether you're completely new to {keyword} or looking to refine your approach, the key is to experiment and have fun with your style choices. Fashion should be an expression of your personality, and {keyword} offers countless opportunities for creative expression.

## Final Thoughts

As fashion continues to evolve, {keyword} proves that great style is about more than following trends—it's about finding what works for you and making it your own. Embrace the journey of style discovery and enjoy the process of making {keyword} a part of your unique fashion story.
"""
        
        return content.strip()
    
    def generate_blog_summary(self, title, content):
        """Generate a brief summary of the blog post"""
        keyword = title.split(':')[0].split(' ')[-1].lower()
        
        summaries = [
            f"Discover everything you need to know about {keyword} in fashion. From styling tips to seasonal adaptations, this comprehensive guide covers all aspects of this trending style.",
            f"Learn how to incorporate {keyword} into your wardrobe with expert tips and practical advice. Perfect for fashion enthusiasts looking to stay on-trend.",
            f"A complete guide to mastering {keyword} with professional styling advice, shopping tips, and inspiration for every occasion.",
            f"Explore the latest in {keyword} fashion with this detailed style guide featuring tips from industry experts and real-world applications."
        ]
        
        return random.choice(summaries)
    
    def categorize_content(self, keyword):
        """Determine the most appropriate category for the content"""
        category_mapping = {
            'trends': ['trend', 'trending', 'fashion week', 'runway', 'latest'],
            'style tips': ['style', 'styling', 'how to', 'guide', 'tips'],
            'seasonal': ['spring', 'summer', 'fall', 'winter', 'seasonal', 'holiday'],
            'accessories': ['accessories', 'jewelry', 'bags', 'shoes', 'belt'],
            'outfits': ['outfit', 'look', 'ensemble', 'combination'],
            'colors': ['color', 'pattern', 'print', 'hue', 'shade'],
            'sustainable': ['sustainable', 'eco', 'ethical', 'green', 'conscious'],
            'budget': ['affordable', 'budget', 'cheap', 'discount', 'sale']
        }
        
        keyword_lower = keyword.lower()
        
        for category, keywords in category_mapping.items():
            if any(word in keyword_lower for word in keywords):
                return category
                
        return 'fashion trends'  # Default category
    
    def generate_tags(self, keyword, content):
        """Generate relevant tags for the blog post"""
        base_tags = ['fashion', 'style', 'trends', 'outfit', 'clothing']
        
        # Add keyword-related tags
        keyword_tags = keyword.lower().split()
        base_tags.extend(keyword_tags)
        
        # Add seasonal tags based on current month
        current_month = datetime.now().month
        seasonal_tags = {
            1: ['winter', 'cold weather'], 2: ['winter', 'valentine'], 3: ['spring', 'transition'],
            4: ['spring', 'easter'], 5: ['spring', 'warm weather'], 6: ['summer', 'vacation'],
            7: ['summer', 'hot weather'], 8: ['summer', 'back to school'], 9: ['fall', 'autumn'],
            10: ['fall', 'halloween'], 11: ['fall', 'thanksgiving'], 12: ['winter', 'holiday']
        }
        
        base_tags.extend(seasonal_tags.get(current_month, []))
        
        # Add content-based tags
        content_lower = content.lower()
        if 'celebrity' in content_lower:
            base_tags.append('celebrity style')
        if 'sustainable' in content_lower:
            base_tags.append('sustainable fashion')
        if 'budget' in content_lower or 'affordable' in content_lower:
            base_tags.append('budget fashion')
        if 'designer' in content_lower:
            base_tags.append('designer fashion')
            
        # Remove duplicates and return as comma-separated string
        unique_tags = list(set(base_tags))
        return ', '.join(unique_tags[:10])  # Limit to 10 tags
    
    def create_blog_post(self, keyword_data):
        """Create a complete blog post from keyword data"""
        keyword = keyword_data['keyword']
        
        # Generate content
        title = self.generate_blog_title(keyword)
        content = self.generate_blog_content(keyword, title)
        summary = self.generate_blog_summary(title, content)
        category = self.categorize_content(keyword)
        tags = self.generate_tags(keyword, content)
        
        # Save to database
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO blog_posts 
            (title, content, summary, category, keywords, tags, created_at, published)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, content, summary, category, keyword, tags, datetime.now(), True))
        
        post_id = cursor.lastrowid
        
        # Mark keyword as used
        cursor.execute('''
            UPDATE trending_keywords 
            SET used_for_content = 1 
            WHERE id = ?
        ''', (keyword_data['id'],))
        
        conn.commit()
        conn.close()
        
        return {
            'id': post_id,
            'title': title,
            'keyword': keyword,
            'category': category,
            'created_at': datetime.now().isoformat()
        }

def generate_daily_content():
    """Main function to generate daily blog content"""
    print(f"Starting daily content generation at {datetime.now()}")
    
    # Initialize components
    keyword_fetcher = TrendingKeywordsFetcher()
    content_generator = FashionContentGenerator()
    
    try:
        # Fetch fresh trending keywords
        print("Fetching trending keywords...")
        keyword_fetcher.fetch_all_trending_keywords()
        
        # Get unused keywords for content generation
        unused_keywords = keyword_fetcher.get_unused_keywords(Config.DAILY_POSTS_TARGET)
        
        if len(unused_keywords) < Config.DAILY_POSTS_TARGET:
            print(f"Warning: Only {len(unused_keywords)} unused keywords available, less than target of {Config.DAILY_POSTS_TARGET}")
        
        # Generate blog posts
        generated_posts = []
        posts_to_generate = min(len(unused_keywords), Config.DAILY_POSTS_TARGET)
        
        print(f"Generating {posts_to_generate} blog posts...")
        
        for i, keyword_data in enumerate(unused_keywords[:posts_to_generate]):
            try:
                print(f"Generating post {i+1}/{posts_to_generate}: {keyword_data['keyword']}")
                post = content_generator.create_blog_post(keyword_data)
                generated_posts.append(post)
                
            except Exception as e:
                print(f"Error generating post for keyword '{keyword_data['keyword']}': {e}")
                continue
        
        # Log generation results
        conn = content_generator.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO generation_log 
            (date, posts_generated, keywords_fetched, status)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().date(), len(generated_posts), len(unused_keywords), 'success'))
        
        conn.commit()
        conn.close()
        
        print(f"Successfully generated {len(generated_posts)} blog posts")
        
        return {
            'posts_created': len(generated_posts),
            'keywords_processed': len(unused_keywords),
            'posts': generated_posts
        }
        
    except Exception as e:
        print(f"Error in daily content generation: {e}")
        
        # Log error
        conn = content_generator.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO generation_log 
            (date, posts_generated, keywords_fetched, status)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().date(), 0, 0, f'error: {str(e)}'))
        
        conn.commit()
        conn.close()
        
        raise e

if __name__ == "__main__":
    result = generate_daily_content()
    print(f"Content generation completed: {result}")