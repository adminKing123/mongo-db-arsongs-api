import django_filters
from .models import Song, Artist, Album, Tag

class SongFilter(django_filters.FilterSet):
    original_name = django_filters.CharFilter(field_name='original_name', lookup_expr='icontains')
    album_id = django_filters.NumberFilter(field_name='album__id', lookup_expr='exact')  # Filter by album ID
    artist_ids = django_filters.BaseInFilter(field_name='song_artists__artist__id', lookup_expr='in')  # Filter by artist IDs
    tag_ids = django_filters.BaseInFilter(field_name='song_tags__tag__id', lookup_expr='in')  # Filter by tag IDs

    class Meta:
        model = Song
        fields = ['original_name', 'album_id', 'artist_ids', 'tag_ids']

class ArtistFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Artist
        fields = ['name']

class TagFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Tag
        fields = ['name']

class AlbumFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(field_name='code', lookup_expr='icontains')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    year = django_filters.NumberFilter(field_name='year')

    class Meta:
        model = Album  # Correct the model to 'Album'
        fields = ['code', 'title', 'year']
