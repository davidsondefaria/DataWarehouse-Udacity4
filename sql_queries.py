import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplay_table;"
user_table_drop = "DROP TABLE IF EXISTS user_table;"
song_table_drop = "DROP TABLE IF EXISTS song_table;"
artist_table_drop = "DROP TABLE IF EXISTS artist_table;"
time_table_drop = "DROP TABLE IF EXISTS time_table;"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_events(
        artist VARCHAR, 
        auth VARCHAR, 
        firstName VARCHAR, 
        gender VARCHAR, 
        itemInSession INT,
        lastName VARCHAR, 
        length NUMERIC, 
        level VARCHAR, 
        location VARCHAR, 
        method VARCHAR,
        page VARCHAR, 
        registration VARCHAR, 
        sessionId INT, 
        song VARCHAR, 
        status INT,
        ts TIMESTAMP, 
        userAgent VARCHAR, 
        userId INT
    );
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs(
        num_songs INT,
        artist_id VARCHAR,
        artist_latitude VARCHAR,
        artist_longitude VARCHAR,
        artist_location VARCHAR,
        artist_name VARCHAR,
        song_id VARCHAR,
        title VARCHAR,
        duration NUMERIC,
        year INT
    );
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplay_table(
        songplay_id INT IDENTITY(1, 1) PRIMARY KEY,
        start_time TIMESTAMP NOT NULL,
        user_id INT NOT NULL REFERENCES user_table(user_id),
        level VARCHAR,
        song_id VARCHAR NOT NULL REFERENCES song_table(song_id),
        artist_id VARCHAR NOT NULL REFERENCES artist_table(artist_id),
        session_id INT NOT NULL REFERENCES time_table(session_id),
        location VARCHAR,
        user_agent VARCHAR
    );
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS user_table(
        user_id INT PRIMARY KEY,
        first_name VARCHAR NOT NULL,
        last_name VARCHAR,
        gender VARCHAR,
        level VARCHAR
    );
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS song_table(
        song_id VARCHAR PRIMARY KEY,
        title VARCHAR NOT NULL,
        artist_id VARCHAR NOT NULL,
        year INT,
        duration NUMERIC
    );
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artist_table(
        artist_id VARCHAR PRIMARY KEY,
        name VARCHAR NOT NULL,
        location VARCHAR,
        latitude VARCHAR,
        longitude VARCHAR
    );
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time_table(
        session_id INT PRIMARY KEY,
        start_time TIMESTAMP NOT NULL,
        hour INT,
        day INT,
        week INT,
        month INT,
        year INT ,
        weekday INT
    );
""")

# STAGING TABLES

staging_events_copy = ("""
    COPY staging_events 
    FROM {} 
    REGION 'us-west-2' 
    iam_role 'arn:aws:iam::301222643146:role/dwhRole'
    COMPUPDATE OFF STATUPDATE OFF
    FORMAT AS JSON {}
    TIMEFORMAT AS 'epochmillisecs';
""").format(config.get('S3','LOG_DATA'), 
            #config.get('IAM_ROLE','ARN'), 
            config.get('S3','LOG_JSONPATH')
           )

staging_songs_copy = ("""
    COPY staging_songs
    FROM {}
    REGION 'us-west-2' 
    iam_role 'arn:aws:iam::301222643146:role/dwhRole'
    COMPUPDATE OFF STATUPDATE OFF
    JSON 'auto'
    TIMEFORMAT AS 'epochmillisecs';
""").format(config.get('S3','SONG_DATA'))#, 
            #config.get('IAM_ROLE','ARN')
#            )

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplay_table(
        start_time, user_id, level, song_id, 
        artist_id, session_id, location, user_agent
    )
        SELECT DISTINCT
            ev.ts,
            ev.userID,
            ev.level,
            sg.song_id,
            sg.artist_id,
            ev.sessionId,
            ev.location,
            ev.userAgent
        FROM staging_events AS ev
        JOIN staging_songs AS sg
            ON (ev.artist = sg.artist_name)
            AND (ev.song = sg.title)
            AND (ev.length = sg.duration)
        WHERE ev.page = 'NextSong';
""")

user_table_insert = ("""
    INSERT INTO user_table (
        user_id, first_name, last_name, gender, level
    )
    SELECT DISTINCT
        userID, firstName, lastName, gender, level
    FROM
        staging_events
    WHERE
        page='NextSong';
""")

song_table_insert = ("""
    INSERT INTO song_table (
        song_id, title, artist_id, year, duration
    )
    SELECT DISTINCT
        song_id, title, artist_id, year, duration
    FROM
        staging_songs;
""")

artist_table_insert = ("""
    INSERT INTO artist_table (
        artist_id, name, location, latitude, longitude
    )
    SELECT DISTINCT
        artist_id, 
        artist_name, 
        artist_location, 
        artist_latitude, 
        artist_longitude
    FROM
        staging_songs;
""")

time_table_insert = ("""
    INSERT INTO time_table (
        session_id, start_time, hour, day, week, month, year, weekday
    )
    SELECT DISTINCT
        sessionId,
        ts,
        EXTRACT(HOUR FROM ts) AS hour,
        EXTRACT(DAY FROM ts) AS day,
        EXTRACT(WEEK FROM ts) AS week,
        EXTRACT(MONTH FROM ts) AS month,
        EXTRACT(YEAR FROM ts) AS year,
        EXTRACT(WEEKDAY FROM ts) AS weekday
    FROM
        staging_events;
""")
#     FROM (
#         SELECT DISTINCT 
#             ts, 
#             '1970-01-01'::date + ts/1000 * interval '1 second' as t_start_time
#     );
# """)

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

copy_table_queries = [staging_events_copy, staging_songs_copy]

insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
