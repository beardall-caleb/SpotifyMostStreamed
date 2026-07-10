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

    # For development
    conn.execute("DROP TABLE IF EXISTS artist_rankings")
    conn.execute("DROP TABLE IF EXISTS album_rankings")
    conn.execute("DROP TABLE IF EXISTS song_rankings")
    conn.execute("DROP TABLE IF EXISTS features")
    conn.execute("DROP TABLE IF EXISTS songs")
    conn.execute("DROP TABLE IF EXISTS albums")
    conn.execute("DROP TABLE IF EXISTS artists")

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
                CHECK (rank BETWEEN 1 AND 20),

            FOREIGN KEY (artist_id)
                REFERENCES artists(id)
        )
    """)

    # Album rankings table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS album_rankings (
            album_id INTEGER PRIMARY KEY,
            rank INTEGER NOT NULL UNIQUE
                CHECK (rank BETWEEN 1 AND 20),

            FOREIGN KEY (album_id)
                REFERENCES albums(id)
        )
    """)

    # Song rankings table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS song_rankings (
            song_id INTEGER PRIMARY KEY,
            rank INTEGER NOT NULL UNIQUE
                CHECK (rank BETWEEN 1 AND 20),

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


def get_featured_artists(conn, song_id):
    """Return a list of featured artist names for a song."""
    rows = conn.execute("""
        SELECT art.name
        FROM features AS f
        JOIN artists AS art
            ON f.featured_artist_id = art.id
        WHERE f.song_id = ?
        ORDER BY art.name
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
        # Identifies a song as a single if the song title and album title are the same
        if song_title != album_title:
            print(f"{rank}. {song_title} by {artist_name} from {album_title}")
        else:
            print(f"{rank}. {song_title} by {artist_name} as a single")


def display_main_menu():
    print("""
Spotify's Most Streamed Music of All Time
-----------------------------------------
1. View the Top 20 Most Streamed Artists
2. View the Top 20 Most Streamed Albums
3. View the Top 20 Most Streamed Songs
4. Come Back Later
""")
    

def main():
    conn = create_connection()

    try:
        create_tables(conn)
        seed_database(conn)

        while True:
            display_main_menu()
            choice = input("What would you like to do?: ").strip()

            if choice == "1":
                display_top_20_artists(conn)
            elif choice == "2":
                display_top_20_albums(conn)
            elif choice == "3":
                display_top_20_songs(conn)
            elif choice == "4":
                print("See you soon!")
                break
            else:
                print("Please choose a valid option.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()