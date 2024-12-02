import urllib.parse
from github import Github
from django import forms
from django.core.validators import FileExtensionValidator
from .models import Song
from config import CONFIG

class SongAdminForm(forms.ModelForm):
    mp3_file = forms.FileField(
        required=False,
        label="Upload MP3 File",
        validators=[FileExtensionValidator(allowed_extensions=['mp3'])]
    )

    class Meta:
        model = Song
        fields = ['original_name', 'album', 'mp3_file']

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Handle the MP3 file upload
        mp3_file = self.cleaned_data.get('mp3_file')
        if mp3_file:
            # Prepare the custom filename
            album_code = instance.album.code  # Assuming the album model has a `code` field
            filename = f"{album_code} - {instance.original_name}.mp3"

            # Prepare GitHub API details
            github_token = CONFIG["GITHUB_TOKEN"]
            branch_name = CONFIG["BRANCH_NAME"]
            github_repo_name = CONFIG["GITHUB_REPO_NAME"]
            github = Github(github_token)
            repo = github.get_user().get_repo(github_repo_name)

            # Prepare file content and path
            file_path = f'songs-file/{filename}'
            content = mp3_file.read()  # Ensure proper encoding for binary files

            # Upload to GitHub
            try:
                repo.create_file(
                    path=file_path,
                    message=f"Upload MP3 file {filename}",
                    content=content,
                    branch=branch_name
                )
                print(f"Successfully uploaded {filename} to GitHub at {file_path}")
            except Exception as e:
                print(f"Failed to upload {filename} to GitHub: {e}")

            # URL-encode the file path and update the song instance details
            instance.title = filename
            encoded_url = urllib.parse.quote(file_path)
            instance.url = encoded_url

        # Save the instance to generate an ID if not already present
        if commit:
            instance.save()
            # Now that the ID exists, set the lyrics field
            instance.lyrics = f"lrc/{instance.id}.lrc"
            instance.save()

        return instance
