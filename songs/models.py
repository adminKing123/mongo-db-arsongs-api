from django.db import models

class Album(models.Model):
    code = models.CharField(max_length=255, unique=True, null=False)
    title = models.CharField(max_length=255, unique=True, null=False)
    year = models.IntegerField(null=False)
    thumbnail300x300 = models.URLField(null=False)
    thumbnail1200x1200 = models.URLField(null=False)

    def __str__(self):
        return self.title

class Artist(models.Model):
    name = models.CharField(max_length=255, null=False)
    thumbnail300x300 = models.URLField(null=False)
    thumbnail1200x1200 = models.URLField(null=False)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name

class Song(models.Model):
    title = models.CharField(max_length=255, unique=True, null=False)
    url = models.URLField(null=False)
    original_name = models.CharField(max_length=255, null=False)
    lyrics = models.URLField(null=False)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')

    class Meta:
        ordering = ['-id']

class SongArtist(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='song_artists')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='song_artists')

class SongTag(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='song_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='song_tags')
