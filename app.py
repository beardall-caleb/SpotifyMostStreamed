import sqlite3

DATABASE_NAME = "moststreamed.db"

def create_connection():
    """Create and connect to the SQLite database."""
    conn = sqlite3.connect(DATABASE_NAME)

    # Enforce foreign-key constraints for this connection
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def create_tables(conn):
    """Reset and create the app's database tables."""

    # Artists table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS artists (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        )
    """)

    # Albums table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS albums (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            artist_id INTEGER NOT NULL,
            release_year INTEGER,

            FOREIGN KEY (artist_id)
                REFERENCES artists(id),

            UNIQUE (title, artist_id)
        )
    """)

    # Songs table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            album_id INTEGER NOT NULL,

            FOREIGN KEY (album_id)
                REFERENCES albums(id),

            UNIQUE (title, album_id)
        )
    """)

    # Features table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS features (
            song_id INTEGER NOT NULL,
            featured_artist_id INTEGER NOT NULL,

            PRIMARY KEY (song_id, featured_artist_id),

            FOREIGN KEY (song_id)
                REFERENCES songs(id),

            FOREIGN KEY (featured_artist_id)
                REFERENCES artists(id)
        )
    """)

    # Artist rankings table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS artist_rankings (
            artist_id INTEGER PRIMARY KEY,
            rank INTEGER NOT NULL UNIQUE
                CHECK (rank BETWEEN 1 AND 20 OR rank = 99),

            FOREIGN KEY (artist_id)
                REFERENCES artists(id)
        )
    """)

    # Album rankings table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS album_rankings (
            album_id INTEGER PRIMARY KEY,
            rank INTEGER NOT NULL UNIQUE
                CHECK (rank BETWEEN 1 AND 20 OR rank = 99),

            FOREIGN KEY (album_id)
                REFERENCES albums(id)
        )
    """)

    # Song rankings table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS song_rankings (
            song_id INTEGER PRIMARY KEY,
            rank INTEGER NOT NULL UNIQUE
                CHECK (rank BETWEEN 1 AND 20 OR rank = 99),

            FOREIGN KEY (song_id)
                REFERENCES songs(id)
        )
    """)

    conn.commit()


def seed_database(conn):
    """
    Insert the app's initial data.

    Data is inserted in dependency order:
    artists -> albums -> songs -> features -> rankings
    """
    seed_artists(conn)
    seed_albums(conn)
    seed_songs(conn)
    seed_features(conn)
    seed_rankings(conn)

    conn.commit()


def seed_artists(conn):
    """
    Seed the artists table.

    This includes artists from the artist rankings, album rankings, song rankings,
    and featured artists so related records can be joined correctly.
    """
    artists = [
        ("Taylor Swift",),
        ("Bad Bunny",),
        ("Drake",),
        ("The Weeknd",),
        ("Ariana Grande",),
        ("Ed Sheeran",),
        ("Justin Bieber",),
        ("Billie Eilish",),
        ("Eminem",),
        ("Kanye West",),
        ("Travis Scott",),
        ("BTS",),
        ("Post Malone",),
        ("Bruno Mars",),
        ("J Balvin",),
        ("Rihanna",),
        ("Coldplay",),
        ("Kendrick Lamar",),
        ("Future",),
        ("Juice WRLD",),
        ("Olivia Rodrigo",),
        ("SZA",),
        ("Arctic Monkeys",),
        ("Dua Lipa",),
        ("XXXTENTACION",),
        ("KAROL G",),
        ("The Neighbourhood",),
        ("Harry Styles",),
        ("Lewis Capaldi",),
        ("The Kid LAROI",),
        ("Imagine Dragons",),
        ("Glass Animals",),
        ("Lord Huron",),
        ("The Chainsmokers",),
        ("Vance Joy",),
        ("Lady Gaga",),
        ("Daft Punk",),
        ("Swae Lee",),
        ("Wizkid",),
        ("Kyla",),
        ("Khalid",),
        ("Halsey",)
    ]

    conn.executemany("""
        INSERT INTO artists (name)
        VALUES (?)
    """, artists)


def seed_albums(conn):
    """
    Seed the albums table.

    Each album is connected to one primary artist.
    Artist IDs are looked up by name instead of being hard-coded.
    """
    albums = [
        ("Un Verano Sin Ti", get_artist_id(conn, "Bad Bunny"), 2022),
        ("Starboy", get_artist_id(conn, "The Weeknd"), 2016),
        ("÷ (Deluxe)", get_artist_id(conn, "Ed Sheeran"), 2017),
        ("SOUR", get_artist_id(conn, "Olivia Rodrigo"), 2021),
        ("After Hours", get_artist_id(conn, "The Weeknd"), 2020),
        ("SOS", get_artist_id(conn, "SZA"), 2022),
        ("Hollywood's Bleeding", get_artist_id(conn, "Post Malone"), 2019),
        ("Lover", get_artist_id(conn, "Taylor Swift"), 2019),
        ("AM", get_artist_id(conn, "Arctic Monkeys"), 2013),
        ("WHEN WE ALL FALL ASLEEP, WHERE DO WE GO?", get_artist_id(conn, "Billie Eilish"), 2019),
        ("Future Nostalgia", get_artist_id(conn, "Dua Lipa"), 2020),
        ("beerbongs & bentleys", get_artist_id(conn, "Post Malone"), 2018),
        ("?", get_artist_id(conn, "XXXTENTACION"), 2018),
        ("MAÑANA SERÁ BONITO", get_artist_id(conn, "KAROL G"), 2023),
        ("YHLQMDLG", get_artist_id(conn, "Bad Bunny"), 2020),
        ("Doo-Wops & Hooligans", get_artist_id(conn, "Bruno Mars"), 2010),
        ("Views", get_artist_id(conn, "Drake"), 2016),
        ("Midnights", get_artist_id(conn, "Taylor Swift"), 2022),
        ("Scorpion", get_artist_id(conn, "Drake"), 2018),
        ("Beauty Behind The Madness", get_artist_id(conn, "The Weeknd"), 2015),
        ("I Love You.", get_artist_id(conn, "The Neighbourhood"), 2013),
        ("Harry's House", get_artist_id(conn, "Harry Styles"), 2022),
        ("Divinely Uninspired To A Hellish Extent", get_artist_id(conn, "Lewis Capaldi"), 2019),
        ("Spider-Man: Into the Spider-Verse", get_artist_id(conn, "Post Malone"), 2018),
        ("STAY (with Justin Bieber)", get_artist_id(conn, "The Kid LAROI"), 2021),
        ("Evolve", get_artist_id(conn, "Imagine Dragons"), 2017),
        ("Dreamland", get_artist_id(conn, "Glass Animals"), 2020),
        ("lovely (with Khalid)", get_artist_id(conn, "Billie Eilish"), 2018),
        ("Parachutes", get_artist_id(conn, "Coldplay"), 2000),
        ("Strange Trails", get_artist_id(conn, "Lord Huron"), 2015),
        ("Closer", get_artist_id(conn, "The Chainsmokers"), 2016),
        ("HIT ME HARD AND SOFT", get_artist_id(conn, "Billie Eilish"), 2024),
        ("Dream Your Life Away", get_artist_id(conn, "Vance Joy"), 2014),
        ("Die With A Smile", get_artist_id(conn, "Lady Gaga"), 2024),
    ]

    conn.executemany("""
        INSERT INTO albums (title, artist_id, release_year)
        VALUES (?, ?, ?)
    """, albums)


def seed_songs(conn):
    """
    Seed the songs table.

    Each song is connected to an album. The album is connected to an artist,
    allowing songs, albums, and artists to be joined together.
    Album IDs are looked up by artist name and album title instead of being hard-coded.
    """
    songs = [
        ("Blinding Lights", get_album_id(conn, "The Weeknd", "After Hours")),
        ("Shape of You", get_album_id(conn, "Ed Sheeran", "÷ (Deluxe)")),
        ("Sweater Weather", get_album_id(conn, "The Neighbourhood", "I Love You.")),
        ("Starboy", get_album_id(conn, "The Weeknd", "Starboy")),
        ("As It Was", get_album_id(conn, "Harry Styles", "Harry's House")),
        ("Someone You Loved", get_album_id(conn, "Lewis Capaldi", "Divinely Uninspired To A Hellish Extent")),
        ("Sunflower", get_album_id(conn, "Post Malone", "Spider-Man: Into the Spider-Verse")),
        ("One Dance", get_album_id(conn, "Drake", "Views")),
        ("Perfect", get_album_id(conn, "Ed Sheeran", "÷ (Deluxe)")),
        ("STAY (with Justin Bieber)", get_album_id(conn, "The Kid LAROI", "STAY (with Justin Bieber)")),
        ("Believer", get_album_id(conn, "Imagine Dragons", "Evolve")),
        ("I Wanna Be Yours", get_album_id(conn, "Arctic Monkeys", "AM")),
        ("Heat Waves", get_album_id(conn, "Glass Animals", "Dreamland")),
        ("lovely (with Khalid)", get_album_id(conn, "Billie Eilish", "lovely (with Khalid)")),
        ("Yellow", get_album_id(conn, "Coldplay", "Parachutes")),
        ("The Night We Met", get_album_id(conn, "Lord Huron", "Strange Trails")),
        ("Closer", get_album_id(conn, "The Chainsmokers", "Closer")),
        ("BIRDS OF A FEATHER", get_album_id(conn, "Billie Eilish", "HIT ME HARD AND SOFT")),
        ("Riptide", get_album_id(conn, "Vance Joy", "Dream Your Life Away")),
        ("Die With A Smile", get_album_id(conn, "Lady Gaga", "Die With A Smile"))
    ]

    conn.executemany("""
        INSERT INTO songs (title, album_id)
        VALUES (?, ?)
    """, songs)


def seed_features(conn):
    """
    Seed the features table.

    The features table uses song ID and featured artist ID as a composite key,
    allowing one song to have multiple featured artists while preventing duplicates.
    """
    features = [
        (get_song_id(conn, "The Weeknd", "Starboy"), get_artist_id(conn, "Daft Punk")),
        (get_song_id(conn, "Post Malone", "Sunflower"), get_artist_id(conn, "Swae Lee")),
        (get_song_id(conn, "Drake", "One Dance"), get_artist_id(conn, "Wizkid")),
        (get_song_id(conn, "Drake", "One Dance"), get_artist_id(conn, "Kyla")),
        (get_song_id(conn, "The Kid LAROI", "STAY (with Justin Bieber)"), get_artist_id(conn, "Justin Bieber")),
        (get_song_id(conn, "Billie Eilish", "lovely (with Khalid)"), get_artist_id(conn, "Khalid")),
        (get_song_id(conn, "The Chainsmokers", "Closer"), get_artist_id(conn, "Halsey")),
        (get_song_id(conn, "Lady Gaga", "Die With A Smile"), get_artist_id(conn, "Bruno Mars")),
    ]

    conn.executemany("""
        INSERT INTO features (song_id, featured_artist_id)
        VALUES (?, ?)
    """, features)


def seed_rankings(conn):
    """
    Seed the rankings tables.
    """
    artist_rankings = [
        (get_artist_id(conn, "Taylor Swift"), 1),
        (get_artist_id(conn, "Bad Bunny"), 2),
        (get_artist_id(conn, "Drake"), 3),
        (get_artist_id(conn, "The Weeknd"), 4),
        (get_artist_id(conn, "Ariana Grande"), 5),
        (get_artist_id(conn, "Ed Sheeran"), 6),
        (get_artist_id(conn, "Justin Bieber"), 7),
        (get_artist_id(conn, "Billie Eilish"), 8),
        (get_artist_id(conn, "Eminem"), 9),
        (get_artist_id(conn, "Kanye West"), 10),
        (get_artist_id(conn, "Travis Scott"), 11),
        (get_artist_id(conn, "BTS"), 12),
        (get_artist_id(conn, "Post Malone"), 13),
        (get_artist_id(conn, "Bruno Mars"), 14),
        (get_artist_id(conn, "J Balvin"), 15),
        (get_artist_id(conn, "Rihanna"), 16),
        (get_artist_id(conn, "Coldplay"), 17),
        (get_artist_id(conn, "Kendrick Lamar"), 18),
        (get_artist_id(conn, "Future"), 19),
        (get_artist_id(conn, "Juice WRLD"), 20)
    ]

    conn.executemany("""
        INSERT INTO artist_rankings (artist_id, rank)
        VALUES (?, ?)
    """, artist_rankings)

    album_rankings = [
        (get_album_id(conn, "Bad Bunny", "Un Verano Sin Ti"), 1),
        (get_album_id(conn, "The Weeknd", "Starboy"), 2),
        (get_album_id(conn, "Ed Sheeran", "÷ (Deluxe)"), 3),
        (get_album_id(conn, "Olivia Rodrigo", "SOUR"), 4),
        (get_album_id(conn, "The Weeknd", "After Hours"), 5),
        (get_album_id(conn, "SZA", "SOS"), 6),
        (get_album_id(conn, "Post Malone", "Hollywood's Bleeding"), 7),
        (get_album_id(conn, "Taylor Swift", "Lover"), 8),
        (get_album_id(conn, "Arctic Monkeys", "AM"), 9),
        (get_album_id(conn, "Billie Eilish", "WHEN WE ALL FALL ASLEEP, WHERE DO WE GO?"), 10),
        (get_album_id(conn, "Dua Lipa", "Future Nostalgia"), 11),
        (get_album_id(conn, "Post Malone", "beerbongs & bentleys"), 12),
        (get_album_id(conn, "XXXTENTACION", "?"), 13),
        (get_album_id(conn, "KAROL G", "MAÑANA SERÁ BONITO"), 14),
        (get_album_id(conn, "Bad Bunny", "YHLQMDLG"), 15),
        (get_album_id(conn, "Bruno Mars", "Doo-Wops & Hooligans"), 16),
        (get_album_id(conn, "Drake", "Views"), 17),
        (get_album_id(conn, "Taylor Swift", "Midnights"), 18),
        (get_album_id(conn, "Drake", "Scorpion"), 19),
        (get_album_id(conn, "The Weeknd", "Beauty Behind The Madness"), 20),
    ]

    conn.executemany("""
        INSERT INTO album_rankings (album_id, rank)
        VALUES (?, ?) 
    """, album_rankings)

    song_rankings = [
        (get_song_id(conn, "The Weeknd", "Blinding Lights"), 1),
        (get_song_id(conn, "Ed Sheeran", "Shape of You"), 2),
        (get_song_id(conn, "The Neighbourhood", "Sweater Weather"), 3),
        (get_song_id(conn, "The Weeknd", "Starboy"), 4),
        (get_song_id(conn, "Harry Styles", "As It Was"), 5),
        (get_song_id(conn, "Lewis Capaldi", "Someone You Loved"), 6),
        (get_song_id(conn, "Post Malone", "Sunflower"), 7),
        (get_song_id(conn, "Drake", "One Dance"), 8),
        (get_song_id(conn, "Ed Sheeran", "Perfect"), 9),
        (get_song_id(conn, "The Kid LAROI", "STAY (with Justin Bieber)"), 10),
        (get_song_id(conn, "Imagine Dragons", "Believer"), 11),
        (get_song_id(conn, "Arctic Monkeys", "I Wanna Be Yours"), 12),
        (get_song_id(conn, "Glass Animals", "Heat Waves"), 13),
        (get_song_id(conn, "Billie Eilish", "lovely (with Khalid)"), 14),
        (get_song_id(conn, "Coldplay", "Yellow"), 15),
        (get_song_id(conn, "Lord Huron", "The Night We Met"), 16),
        (get_song_id(conn, "The Chainsmokers", "Closer"), 17),
        (get_song_id(conn, "Billie Eilish", "BIRDS OF A FEATHER"), 18),
        (get_song_id(conn, "Vance Joy", "Riptide"), 19),
        (get_song_id(conn, "Lady Gaga", "Die With A Smile"), 20),
    ]

    conn.executemany("""
        INSERT INTO song_rankings (song_id, rank)
        VALUES (?, ?)    
    """, song_rankings)


def get_artist_id(conn, name):
    """Return the ID for an artist by name."""
    row = conn.execute("""
        SELECT id
        FROM artists
        WHERE name = ?   
    """, (name,)).fetchone()

    if row is None:
        raise ValueError(f"Artist not found: {name}")
    
    return row[0]


def get_album_id(conn, artist_name, title):
    """Return the ID for an album by artist name and title."""
    row = conn.execute("""
        SELECT alb.id
        FROM albums AS alb
        JOIN artists AS art
            ON alb.artist_id = art.id
        WHERE art.name = ?
            AND alb.title = ?
    """, (artist_name, title)).fetchone()

    if row is None:
        raise ValueError(f"Album not found: {title} by {artist_name}")

    return row[0]


def get_song_id(conn, artist_name, title):
    """Return the ID for a song by artist name and title."""
    row = conn.execute("""
        SELECT s.id
        FROM songs AS s
        JOIN albums AS alb
            ON s.album_id = alb.id
        JOIN artists AS art
            ON alb.artist_id = art.id
        WHERE art.name = ?
            AND s.title = ?            
    """, (artist_name, title)).fetchone()

    if row is None:
        raise ValueError(f"Song not found: {title} by {artist_name}")
    
    return row[0]


def get_object_rank(conn, table_name, id_column, object_id):
    """
    Return the current rank for an artist, album, or song.

    Requires the ranking table name, foreign-key column name, and the object's ID.
    """
    row = conn.execute(f"""
        SELECT rank
        FROM {table_name}
        WHERE {id_column} = ?
    """, (object_id,)).fetchone()

    if row is None:
        return None
    
    return row[0]


def shift_rankings_down(conn, table_name, id_column, start_rank, end_rank):
    """
    Move rankings down by one.

    Used when inserting or moving an item into a higher position.
    """
    rows_to_shift = conn.execute(f"""
        SELECT {id_column}, rank
        FROM {table_name}
        WHERE rank >= ?
            AND rank < ?
        ORDER BY rank DESC
    """, (start_rank, end_rank)).fetchall()

    for ranked_object_id, current_rank in rows_to_shift:
        conn.execute(f"""
            UPDATE {table_name}
            SET rank = ?
            WHERE {id_column} = ?
        """, (current_rank + 1, ranked_object_id))


def shift_rankings_up(conn, table_name, id_column, start_rank, end_rank):
    """
    Move rankings up by one.

    Used when deleting an item or moving an item to a lower position.
    """
    rows_to_shift = conn.execute(f"""
        SELECT {id_column}, rank
        FROM {table_name}
        WHERE rank > ?
            AND rank <= ?
        ORDER BY rank ASC
    """, (start_rank, end_rank)).fetchall()

    for ranked_object_id, current_rank in rows_to_shift:
        conn.execute(f"""
            UPDATE {table_name}  
            SET rank = ?
            WHERE {id_column} = ?
        """, (current_rank - 1, ranked_object_id))


def add_ranking(conn, ranking_type):
    print("""
