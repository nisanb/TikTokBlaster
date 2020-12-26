import os
import urllib.request
from json import JSONDecodeError

from api import tiktok
import configuration


def video_pipeline(video: str) -> str:
    author_id = video["author"]["uniqueId"]
    video_id = video["video_id"]

    try:
        url_object = tiktok.get_no_watermark_video(author_id=author_id, video_id=video_id)
    except JSONDecodeError:
        print(f"Couldn't fetch video download URL with no watermark. Skipping video..")
        return ""

    # get_no_watermark_video failed
    if url_object is None or "videoUrlNoWaterMark" not in url_object:
        return ""

    url_link = url_object["videoUrlNoWaterMark"]

    return download_video(video_id=video_id, url=url_link)


def video_pipeline_old(video: str) -> str:
    author_id = video["author"]["uniqueId"]
    video_id = video["video_id"]

    try:
        url_object = tiktok.get_no_watermark_video(author_id=author_id, video_id=video_id)
    except JSONDecodeError:
        print(f"Couldn't fetch video download URL with no watermark. Skipping video..")
        return ""

    # get_no_watermark_video failed
    if url_object is None or "tmp_no_watermakr_url" not in url_object:
        return ""

    url_link = url_object["tmp_no_watermakr_url"]

    return download_video(video_id=video_id, url=url_link)


def download_video(video_id: str, url: str) -> str:
    """
    Downloads a video to the temporary folder, returning its' saved path
    :param video_id: The video ID to be downloaded
    :param url: A path
    :return: Path to a video file, empty string if couldn't download
    """
    if url is None:
        print(f"Skipped video {video_id}: Cannot find URL for video {url}")
        return ""

    saved_video_path = os.path.join(configuration.Paths.tmp_path, f"{video_id}.mp4")

    if os.path.exists(saved_video_path):
        return saved_video_path

    # Download the video
    print(f"Downloading {url}")
    urllib.request.urlretrieve(url, saved_video_path)
    print(f"Downloaded to {saved_video_path}")

    return saved_video_path
