import sqlite3

def create_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.executescript('''
    DROP TABLE IF EXISTS evanston311;
    DROP TABLE IF EXISTS stackoverflow;
    DROP TABLE IF EXISTS tag_type;
    DROP TABLE IF EXISTS tag_company;
    DROP TABLE IF EXISTS company;
    DROP TABLE IF EXISTS fortune500;

    CREATE TABLE evanston311 (
      id INTEGER PRIMARY KEY,
      priority TEXT,
      source TEXT,
      category TEXT,
      date_created DATETIME,
      date_completed DATETIME,
      street TEXT,
      house_num TEXT,
      zip TEXT,
      description TEXT
    );

    CREATE TABLE company (
      id INTEGER PRIMARY KEY,
      exchange TEXT,
      ticker TEXT UNIQUE,
      name TEXT NOT NULL,
      parent_id INTEGER
    );

    CREATE TABLE tag_company (
      tag TEXT PRIMARY KEY,
      company_id INTEGER REFERENCES company(id)
    );

    CREATE TABLE stackoverflow (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      tag TEXT REFERENCES tag_company(tag),
      date DATE,
      question_count INTEGER DEFAULT 0,  
      question_pct REAL, 
      unanswered_count INTEGER,
      unanswered_pct REAL
    );

    CREATE TABLE tag_type (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      tag TEXT REFERENCES tag_company(tag),
      type TEXT
    );

    CREATE TABLE fortune500 (
      rank INTEGER NOT NULL,
      title TEXT PRIMARY KEY,
      name TEXT NOT NULL UNIQUE,
      ticker TEXT,
      url TEXT,
      hq TEXT,
      sector TEXT,
      industry TEXT,
      employees INTEGER CHECK (employees > 0),
      revenues INTEGER,
      revenues_change REAL,
      profits REAL,
      profits_change REAL,
      assets REAL CHECK (assets > 0),
      equity REAL
    );
    ''')
    conn.commit()
    cursor.close()

def main():
    create_database()

if __name__ == "__main__":
    main()