Add Ranking
-----------
""")
    # Get or create the artist, album, or song to be ranked.
    # Then store its ID so it can be added to the correct rankings table.

    # Add artists
    if ranking_type == "artists":
        ranking_table = "artist_rankings"
        id_column = "artist_id"

        artist_name = input("Which artist would you like to add to the rankings? ").strip()
        display_name = artist_name

        try:
            object_id = get_artist_id(conn, artist_name)
        except ValueError:
            create_object = input(f"{artist_name} is not in the database. Add this artist? (yes/no): ").strip().lower()

            if create_object != "yes":
                print(f"{artist_name} was not added.")
                return

            conn.execute("""
                INSERT INTO artists (name)
                VALUES (?)
            """, (artist_name,))

            object_id = get_artist_id(conn, artist_name)
    
    # Add albums
    elif ranking_type == "albums":
        ranking_table = "album_rankings"
        id_column = "album_id"

        album_title = input("Which album would you like to add to the rankings? ").strip()
        artist_name = input("Who is the album by? ").strip()

        display_name = f"{album_title} by {artist_name}"

        try:
            object_id = get_album_id(conn, artist_name, album_title)
        except ValueError:
            create_object = input(f"{display_name} is not in the database. Add this album? (yes/no): ").strip().lower()

            if create_object != "yes":
                print(f"{display_name} was not added.")
                return

            try:
                artist_id = get_artist_id(conn, artist_name)
            except ValueError:
                print(f"{artist_name} is not in the database. Add the artist first.")
                return

            while True:
                try:
                    album_year = int(input(f"What year was {album_title} released? ").strip())
                    break
                except ValueError:
                    print("Please enter a whole number.")

            conn.execute("""
                INSERT INTO albums (title, artist_id, release_year)
                VALUES (?, ?, ?)
            """, (album_title, artist_id, album_year))

            object_id = get_album_id(conn, artist_name, album_title)

    # Add songs
    else:
        ranking_table = "song_rankings"
        id_column = "song_id"

        song_title = input("Which song would you like to add to the rankings? ").strip()
        album_title = input("Which album was the song released under? ").strip()
        artist_name = input("Who is the song by? ").strip()

        display_name = f"{song_title} by {artist_name}"

        try:
            object_id = get_song_id(conn, artist_name, song_title)
        except ValueError:
            create_object = input(f"{display_name} is not in the database. Add this song? (yes/no): ").strip().lower()

            if create_object != "yes":
                print(f"{display_name} was not added.")
                return
            
            try:
                album_id = get_album_id(conn, artist_name, album_title)
            except ValueError:
                print(f"{artist_name} or {album_title} is not in the database. Add both first.")
                return
            
            conn.execute("""
                INSERT INTO songs (title, album_id)
                VALUES (?, ?)          
            """, (song_title, album_id))

            object_id = get_song_id(conn, artist_name, song_title)

    # Call the get_object_rank function to get the object's rank.
    current_rank = get_object_rank(conn, ranking_table, id_column, object_id)

    # Hanle objects that are already ranked
    if current_rank is not None:
        print(f"{display_name} is already ranked #{current_rank}.")
        return
    
    while True:
        try:
            new_rank = int(input(f"What rank should {display_name} have? ").strip())
            break
        except ValueError:
            print("Please enter a number between 1 and 20.")
    
    if new_rank not in range(1, 21):
        print(f"Invalid input: {new_rank}")
        return
    
    # Delete the row ranked 20 so it is not moved out of bounds
    conn.execute(f"""
        DELETE FROM {ranking_table}
        WHERE rank = 20
    """)

    # Shift affected items down.
    shift_rankings_down(conn, ranking_table, id_column, new_rank, 20)

    # Add the object to the table at the specified rank
    conn.execute(f"""
        INSERT INTO {ranking_table} ({id_column}, rank)
        VALUES (?, ?)
    """, (object_id, new_rank))

    conn.commit()

    print(f"{display_name} is now ranked #{new_rank}.")


def update_ranking(conn, ranking_type):
    print("""
