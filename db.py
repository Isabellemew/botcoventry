import sqlite3

def column_exists(conn, table_name, column_name):
    c = conn.cursor()
    c.execute(f"PRAGMA table_info({table_name})")
    columns = c.fetchall()
    for column in columns:
        if column[1] == column_name:
            return True
    return False

def init_db():
    conn = sqlite3.connect('applicants.db')
    c = conn.cursor()
    # Create applicants table if not exists with minimal columns
    c.execute('''CREATE TABLE IF NOT EXISTS applicants
                 (user_id INTEGER PRIMARY KEY, name TEXT, basis TEXT)''')
    # Add ielts_score if not exists
    if not column_exists(conn, 'applicants', 'ielts_score'):
        c.execute("ALTER TABLE applicants ADD COLUMN ielts_score REAL")
    # Add ent_score if not exists
    if not column_exists(conn, 'applicants', 'ent_score'):
        c.execute("ALTER TABLE applicants ADD COLUMN ent_score INTEGER")
    # Add total_score if not exists
    if not column_exists(conn, 'applicants', 'total_score'):
        c.execute("ALTER TABLE applicants ADD COLUMN total_score REAL")
    # Create documents table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS documents
                 (document_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  document_type TEXT,
                  file_path TEXT,
                  score REAL,
                  UNIQUE(user_id, document_type),
                  FOREIGN KEY(user_id) REFERENCES applicants(user_id))''')
    conn.commit()
    conn.close()