from django.contrib import admin
from .models import Album, Artist, Tag, Song, SongArtist, SongTag
from django.utils.safestring import mark_safe
from config import CONFIG
from .admin_forms import SongAdminForm

# Register Album model
@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'year', 'custom_thumbnail300x300', 'custom_thumbnail1200x1200']
    search_fields = ['title', 'code']

    def custom_thumbnail300x300(self, obj):
        # Custom logic for the URL (display as a clickable link)
        link = f'{CONFIG["SRC_URI"]}{obj.thumbnail300x300}'  # Generate the full URL
        return mark_safe(f'<a href="{link}" target="_blank">{obj.title}</a>')
    
    def custom_thumbnail1200x1200(self, obj):
        # Custom logic for the URL (display as a clickable link)
        link = f'{CONFIG["SRC_URI"]}{obj.thumbnail1200x1200}'  # Generate the full URL
        return mark_safe(f'<a href="{link}" target="_blank">{obj.title}</a>')
    
    def custom_thumbnailpreview(self, obj):
        link = f'{CONFIG["SRC_URI"]}{obj.thumbnail300x300}'  # Generate the full URL
        return mark_safe(f'<img src="{link}" alt="{obj.title}" width="300" height="300" style="border: 1px solid var(--border-color);border-radius:4px;" />')
    
    fields = ['code', 'title', 'year', 'thumbnail300x300', 'thumbnail1200x1200', 'custom_thumbnailpreview']
    readonly_fields = ['custom_thumbnailpreview']
    custom_thumbnail300x300.short_description = 'thumbnail300x300'
    custom_thumbnail1200x1200.short_description = 'thumbnail1200x1200'
    custom_thumbnailpreview.short_description = 'Thumbnail Preview'

# Register Artist model
@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'custom_thumbnail300x300', 'custom_thumbnail1200x1200']
    search_fields = ['name']

    def custom_thumbnail300x300(self, obj):
        # Custom logic for the URL (display as a clickable link)
        link = f'{CONFIG["SRC_URI"]}{obj.thumbnail300x300}'  # Generate the full URL
        return mark_safe(f'<a href="{link}" target="_blank">{obj.name}</a>')
    
    def custom_thumbnail1200x1200(self, obj):
        # Custom logic for the URL (display as a clickable link)
        link = f'{CONFIG["SRC_URI"]}{obj.thumbnail1200x1200}'  # Generate the full URL
        return mark_safe(f'<a href="{link}" target="_blank">{obj.name}</a>')
    
    def custom_thumbnailpreview(self, obj):
        link = f'{CONFIG["SRC_URI"]}{obj.thumbnail300x300}'  # Generate the full URL
        return mark_safe(f'<img src="{link}" alt="{obj.name}" width="300" height="300" style="border: 1px solid var(--border-color);border-radius:4px;" />')

    fields = ['name', 'thumbnail300x300', 'thumbnail1200x1200', 'custom_thumbnailpreview']
    readonly_fields = ['custom_thumbnailpreview']
    custom_thumbnail300x300.short_description = 'thumbnail300x300'
    custom_thumbnail1200x1200.short_description = 'thumbnail1200x1200'
    custom_thumbnailpreview.short_description = 'Thumbnail Preview'

# Register Tag model
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class SongArtistInline(admin.TabularInline):
    model = SongArtist
    extra = 0  # Number of empty forms to display initially

# Inline for SongTag relationship
class SongTagInline(admin.TabularInline):
    model = SongTag
    extra = 0

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    form = SongAdminForm
    list_display = ['original_name', 'album_name', 'year', 'custom_url', 'artist_names', 'tag_names']  # Add 'artist_names' to list_display
    search_fields = ['original_name']
    inlines = [SongArtistInline, SongTagInline]  # Show SongArtists and SongTags as inlines

    def get_fields(self, request, obj=None):
        if obj:  # Editing or viewing an existing Song
            return ['title', 'original_name', 'lyrics', 'album', 'url', 'audio_preview']
        else:  # Adding a new Song
            return ['original_name', 'album', 'mp3_file']

    # Custom method to display album name instead of ID
    def album_name(self, obj):
        return mark_safe(f'<a href="/admin/songs/album/{obj.album.id}/change/">{obj.album.title}</a>')
    
    def year(self, obj):
        return obj.album.year  # Access the year of the related album
    
    def custom_url(self, obj):
        # Custom logic for the URL (display as a clickable link)
        link = f'{CONFIG["SRC_URI"]}{obj.url}'  # Generate the full URL
        return mark_safe(f'<a href="{link}" target="_blank">{obj.title}</a>')
    
    def artist_names(self, obj):
        # Get the related artists and generate clickable links
        artists = obj.song_artists.all()  # Access related SongArtist instances
        artist_links = [f'<a href="/admin/songs/artist/{artist.artist.id}/change/">{artist.artist.name}</a>' for artist in artists]  # Create links for each artist
        return mark_safe(", ".join(artist_links))
    
    def tag_names(self, obj):
        # Get the related artists and generate clickable links
        tags = obj.song_tags.all()  # Access related SongArtist instances
        tag_links = [f'<a href="/admin/songs/tag/{tag.tag.id}/change/">{tag.tag.name}</a>' for tag in tags]  # Create links for each artist
        return mark_safe(", ".join(tag_links))
    
    def audio_preview(self, obj):
        print(f'{CONFIG["SRC_URI"]}{obj.url}')
        return mark_safe(f'<audio controls><source src="{CONFIG["SRC_URI"]}{obj.url}" type="audio/mpeg"></audio>')
    
    album_name.admin_order_field = 'album'  # Allow sorting by album
    album_name.short_description = 'Album'  # Set the column header name
    custom_url.short_description = 'URL'  # Set custom header for the URL field
    artist_names.short_description = 'Artists'  # Set custom header for the artist names
    tag_names.short_description = 'Tags'  # Set custom header for the artist names

    # Define the fields for the form layout when editing a Song
    readonly_fields = ['audio_preview', 'title']

    # Use a custom form layout to display related artists and tags
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Customize the form fields to include artists and tags
        form.base_fields['album'].queryset = Album.objects.all()  # All albums
        return form
