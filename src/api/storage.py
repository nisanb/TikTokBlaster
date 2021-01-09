"""
Google cloud storage API
"""

from google.cloud import storage
import configuration
import os


def upload_file(file_path: str):
    if not os.path.isfile(file_path):
        return False

    client = storage.Client()
    bucket = client.get_bucket("tiktok_blaster_videos")
    blob = bucket.blob(os.path.basename(file_path))
    blob.upload_from_filename(file_path)

    return True


if __name__ == "__main__":
    client = storage.Client()
    bucket = client.get_bucket("tiktok_blaster_videos")
    blob2 = bucket.blob('TikTokBlaster-4f915ab976e7.json')
    blob2.upload_from_filename("TikTokBlaster-4f915ab976e7.json")
