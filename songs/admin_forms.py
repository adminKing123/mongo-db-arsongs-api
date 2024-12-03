from github import Github
from django import forms
from django.core.validators import FileExtensionValidator
from .models import Song, Album
from config import CONFIG
from PIL import Image
import os
from io import BytesIO

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

        # Save the instance to generate an ID if not already present
        if commit:
            instance.save()  # Save the instance first to generate the ID

        return instance

class AlbumAdminForm(forms.ModelForm):
    image_file = forms.FileField(
        required=False,
        label="Upload Image File (1:1 aspect ratio)",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    class Meta:
        model = Album  # Replace 'Album' with the actual model you're using
        fields = ['image_file']

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Handle the image file upload
        image_file = self.cleaned_data.get('image_file')
        if image_file:
            # Open the image
            img = Image.open(image_file)

            # Ensure the image has a 1:1 aspect ratio
            width, height = img.size
            if width != height:
                raise ValueError("The uploaded image must have a 1:1 aspect ratio.")

            # Resizing logic
            target_sizes = [(300, 300), (1200, 1200)]
            buffers = {}

            for size in target_sizes:
                resized_img = img.copy()

                # Resize image to the exact dimensions
                resized_img = resized_img.resize(size, Image.Resampling.LANCZOS)
                
                # Save resized image to buffer
                buffer = BytesIO()
                resized_img.save(buffer, format='PNG')
                buffer.seek(0)  # Reset buffer position
                buffers[size] = buffer

            # Upload to GitHub
            github_token = CONFIG["GITHUB_TOKEN"]
            branch_name = CONFIG["BRANCH_NAME"]
            github_repo_name = CONFIG["GITHUB_REPO_NAME"]

            github = Github(github_token)
            repo = github.get_user().get_repo(github_repo_name)

            _, extension = os.path.splitext(image_file.name)
            filename = f'{instance.code} - {instance.title} ({instance.year}).png'

            for size, buffer in buffers.items():
                file_path = f'album-images/{size[0]}x{size[1]}/{filename}'
                buffer.seek(0)  # Ensure buffer is at the start for reading
                content = buffer.read()

                try:
                    repo.create_file(
                        path=file_path,
                        message=f"Upload {os.path.basename(file_path)}",
                        content=content,
                        branch=branch_name
                    )
                    print(f"Successfully uploaded {file_path} to GitHub.")
                except Exception as e:
                    print(f"Failed to upload {file_path} to GitHub: {e}")

        # Save the instance
        if commit:
            instance.save()
        return instance
