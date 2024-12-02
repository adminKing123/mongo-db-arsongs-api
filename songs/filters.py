import django_filters
from .models import Song

class SongFilter(django_filters.FilterSet):
    original_name = django_filters.CharFilter(field_name='original_name', lookup_expr='icontains')
    album_id = django_filters.NumberFilter(field_name='album__id', lookup_expr='exact')  # Filter by album ID
    artist_ids = django_filters.BaseInFilter(field_name='song_artists__artist__id', lookup_expr='in')  # Filter by artist IDs
    tag_ids = django_filters.BaseInFilter(field_name='song_tags__tag__id', lookup_expr='in')  # Filter by tag IDs

    class Meta:
        model = Song
        fields = ['original_name', 'album_id', 'artist_ids', 'tag_ids']