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
    Insert the app's initial data in the following order due to dependencies:
    Artists -> albums -> songs -> rankings
    """
    seed_artists(conn)
    #seed_albums(conn)
    #seed_songs(conn)
    #seed_rankings(conn)

    conn.commit()


def seed_artists(conn):
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
    ]

    conn.executemany("""
        INSERT INTO artists (name)
        VALUES (?)
    """, artists)


def main():
    conn = create_connection()

    try:
        create_tables(conn)
        seed_database(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()