import instaloader
import os
import shutil
from zipfile import ZipFile

def download_instagram_profile(profile_name, download_folder):
    clear_download_folder(download_folder)

    loader = instaloader.Instaloader()

    try:
        profile = instaloader.Profile.from_username(loader.context, profile_name)

        for post in profile.get_posts():
            print(f"Downloading {post.url}")
            loader.download_post(post, target=download_folder)

        print(f"Download completed. All images are saved in '{download_folder}'.")
        move_non_jpg_files(download_folder)
        create_zip_from_jpg(download_folder)

    except Exception as e:
        print(f"An error occurred: {e}")

def clear_download_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
        print(f"Deleted existing folder: {folder}")
    if os.path.exists(f"{folder}.zip"):
        os.remove(f"{folder}.zip")
        print(f"Deleted existing zip file: {folder}.zip")

def move_non_jpg_files(folder):
    non_jpg_folder = os.path.join(folder, "non_jpgs")
    os.makedirs(non_jpg_folder, exist_ok=True)

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if not filename.endswith('.jpg') and os.path.isfile(file_path):
            shutil.move(file_path, os.path.join(non_jpg_folder, filename))
            print(f"Moved non-jpg file: {filename} to {non_jpg_folder}")

def create_zip_from_jpg(folder):
    zip_file = os.path.join(folder, "images.zip")
    with ZipFile(zip_file, 'w') as zipf:
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith('.jpg'):
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.basename(file_path))
                    print(f"Added {file} to {zip_file}")
    print(f"All jpg files have been zipped into '{zip_file}'.")

if __name__ == "__main__":
    profile_name = input("Enter the Instagram username: ")
    download_folder = "downloaded_images"
    download_instagram_profile(profile_name, download_folder)