Update Ranking
-------------- 
""")
    
    # Get the ID of the artist, album, or song to update.
    if ranking_type == "artists":
        table_name = "artist_rankings"
        id_column = "artist_id"

        artist_name = input("Whose ranking would you like to update? ").strip()

        try:
            object_id = get_artist_id(conn, artist_name)
        except ValueError:
            print(f"Invalid input: {artist_name}")
            return
        
        display_name = artist_name

    elif ranking_type == "albums":
        table_name = "album_rankings"
        id_column = "album_id"

        album_title = input("Which album's ranking would you like to update? ").strip()
        artist_name = input("Who is the album by? ").strip()

        try:
            object_id = get_album_id(conn, artist_name, album_title)
        except ValueError:
            print(f"Invalid input: {album_title} by {artist_name}")
            return
        
        display_name = f"{album_title} by {artist_name}"

    else:
        table_name = "song_rankings"
        id_column = "song_id"

        song_title = input("Which song's ranking would you like to update? ").strip()
        artist_name = input("Who is the song by? ").strip()

        try:
            object_id = get_song_id(conn, artist_name, song_title)
        except ValueError:
            print(f"Invalid input: {song_title} by {artist_name}")
            return

        display_name = f"{song_title} by {artist_name}"

    # Call the get_object_rank function to get the object's rank.
    current_rank = get_object_rank(conn, table_name, id_column, object_id)

    if current_rank is None:
        print(f"{display_name} is not currently ranked.")
        return

    noun = "their" if ranking_type == "artists" else "its"

    while True:
        print(f"{display_name} is currently ranked {current_rank}")

        # Convert the user's input to an integer.
        try:
            updated_rank = int(input(f"What should {noun} ranking be? ").strip())
        except ValueError:
            print("Please enter a number between 1 and 20.")
            return

        if updated_rank == current_rank:
            print("Rank unchanged.")
            return
        
        elif updated_rank not in range(1, 21):
            print(f"Invalid input: {updated_rank}")
            return
        
        else:
            # Move selected item out of the way temporarily.
            conn.execute(f"""
                UPDATE {table_name}
                SET rank = 99
                WHERE {id_column} = ?
            """, (object_id,))

            if updated_rank < current_rank:
                # Shift affected items down.
                shift_rankings_down(conn, table_name, id_column, updated_rank, current_rank)

            elif updated_rank > current_rank:
                # Shift affected items up.
                shift_rankings_up(conn, table_name, id_column, current_rank, updated_rank)

            # Put selected item into its new rank.
            conn.execute(f"""
                UPDATE {table_name}
                SET rank = ?
                WHERE {id_column} = ?
            """, (updated_rank, object_id))

            conn.commit()
            break

    print(f"{display_name} is now ranked #{updated_rank}.")


def delete_ranking(conn, ranking_type):
    print("""
