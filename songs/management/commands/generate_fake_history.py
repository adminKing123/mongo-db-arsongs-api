import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from songs.models import Song, UserSongHistory
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Generate fake song history for a specified user."

    def add_arguments(self, parser):
        parser.add_argument(
            'user_id', type=int, help="The ID of the user to generate history for."
        )
        parser.add_argument(
            '--entries', type=int, default=10, help="Number of history entries to generate."
        )

    def handle(self, *args, **kwargs):
        user_id = kwargs['user_id']
        num_entries = kwargs['entries']

        try:
            # Fetch the user
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User with ID {user_id} does not exist."))
            return

        # Fetch all songs
        all_songs = list(Song.objects.all())
        if not all_songs:
            self.stdout.write(self.style.ERROR("No songs available in the database."))
            return

        # Generate fake history
        for _ in range(num_entries):
            # Pick a random song
            song = random.choice(all_songs)

            # Generate a random accessed_at time within the past 30 days
            days_ago = random.randint(0, 30)
            accessed_at = now() - timedelta(days=days_ago)

            # Create or update the history entry
            history, created = UserSongHistory.objects.update_or_create(
                user=user,
                song=song,
                defaults={'accessed_at': accessed_at}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Added history for song '{song.title}' accessed at {accessed_at}."))
            else:
                self.stdout.write(f"Updated history for song '{song.title}' to accessed at {accessed_at}.")

        self.stdout.write(self.style.SUCCESS(f"Successfully generated {num_entries} history entries for user ID {user_id}."))
