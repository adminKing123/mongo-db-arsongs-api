from django.core.management.base import BaseCommand
import sqlite3
from songs.models import Album, Artist, Tag, Song, SongArtist, SongTag
from config import CONFIG
from tqdm import tqdm  # Import tqdm for progress bars

class Command(BaseCommand):
    help = "Seed data from another SQLite database"

    def handle(self, *args, **kwargs):
        # Connect to the source SQLite database
        source_conn = sqlite3.connect(CONFIG["SEED_DB_PATH"])  # Replace with your source DB path
        cursor = source_conn.cursor()

        try:
            # Seed Albums
            self.stdout.write("Seeding Albums...")
            cursor.execute("SELECT id, code, title, year, thumbnail300x300, thumbnail1200x1200 FROM albums")
            albums = cursor.fetchall()
            for id, code, title, year, thumb300, thumb1200 in tqdm(albums, desc="Albums", unit="album"):
                Album.objects.get_or_create(
                    id=id,
                    code=code,
                    title=title,
                    year=year,
                    thumbnail300x300=thumb300,
                    thumbnail1200x1200=thumb1200,
                )

            # Seed Artists
            self.stdout.write("Seeding Artists...")
            cursor.execute("SELECT id, name, thumbnail300x300, thumbnail1200x1200 FROM artists")
            artists = cursor.fetchall()
            for artist_id, name, thumb300, thumb1200 in tqdm(artists, desc="Artists", unit="artist"):
                Artist.objects.get_or_create(
                    id=artist_id,
                    name=name,
                    thumbnail300x300=thumb300,
                    thumbnail1200x1200=thumb1200,
                )

            # Seed Tags
            self.stdout.write("Seeding Tags...")
            cursor.execute("SELECT id, name FROM tags")
            tags = cursor.fetchall()
            for tag_id, name in tqdm(tags, desc="Tags", unit="tag"):
                Tag.objects.get_or_create(id=tag_id, name=name)

            # Seed Songs
            self.stdout.write("Seeding Songs...")
            cursor.execute("SELECT id, title, url, original_name, lyrics, album_id FROM songs")
            songs = cursor.fetchall()
            for song_id, title, url, original_name, lyrics, album_id in tqdm(songs, desc="Songs", unit="song"):
                album = Album.objects.get(pk=album_id)  # Resolve foreign key for album
                song = Song.objects.get_or_create(
                    id=song_id,
                    title=title,
                    url=url,
                    original_name=original_name,
                    lyrics=lyrics,
                    album=album,
                )[0]

                # Seed Song-Artist Relationship (Many-to-Many)
                cursor.execute("SELECT artist_id FROM songartists WHERE song_id = ?", (song_id,))
                artist_ids = cursor.fetchall()
                for artist_id, in artist_ids:
                    artist = Artist.objects.get(id=artist_id)  # Resolve artist by ID
                    SongArtist.objects.get_or_create(song=song, artist=artist)

                # Seed Song-Tag Relationship (Many-to-Many)
                cursor.execute("SELECT tag_id FROM songtags WHERE song_id = ?", (song_id,))
                tag_ids = cursor.fetchall()
                for tag_id, in tag_ids:
                    tag = Tag.objects.get(id=tag_id)  # Resolve tag by ID
                    SongTag.objects.get_or_create(song=song, tag=tag)

            self.stdout.write(self.style.SUCCESS("Data seeded successfully!"))

        except Exception as e:
            self.stderr.write(f"Error occurred: {e}")

        finally:
            source_conn.close()
