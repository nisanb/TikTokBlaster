import os
import urllib.request
from api import tiktok
import configuration


def video_pipeline(video: str):
    author_id = video["author"]["uniqueId"]
    video_id = video["video_id"]
    print(f"Retrieved video {video_id} from author {author_id}")
    url_object = tiktok.get_no_watermark_video(author_id=author_id, video_id=video_id)
    try:
        url_link = url_object["tmp_no_watermakr_url"]
    except KeyError:
        raise KeyError(f"No value for url_object: {url_object}")
    print(f"type of video_id {type(video_id)}")
    print(url_object)
    print(url_link)
    return download_video(video_id=video_id, url=url_link)


def download_video(video_id: str, url: str) -> str:
    """
    Downloads a video to the temporary folder, returning its' saved path
    :param hash_tag:
    :param url:
    :return:
    """
    print(configuration.Paths.tmp_path)
    print(video_id)
    saved_video_path = os.path.join(configuration.Paths.tmp_path, f"{video_id}.mp4")

    if os.path.exists(saved_video_path):
        print(f"Skipping video {saved_video_path} - already exists")
        return saved_video_path

    # Download the video
    print(f"Downloading {url}")
    urllib.request.urlretrieve(url, saved_video_path)
    print(f"Downloaded to {saved_video_path}")

    return saved_video_path