Remove Ranking
--------------
""")

    # Get the ID of the artist, album, or song to remove from the rankings.
    if ranking_type == "artists":
        table_name = "artist_rankings"
        id_column = "artist_id"

        artist_name = input("Which artist would you like to remove from the rankings? ").strip()

        try:
            object_id = get_artist_id(conn, artist_name)
        except ValueError:
            print(f"Invalid input: {artist_name}")
            return

        display_name = artist_name

    elif ranking_type == "albums":
        table_name = "album_rankings"
        id_column = "album_id"

        album_title = input("Which album would you like to remove from the rankings? ").strip()
        artist_name = input("Who is the album by? ").strip()

        try:
            object_id = get_album_id(conn, artist_name, album_title)
        except ValueError:
            print(f"Invalid input: {album_title} by {artist_name}")
            return

        display_name = f"{album_title} by {artist_name}"

    else:
        table_name = "song_rankings"
        id_column = "song_id"

        song_title = input("Which song would you like to remove from the rankings? ").strip()
        artist_name = input("Who is the song by? ").strip()

        try:
            object_id = get_song_id(conn, artist_name, song_title)
        except ValueError:
            print(f"Invalid input: {song_title} by {artist_name}")
            return

        display_name = f"{song_title} by {artist_name}"

    # Call the get_object_rank function to get the object's rank.
    deleted_rank = get_object_rank(conn, table_name, id_column, object_id)

    if deleted_rank is None:
        print(f"{display_name} is not currently ranked.")
        return

    conn.execute(f"""
        DELETE FROM {table_name}
        WHERE {id_column} = ?
    """, (object_id,))

    # Shift all the items that were below the object up by one.
    shift_rankings_up(conn, table_name, id_column, deleted_rank, 20)

    # Commit changes.
    conn.commit()

    print(f"{display_name} has been removed from the ranking.")
    

def get_featured_artists(conn, song_id):
    """Return a list of featured artist names for a song."""
    rows = conn.execute("""
        SELECT art.name
        FROM features AS f
        JOIN artists AS art
            ON f.featured_artist_id = art.id
        WHERE f.song_id = ?
    """, (song_id,)).fetchall()

    return [row[0] for row in rows]


def display_top_20_artists(conn):
    """
    Display the top 20 most streamed artists.

    The query joins artist_rankings with artists using the artist ID.
    """
    rows = conn.execute("""
        SELECT
            r.rank,
            a.name
        FROM artist_rankings AS r
        JOIN artists AS a
            ON r.artist_id = a.id
        ORDER BY r.rank
    """).fetchall()

    print("\nSpotify's Top 20 Most Streamed Artists:")

    for rank, name in rows:
        print(f"{rank}. {name}")


def display_top_20_albums(conn):
    """
    Display the top 20 most streamed albums.

    The query:
        * Joins album_rankings with albums using the album ID
        * Joins albums with artists using the artist ID
    """
    rows = conn.execute("""
        SELECT
            r.rank,
            alb.title,
            art.name
        FROM album_rankings AS r
        JOIN albums AS alb
            ON r.album_id = alb.id
        JOIN artists AS art
            ON art.id = alb.artist_id
        ORDER BY r.rank
    """).fetchall()

    print("\nSpotify's Top 20 Most Streamed Albums:")

    for rank, album_title, artist_name in rows:
        print(f"{rank}. {album_title} by {artist_name}")


def display_top_20_songs(conn):
    """
    Display the top 20 most streamed songs.

    The query:
        * Joins song_rankings with songs using the song ID
        * Joins songs with albums using the album ID
        * Joins albums with artists using the artist ID
    """
    rows = conn.execute("""
        SELECT
            s.id,
            r.rank,
            s.title,
            alb.title,
            art.name
        FROM song_rankings AS r
        JOIN songs AS s
            ON r.song_id = s.id
        JOIN albums AS alb
            ON s.album_id = alb.id
        JOIN artists AS art
            ON alb.artist_id = art.id
        ORDER BY r.rank
    """).fetchall()

    print("\nSpotify's Top 20 Most Streamed Songs:")

    for song_id, rank, song_title, album_title, artist_name in rows:
        featured_artists = get_featured_artists(conn, song_id)

        # Start building the display line with the rank, song title, and primary artist.
        line = f"{rank}. {song_title} by {artist_name}"

        # Add featured artists when the song has one or more features.
        if len(featured_artists) == 1:
            line += f" featuring {featured_artists[0]}"
        elif len(featured_artists) == 2:
            line += f" featuring {featured_artists[0]} and {featured_artists[1]}"
        elif len(featured_artists) > 2:
            line += f" featuring {', '.join(featured_artists[:-1])}, and {featured_artists[-1]}"

        # Treat the song as a single when the song title and album title match.
        if song_title != album_title:
            line += f" from {album_title}"
        else:
            line += " as a single"

        print(line)


def edit_rankings(conn):
    while True:
        display_ranking_type_menu()
        ranking_type_choice = input("Which ranking list would you like to edit? ").strip()

        if ranking_type_choice == "1":
            ranking_type = "artists"
        elif ranking_type_choice == "2":
            ranking_type = "albums"
        elif ranking_type_choice == "3":
            ranking_type = "songs"
        elif ranking_type_choice == "4":
            return
        else:
            print("Please choose a valid option.")
            continue

        while True:
            display_ranking_action_menu(ranking_type)
            action_choice = input("Choose an action: ").strip()

            if action_choice == "1":
                add_ranking(conn, ranking_type)
                return
            elif action_choice == "2":
                update_ranking(conn, ranking_type)
                return
            elif action_choice == "3":
                delete_ranking(conn, ranking_type)
                return
            elif action_choice == "4":
                break
            else:
                print("Please choose a valid option.")
    
    
def display_ranking_action_menu(ranking_type):
    display_name = ranking_type.capitalize()

    print(f"""
Edit Top 20 {display_name}
--------------------------
1. Add a Ranking
2. Update a Ranking
3. Remove a Ranking
4. Return to Ranking List Menu   
""")

def display_ranking_type_menu():
    print("""
Edit Rankings
---------------------
1. Artists
2. Albums
3. Songs
4. Return to Main Menu
""")


def display_main_menu():
    print("""
Spotify's Most Streamed Music of All Time
-----------------------------------------
1. View Top 20 Artists
2. View Top 20 Albums
3. View Top 20 Songs
4. Edit Rankings
5. Exit
""")
    

def main():
    conn = create_connection()

    try:
        create_tables(conn)
        seed_database(conn)

        while True:
            display_main_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                display_top_20_artists(conn)
            elif choice == "2":
                display_top_20_albums(conn)
            elif choice == "3":
                display_top_20_songs(conn)
            elif choice == "4":
                edit_rankings(conn)
            elif choice == "5":
                print("See you soon!")
                break
            else:
                print("Please choose a valid option.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()