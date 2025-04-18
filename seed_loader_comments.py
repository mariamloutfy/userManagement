import psycopg2
from config.database import connect_db

def copy_from_csv(file_path, table_name, columns):
    try:
        conn = connect_db()
        cur = conn.cursor()
        
        # Open the CSV file and load the data
        with open(file_path, 'r') as f:
            next(f)  # Skip header
            cur.copy_expert(f"COPY {table_name}({columns}) FROM STDIN WITH CSV", f)
        
        # Commit changes and close connection
        conn.commit()
        cur.close()
        conn.close()
        print(f"Data loaded into {table_name}")
    except Exception as e:
        print(f"Error loading data into {table_name}: {str(e)}")

if __name__ == '__main__':
    # Insert users first
    copy_from_csv('seeds/comments_seed.csv', 'comments', 'comment,created_by,post_id,created_at')
    # Insert posts after users are inserted

