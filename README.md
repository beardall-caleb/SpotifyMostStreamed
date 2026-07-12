# SpotifyMostStreamed

I am a music junkie. I love music and often have Spotify playing in the background while I code. I am constantly searching artist, album, and song rankings to discover new music.

When Spotify turned 20 years old, they released lists of the top 20 most-streamed artists, albums, and songs. As one might expect, many of the most-streamed songs came from the most-streamed albums, and many of the most-streamed albums were created by the most-streamed artists. Because of my background in data analytics and experience working with SQL, I thought this data would make a great mini database project. That idea led to the creation of this application.

While I have some experience working with T-SQL, I have not had many opportunities to pair traditional programming in an object-oriented language like Python with a relational database. This project gave me the opportunity to sharpen my programming skills while also practicing relational database design, table relationships, joins, and CRUD operations.

[Software Demo Video](https://youtu.be/zQNLQ8CnODo)

# Relational Database

The database schema includes three primary tables: artists, albums, and songs. Each of these tables has a related rankings table used to store its top 20 ranking data. The database also includes a features table, which connects songs to featured artists.

The artists table is the simplest table. It contains an id primary key and a name column. The albums table is connected to the artists table through an artist_id foreign key. It contains an id primary key, a title, an artist_id, and a release_year. The songs table is connected to the albums table through an album_id foreign key. It contains an id primary key, a title, and an album_id.

To display the top 20 songs with their albums and artists, the application joins the songs, albums, and artists tables together. The rankings tables are then joined to their related primary tables to display the ranked artist, album, and song lists in order.

# Development Environment

This application was created using Python and SQLite. It uses Python’s built-in sqlite3 module, so no external database package was required. Because SQLite is serverless and self-contained, the database can be created and managed directly from the Python application.

# Useful Websites

- [GeeksforGeeks Python SQLite](https://www.geeksforgeeks.org/python/python-sqlite/)
- [SQLite Official Cite](https://www.sqlite.org/index.html)
- [Spotify at 20: The Most Streamed Music, Podcasts, and Audiobooks of All Time](https://newsroom.spotify.com/2026-04-23/spotify-20-most-streamed-music-podcasts-audiobooks/)

# Future Work

- Add more complete create functionality for related records. Currently, when users add an artist ranking, they can add a new artist to the artists table if that artist does not already exist. This is simpler because the artists table does not depend on any foreign keys. In the future, I would like users to be able to add missing artists and albums while adding album rankings. I would also like users to be able to add missing artists, albums, and songs while adding song rankings. Because albums and songs depend on foreign keys, these records must be created in the correct order before they can be added to the rankings tables.

- Use the release_year column in the albums table to support date-based filtering or sorting in a future version of the application.
