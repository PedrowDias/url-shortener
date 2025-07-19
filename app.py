from flask import Flask, request, redirect, render_template
from db import init_db, short_id_exists, generate_short_id
import sqlite3
import re
import logging

app = Flask(__name__)

# Load configuration
app.config.from_pyfile('config.py')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# URL validation regex
url_regex = re.compile(
    r'^(https?://)?'  # Optional http:// or https://
    r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'  # Domain (e.g., example.com)
    r'(/.*)?$'  # Optional path
)

def is_valid_url(url):
    """Validates URL using regex"""
    return bool(url_regex.match(url))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Gets the URL submitted by the input by acessing it's name 'url'
        input_url = request.form['url']
        
        # Ensure URL starts with the HTTP protocol (or its safer version). If not, append it
        if not input_url.startswith(('http://', 'https://')):
            input_url = 'http://' + input_url

        # Validate URL. If it is invalid, send the error to index.html and show it to the user
        if not is_valid_url(input_url):
            logger.warning(f"Invalid URL submitted: {input_url}")
            return render_template('index.html', error="Invalid URL"), 400

        # Generate unique short ID using the functions from db.py
        try:
            while True:
                # From config.py, the length of the shortened URLs will be 6.
                short_id = generate_short_id(app.config['SHORT_ID_LENGTH'])
                if not short_id_exists(short_id):
                    break

            # Store in SQL database
            conn = sqlite3.connect(app.config['DATABASE'])
            c = conn.cursor()
            c.execute("INSERT INTO urls (short_id, input_url) VALUES (?, ?)",
                     (short_id, input_url))
            conn.commit()
            conn.close()

            # This creates a local URL that can be accessed
            short_url = request.host_url + short_id
            logger.info(f"Shortened URL created: {short_url}")
            return render_template('result.html', short_url=short_url)
        
        # If any error happens in the way, it logs the error
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            return render_template('index.html', error="Database error occurred"), 500

    # This line only executes if the method is GET. In this case, it just renders the index.html file
    return render_template('index.html')

# If the user access the shortened URL, this function is responsible for redirecting him to the original URL
@app.route('/<short_id>')
def redirect_url(short_id):
    try:
        # This gets the original url from the given shortened URL
        conn = sqlite3.connect(app.config['DATABASE'])
        c = conn.cursor()
        c.execute("SELECT input_url FROM urls WHERE short_id = ?", (short_id,))
        result = c.fetchone()
        conn.close()

        if result:
            logger.info(f"Redirecting to: {result[0]}")
            return redirect(result[0])
        # This is triggered only if it cannot access the short URL in the table
        logger.warning(f"Short URL not found: {short_id}")
        # Then, returns the Page Not Found error 404
        return render_template('index.html', error="URL not found"), 404
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return render_template('index.html', error="Database error occurred"), 500

# This guarantees that it is only going to be run in this file/module, and not if this is imported
if __name__ == '__main__':
    init_db()
    app.run(debug=app.config['DEBUG'])