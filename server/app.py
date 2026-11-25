
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User, ArticleSchema, UserSchema


# Create the Flask application
app = Flask(__name__)

# Secret key for signing session cookies
# Development lesson only
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize the database
db.init_app(app)

# Initialize database migrations
migrate = Migrate(app, db)


# STEP 1: Clear session page views
@app.route('/clear')
def clear_session():

    session['page_views'] = 0

    return {
        'message': '200: Successfully cleared session data.'
    }, 200


# STEP 2: Show all articles
@app.route('/articles')
def index_articles():

    articles = [
        ArticleSchema().dump(article)
        for article in Article.query.all()
    ]

    return make_response(jsonify(articles), 200)


# STEP 3: Show one article with a paywall
@app.route('/articles/<int:id>')
def show_article(id):

    # Get previous page views and increment by 1
    session['page_views'] = session.get('page_views', 0) + 1

    # Block visitors after 3 article views
    if session['page_views'] > 3:

        return {
            'message': 'Maximum pageview limit reached'
        }, 401

    # Retrieve the article from the database
    article = Article.query.get(id)

    # Handle missing articles
    if not article:

        return {
            'error': 'Article not found'
        }, 404

    # Serialize and return the article
    return make_response(
        jsonify(ArticleSchema().dump(article)),
        200
    )


# Start Flask
if __name__ == '__main__':
    app.run(port=5555)
