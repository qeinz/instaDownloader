import instaloader
import os
from zipfile import ZipFile

LOGIN_FILE = 'login_credentials.txt'

def download_instagram_profile(profile_name, download_folder):
    # Clear and remove the download folder at the start
    clear_and_remove_folder(download_folder)

    # Delete the existing archive.zip if it exists
    delete_existing_zip()

    loader = instaloader.Instaloader()

    username, password = get_login_credentials()

    try:
        print(f"Logging in as {username}...")
        loader.login(username, password)
        print("Login successful!")
    except instaloader.exceptions.BadCredentialsException:
        print("Login failed! Check your username and password.")
        return
    except Exception as e:
        print(f"An error occurred during login: {e}")
        return

    try:
        profile = instaloader.Profile.from_username(loader.context, profile_name)

        # Download posts
        for i, post in enumerate(profile.get_posts(), start=1):
            filename = f"post_{i}.jpg"
            print(f"Downloading post: {post.url}")
            loader.download_post(post, target=download_folder)
            # Rename the downloaded file
            for file in os.listdir(download_folder):
                if file.startswith('post_'):
                    old_file_path = os.path.join(download_folder, file)
                    new_file_path = os.path.join(download_folder, filename)
                    print(f"Renaming {old_file_path} to {new_file_path}")
                    os.rename(old_file_path, new_file_path)
                    break

        # Download stories
        stories = loader.get_stories(userids=[profile.userid])
        for i, story in enumerate(stories, start=1):
            for j, item in enumerate(story.get_items(), start=1):
                filename = f"story_{i}_{j}.jpg"
                print(f"Downloading story: {item.url}")
                loader.download_storyitem(item, target=download_folder)
                # Rename the downloaded file
                for file in os.listdir(download_folder):
                    if file.startswith(f'story_{i}_'):
                        old_file_path = os.path.join(download_folder, file)
                        new_file_path = os.path.join(download_folder, filename)
                        print(f"Renaming {old_file_path} to {new_file_path}")
                        os.rename(old_file_path, new_file_path)
                        break

        # Download highlights
        download_highlights(profile, loader, download_folder)

        # Delete non-JPG files
        delete_non_jpg_files(download_folder)

        # Create and move the ZIP file to the root directory
        zip_file_path = create_zip_from_folder(download_folder)

        print(f"Download completed. All images are saved in '{download_folder}'.")
        print(f"ZIP file created at: {zip_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

def download_highlights(profile, loader, download_folder):
    highlights = loader.get_highlights(profile)
    for i, highlight in enumerate(highlights, start=1):
        print(f"Downloading highlight: {i}")
        for j, item in enumerate(highlight.get_items(), start=1):
            filename = f"highlight_{i}_{j}.jpg"
            print(f"Downloading highlight item: {item.url}")
            file_path = os.path.join(download_folder, filename)
            # Save each highlight item directly to the download_folder
            loader.download_storyitem(item, target=download_folder)
            # Rename the downloaded file
            for file in os.listdir(download_folder):
                if file.startswith(f"highlight_{i}_"):
                    old_file_path = os.path.join(download_folder, file)
                    new_file_path = file_path
                    print(f"Renaming {old_file_path} to {new_file_path}")
                    os.rename(old_file_path, new_file_path)
                    break

def clear_and_remove_folder(folder):
    # Remove the folder if it exists
    if os.path.exists(folder):
        for root, dirs, files in os.walk(folder, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(folder)  # Remove the folder itself
        print(f"Removed the folder: {folder}")

def delete_non_jpg_files(folder):
    for filename in os.listdir(folder):
        if not filename.endswith('.jpg'):
            file_path = os.path.join(folder, filename)
            os.remove(file_path)
            print(f"Deleted non-jpg file: {filename}")

def create_zip_from_folder(folder):
    zip_file_name = "archive.zip"
    zip_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), zip_file_name)
    with ZipFile(zip_file_path, 'w') as zipf:
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder))
                print(f"Added {file} to {zip_file_path}")
    return zip_file_path

def delete_existing_zip():
    zip_file_name = "archive.zip"
    zip_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), zip_file_name)
    if os.path.exists(zip_file_path):
        os.remove(zip_file_path)
        print(f"Deleted existing ZIP file: {zip_file_path}")

def get_login_credentials():
    if os.path.exists(LOGIN_FILE):
        with open(LOGIN_FILE, 'r') as f:
            lines = f.readlines()
            if len(lines) >= 2:
                username = lines[0].strip()
                password = lines[1].strip()
                return username, password
    
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")
    
    with open(LOGIN_FILE, 'w') as f:
        f.write(f"{username}\n")
        f.write(f"{password}\n")
    
    return username, password

if __name__ == "__main__":
    profile_name = input("Enter the Instagram username you want to download from: ")
    download_folder = "downloads"
    clear_and_remove_folder(download_folder)  # Clear and remove folder at the start
    download_instagram_profile(profile_name, download_folder)
