from flask import Flask, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Establish connection to MySQL
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',  # Update this for Heroku
            user='seanjibowu',  # Update to your Heroku database user
            password='Black4679**',  # Update to your Heroku database password
            database='apocrypha_decoded'  # Update to your Heroku database name
        )
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

def display_year(year):
    """Convert year from integer to BC/AD format for display."""
    if year < 0:
        return f"{abs(year)} BC"  # Convert negative year to BC
    else:
        return f"{year} AD"  # Convert positive year to AD

@app.route('/')
def index():
    conn = get_db_connection()
    if conn is None:
        return "Database connection error", 500
    
    cursor = conn.cursor()

    # Query for books in chronological order
    cursor.execute("SELECT name, author, year_written, is_apocrypha, notes, links FROM books ORDER BY year_written ASC")
    books = cursor.fetchall()

    # Format the book data for display
    formatted_books = []
    for book in books:
        name, author, year_written, is_apocrypha, notes, link = book
        formatted_year = display_year(year_written)  # Convert to BC/AD format
        apocrypha_status = "Apocrypha" if is_apocrypha else "Canon"
        
        # Create a hyperlink for the book name
        if link:
            formatted_name = f'<a href="{link}" target="_blank">{name}</a>'
        else:
            formatted_name = name  # Fallback to plain name if no link
        
        formatted_books.append({
            'name': formatted_name,
            'author': author,
            'year_written': formatted_year,
            'is_apocrypha': apocrypha_status,
            'notes': notes
        })

    # Query for translations
    translations = {}
    cursor.execute("""
        SELECT books.name, translations.language, translations.translation
        FROM translations 
        JOIN books ON books.id = translations.book_id
    """)
    for book_name, language, translation in cursor.fetchall():
        if book_name not in translations:
            translations[book_name] = []
        translations[book_name].append((language, translation))
    
    cursor.close()
    conn.close()
    
    return render_template('index.html', books=formatted_books, translations=translations)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

