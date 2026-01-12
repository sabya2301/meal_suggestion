import sqlite3
from datetime import datetime, timedelta
import os
from logger import setup_logger

logger = setup_logger("db_handler")

# Use absolute path ensures the DB is created in the same directory as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "meal_history.db")

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with the meals table."""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                meal_type TEXT NOT NULL,
                content TEXT NOT NULL,
                macros TEXT
            )
        ''')
        conn.commit()
        conn.close()
        logger.info(f"Database initialized and table verified at {DB_NAME}")
    except Exception as e:
        logger.exception("Failed to initialize database")

def add_meal(meal_type, content, macros=None, date=None):
    """
    Add a new meal to the database.
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('INSERT INTO meals (date, meal_type, content, macros) VALUES (?, ?, ?, ?)',
                (date, meal_type, content, macros))
        conn.commit()
        conn.close()
        logger.debug(f"Added meal: {meal_type} on {date}")
    except Exception as e:
        logger.exception("Error adding meal")

def get_recent_meals(days=3):
    """
    Retrieve meals from the last 'days' days.
    
    Returns:
        list: A list of dictionaries representing the meals.
    """
    conn = get_db_connection()
    c = conn.cursor()
    
    # Calculate date threshold
    threshold_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    c.execute('SELECT * FROM meals WHERE date >= ? ORDER BY date DESC', (threshold_date,))
    rows = c.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

if __name__ == "__main__":
    # When run directly, initialize the DB
    init_db()
    print(f"Database initialized at {DB_NAME}")
