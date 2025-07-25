
# - Write SQL queries to analyze the database and extract meaningful business insights.
# - You must write at least 10 SQL queries that demonstrate your analytical skills and bring value. Some examples of questions to explore:
#   - Which percentage of companies are under which juridical form?
#   - What is the distribution of company statuses?
#   - Calculate average company age by sector (NACE codes)
#   - Track company creation trends over time with time-based analysis
#   - Compare geographical distribution of companies
#   - Find growth trends by sector with year-over-year analysis
#   - Detect seasonal patterns for company creation
#   - Create your own analytical queries that showcase advanced SQL concepts like:
#     - Complex joins (INNER, LEFT, RIGHT)
#     - CASE statements
#     - Date/time functions
#     - Aggregate functions
#     - GROUP BY
#     - ORDER BY
#     - ...
# - Create a 5-8 slides presentation to showcase your insights by using professional storytelling techniques (Problem statement, answer, conclusion)


import sqlite3
import pandas as pd
from utils.nace_section import Nace

db_url = "data/kbo_database.db"

def get_connection():
    return sqlite3.connect(db_url)

def get_categories(cursor):
    query = "SELECT DISTINCT Category FROM code"
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]

def create_category_tables(cursor, categories):
    for category in categories:
        query_create = f"""
            CREATE TABLE IF NOT EXISTS "{category}" (
                code TEXT PRIMARY KEY,
                description_nl TEXT,
                description_fr TEXT,
                description_de TEXT
            );
        """
        cursor.execute(query_create)

def populate_category_tables(cursor, categories):
    cat_detail = {}
    for category in categories:
        query_select = """
            SELECT Code, Language, Description
            FROM code
            WHERE Category = ?
        """
        cursor.execute(query_select, (category,))
        cat_detail[category] = cursor.fetchall()

    for category, rows in cat_detail.items():
        data = {}
        for code, lang, desc in rows:
            lang = lang.lower()
            if code not in data:
                data[code] = {'nl': None, 'fr': None, 'de': None}
            if lang in data[code]:
                data[code][lang] = desc

        for code, langs in data.items():
            query_insert = f"""
                INSERT OR REPLACE INTO "{category}" 
                (code, description_nl, description_fr, description_de)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query_insert, (
                code,
                langs['nl'],
                langs['fr'],
                langs['de']
            ))

def create_activity_labeled_table(cursor):
    query = """
    CREATE TABLE IF NOT EXISTS activity_labeled (
        EntityNumber TEXT,
        NaceCode TEXT,
        description_nl TEXT,
        description_fr TEXT,
        description_de TEXT,
        Classification TEXT,
        nace_section TEXT
    )
    """
    cursor.execute(query)

def populate_activity_labeled(cursor):
    nace_year_map = {
        2003: "Nace2003",
        2008: "Nace2008",
        2025: "Nace2025"
    }
    for year, nace_table in nace_year_map.items():
        query_insert = f"""
            INSERT INTO activity_labeled (EntityNumber, NaceCode, description_nl, description_fr, description_de, Classification)
            SELECT 
                a.EntityNumber,
                a.NaceCode,
                n.description_nl,
                n.description_fr,
                n.description_de,
                a.Classification
            FROM activity AS a
            JOIN "{nace_table}" AS n ON a.NaceCode = n.code
            WHERE a.NaceVersion = ?
        """
        cursor.execute(query_insert, (year,))
        print(f"Inserted rows for NaceVersion {year} using {nace_table}")

def update_nace_sections(cursor):
    cursor.execute("SELECT rowid, NaceCode FROM activity_labeled")
    rows = cursor.fetchall()
    for rowid, nace_code in rows:
        section = Nace.get_nace_section(nace_code)
        cursor.execute("UPDATE activity_labeled SET nace_section = ? WHERE rowid = ?", (section, rowid))
    print("NACE sections updated for all rows.")

def clean_activity_lable(cursor):
    query_clean =  """ CREATE TABLE IF NOT EXISTS activity_lable_cleaned AS
    SELECT DISTINCT EntityNumber, Classification, nace_section
    FROM activity_labeled; """
    cursor.execute(query_clean)
    print("Remove duplicates (entire row repeated)")
    
    
def crete_nac_table(cursor):
    query_create =  """CREATE TABLE IF NOT EXISTS nace_section (section TEXT PRIMARY KEY,
    description TEXT);"""
    cursor.execute(query_create)
    
def insert_nace_table(cursor):
    query_insert = """INSERT INTO nace_section VALUES
    ('A','Agriculture, forestry and fishing'),
    ('B','Mining and quarrying'),
    ('C','Manufacturing'),
    ('D','Electricity, gas, steam and air conditioning supply'),
    ('E','Water supply; sewerage, waste management and remediation activities'),
    ('F','Construction'),
    ('G','Wholesale and retail trade'),
    ('H','Transportation and storage'),
    ('I','Accommodation and food service activities'),
    ('J','Information and communication'),
    ('K','Financial and insurance activities'),
    ('L','Real estate activities'),
    ('M','Professional, scientific and technical activities'),
    ('N','Administrative and support service activities'),
    ('O','Public administration and defence'),
    ('P','Education'),
    ('Q','Human health and social work activities'),
    ('R','Arts, entertainment and recreation'),
    ('S','Other service activities'),
    ('T','Activities of households'),
    ('U','Extraterritorial organisations and bodies');"""
    cursor.execute(query_insert)
    print("created nace section")


   

def main():
    connexion = get_connection()
    cursor = connexion.cursor()

    # categories = get_categories(cursor)
    # create_category_tables(cursor, categories)
    # populate_category_tables(cursor, categories)

    # create_activity_labeled_table(cursor)
    # populate_activity_labeled(cursor)
    # update_nace_sections(cursor)
    
    # clean_activity_lable(cursor)
    
    # crete_nac_table(cursor)
    # insert_nace_table(cursor)
    
    geo_data = pd.read_csv('data/georef-belgium-postal-codes.csv', delimiter=';')
    geo_data.to_sql('geo_data', connexion, if_exists='replace', index=False)

    connexion.commit()
    connexion.close()

if __name__ == "__main__":
    main()
