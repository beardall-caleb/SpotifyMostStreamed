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
    artists -> albums -> songs -> rankings
    """
    seed_artists(conn)
    seed_albums(conn)
    seed_songs(conn)
    #seed_rankings(conn)

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
        ("WizKid",),
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

    Each album is connected to one primary artists.
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
    artist_id = get_artist_id(conn, artist_name)

    row = conn.execute("""
        SELECT id
        FROM albums
        WHERE artist_id = ?
            AND title = ?   
    """, (artist_id, title)).fetchone()

    if row is None:
        raise ValueError(f"Album not found: {title} by {artist_name}")
    
    return row[0]

def main():
    conn = create_connection()

    try:
        create_tables(conn)
        seed_database(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()