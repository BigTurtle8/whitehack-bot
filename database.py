import psycopg2
import os

ON_HEROKU = 'ON_HEROKU' in os.environ

if ON_HEROKU == False:
    from secrets import DISCORD_TOKEN, rito_api_token, USER, PASSWORD, DATABASE_URL, DATABASE
    TOKEN = DISCORD_TOKEN

else:
    TOKEN = os.environ.get('TOKEN')
    rito_api_token = os.environ.get('RITO_API_TOKEN')
    USER = os.environ.get('USER')
    PASSWORD = os.environ.get('PASSWORD')
    DATABASE = os.environ.get("DATABASE")
    DATABASE_URL = os.environ.get('DATABASE_URL')

def create_table():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require',
                            database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    cursor.execute(
            """
            DROP TABLE IF EXISTS elo_tracker;

            CREATE TABLE elo_tracker (
                discord_id VARCHAR(50) PRIMARY KEY,
                division VARCHAR(50),
                LP integer
            );
            """
    )
    conn.commit()
    
    conn.close()
    

def matchmaking(user):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require',
                            database=DATABASE, user=USER, password=PASSWORD)
        cursor = conn.cursor()
        
        data = (user,)
        cursor.execute(
            """
            INSERT INTO elo_tracker (discord_id, division, LP)
            VALUES
                (
                    %s,
                    'Iron 1',
                    0
                ) 
            ON CONFLICT (discord_id) 
            DO NOTHING;
            """,
            data
        )

        cursor.execute(
            """
            SELECT * FROM elo_tracker;
            """
        )
        
        record = cursor.fetchall()
        #print(record)

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database conn.
            if(conn):
                conn.commit()
                cursor.close()
                conn.close()
                print("PostgreSQL conn is closed")
