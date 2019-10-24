
# Project4 - Data Warehouse 
#### A project from Udacity's Data Engineering course
The code was written along the lines of the default Jupyter notebook workspace provided by Udemy.

Author: [Davidson de Faria](https://github.com/davidsondefaria)

## Introduction
The goal of this project is to use Data Warehouse and AWS knowledge to create an ETL pipeline for a Redshift-hosted database.

For this we created tables to receive raw data from S3 and tables in the star schema for data organization. Finally, we execute SQL queries to perform data analysis.

## Code and Data Structure

The data structure is shown in the relationship image below.

IMAGE

The `staging_events` and` staging_songs` tables are used to store raw data, while the `songplay_table`,` user_table`, `song_table`,` artist_table` and `time_table` tables are part of the star schema. The `songplay_table` is the fact table and contains the IDs for the relationship to the dimensional tables.

### Querys
The querys are coded in the `sql_queries.py`.

### Create Tables
The code for creating the tables is in the `create_tables.py` file.


## Querys de teste
1. Quantas artistas tem no banco?
```
    SELECT count(*) FROM artist_table;
```
>**Answer:**
        10025


2. Quais músicas o usuário 97 ouviu? Qual nome do artista? Duração? Sessão (ordenado)?
```
    SELECT
        us.first_name,
        sp.session_id,
        sg.title,
        at.name,
        sg.duration
    FROM (SELECT session_id, song_id, user_id 
          FROM songplay_table
         ) AS sp
    JOIN (SELECT user_id, first_name
          FROM user_table
         ) AS us
    ON sp.user_id = us.user_id
    JOIN ((SELECT song_id, title, artist_id, duration 
           FROM song_table
          ) AS sg
          JOIN (SELECT name, artist_id 
                FROM artist_table
               ) AS at
          ON sg.artist_id = at.artist_id
         )
    ON sp.song_id=sg.song_id
    WHERE sp.user_id=97
    ORDER BY sp.session_id;
```
> **Answer:**
> 5 lines of 58

| first_name | session_id | title                                                | name                  | duration |
|------------|------------|------------------------------------------------------|-----------------------|----------|
| Kate       | 147        | Ezio In Florence                                     | Jesper Kyd            | 138      |
| Kate       | 147        | Girlfriend In A Coma                                 | The Smiths            | 123      |
| Kate       | 147        | Ezio In Florence                                     | Jesper Kyd            | 138      |
| Kate       | 147        | Girlfriend In A Coma                                 | The Smiths            | 123      |
| Kate       | 147        | You're The One                                       | Dwight Yoakam         | 239      |

3. De qual cidade é a banda 'Foo Fighters'?
```
    SELECT 
        at.location
    FROM (SELECT location, name
          FROM artist_table
         ) AS at
    WHERE at.name='Foo Fighters';
```
> **Answer:**
	 Seattle, WA

4. Qual a sessão com mais músicas? Qual o usuário?
```
    SELECT
        sp.session_id,
        us.first_name,
        us.last_name,
        count(*)
    FROM (SELECT session_id, user_id
          FROM songplay_table
         ) AS sp
    JOIN (SELECT user_id, first_name, last_name
          FROM user_table
         ) AS us
    ON sp.user_id = us.user_id
    GROUP BY
        sp.session_id,
        us.first_name,
        us.last_name
    ORDER BY count(*) DESC
    LIMIT 3;
```
> **Answer:**
		
| session_id | first_name | last_name | count |
|------------|------------|-----------|-------|
| 1041       | Chloe      | Cuevas    | 44    |
| 888        | Mohammad   | Rodriguez | 20    |
| 574        | Tegan      | Levine    | 20    |

5. Quem ouviu a música 'Fade To Black'? Quantas vezes? Em quais sessões? Nome(ordenado) e Sobrenome.
```
    SELECT
        us.first_name,
        us.last_name,
        sp.session_id,
        count(*)
    FROM (SELECT title, song_id
          FROM song_table
         ) AS sg
    JOIN ((SELECT song_id, session_id, user_id
           FROM songplay_table
          ) AS sp
          JOIN (SELECT user_id, first_name, last_name
                FROM user_table
               ) AS us
           ON sp.user_id = us.user_id
         )
    ON sg.song_id = sp.song_id
    WHERE sg.title='Fade To Black'
    GROUP BY
        sp.session_id,
        us.first_name,
        us.last_name
    ORDER BY first_name;
```
>**Answer:**

| first_name | last_name | session_id | count |
|------------|-----------|------------|-------|
| Avery      | Watkins   | 691        | 1     |
| Aiden      | Hess      | 869        | 1     |
| Sienna     | Colon     | 317        | 1     |

6. Quantas mulheres pagam?
```
    SELECT count(*)
    FROM (SELECT gender, level FROM user_table AS us)
    WHERE us.gender='M'
    AND us.level='paid'
```
>**Answer:**
		7

7. TOP 10 músicas mais ouvidas.
```
    SELECT
        sg.title,
        count(*)
    FROM (SELECT song_id
          FROM songplay_table
         ) AS sp
    JOIN (SELECT song_id, title
          FROM song_table
         ) AS sg
    ON sp.song_id = sg.song_id
    GROUP BY sg.title
    HAVING count(*) > 1
	ORDER BY count(*) DESC
    LIMIT 10;
```
>**Answer:** 

| title                                                | count |
|------------------------------------------------------|-------|
| You're The One                                       | 74    |
| I CAN'T GET STARTED                                  | 18    |
| Catch You Baby (Steve Pitron & Max Sanna Radio Edit) | 18    |
| Nothin' On You [feat. Bruno Mars] (Album Version)    | 16    |
| Hey Daddy (Daddy's Home)                             | 12    |
| Make Her Say                                         | 10    |
| Up Up & Away                                         | 10    |
| Unwell (Album Version)                               | 8     |
| Mr. Jones                                            | 8     |
| Supermassive Black Hole (Album Version)              | 8     |