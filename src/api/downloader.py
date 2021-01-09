import json
import os
import urllib.request
from json import JSONDecodeError
from . import tiktok, compiler
import configuration


def video_pipeline(video: str) -> str:
    author_id = video["author"]["uniqueId"]
    video_id = video["video_id"]

    try:
        url_object = tiktok.get_no_watermark_video(author_id=author_id, video_id=video_id)
    except JSONDecodeError:
        print(f"Couldn't fetch video download URL with no watermark. Skipping video..")
        _record_error(video_id, video)
        return ""

    # get_no_watermark_video failed
    if url_object is None or "videoUrlNoWaterMark" not in url_object:
        print("Couldn't fetch:")
        print(url_object)

        _record_error(video_id, video)
        return ""

    url_link = url_object["videoUrlNoWaterMark"]
    video_path = download_video(video_id=video_id, url=url_link)
    if video_path:
        return compiler.convert_to_ts(video_path)


def _record_error(video_id, video):
    with open(f"{video_id}.log", "w") as fh:
        fh.write(json.dumps(video))


def download_video(video_id: str, url: str) -> str:
    """
    Downloads a video to the temporary folder, returning its' saved path
    :param video_id: The video ID to be downloaded
    :param url: A path
    :return: Path to a video file, empty string if couldn't download
    """
    if not url:
        print(f"Skipped video {video_id}: Cannot find URL for video {url}")
        _record_error(video_id, url)
        return ""

    saved_video_path = os.path.join(configuration.Paths.tmp_path, f"{video_id}.mp4")

    if os.path.exists(saved_video_path):
        return saved_video_path

    # Download the video
    urllib.request.urlretrieve(url, saved_video_path)

    return saved_video_path


if __name__ == "__main__":
    video = """
    {"video_id": "6860012641151126789", "create_time": "1597221171", "description": "It's the fake friends for me  #test #foryou", "author": {"id": "6725450734508426246", "uniqueId": "jacobplak", "nickname": "Jacob Plank", "avatarThumb": "https://p16-sign-va.tiktokcdn.com/musically-maliva-obj/ce1f1ca447750ce3bec49399a4e2b74f~c5_100x100.jpeg?x-expires=1609185600&x-signature=viKmKhrXLr%2FtPsY%2Fkh3G54%2BMfBI%3D", "avatarMedium": "https://p16-sign-va.tiktokcdn.com/musically-maliva-obj/ce1f1ca447750ce3bec49399a4e2b74f~c5_720x720.jpeg?x-expires=1609185600&x-signature=WoaQhvTfJ7RMo6lnwb2guFawQlY%3D", "avatarLarger": "https://p16-sign-va.tiktokcdn.com/musically-maliva-obj/ce1f1ca447750ce3bec49399a4e2b74f~c5_1080x1080.jpeg?x-expires=1609185600&x-signature=awrfRbv8YPpvcwyLN%2FcAWVlkthw%3D", "signature": "DM me on instabusiness@otterinfluence.comy bored", "verified": false, "private": false, "secUid": "MS4wLjABAAAA776Z-6xv8tCTzMtrzsvK6P2RcrsVLihfNN4wWO45v4fF3RDGXuotGGp96rjEmN7u", "following": 321, "followers": 576900, "heartCount": "14000000", "videoCount": 314, "diggCount": 44100}, "video": {"height": 1024, "width": 576, "duration": 18, "ratio": 18, "cover": "https://p16-sign-sg.tiktokcdn.com/obj/tos-maliva-p-0068/bf0059a432c449879b33fea5172cdc1e?x-expires=1609120800&x-signature=2lIEanP4zZkKY18K9PB4rl2sE%2B4%3D", "originCover": "https://p16-sign-sg.tiktokcdn.com/obj/tos-maliva-p-0068/de80c4a2175f4f2da9ee2ac266f12003_1597221173?x-expires=1609120800&x-signature=afsIdNvWjxmWhLt9cTrLmPOn7yE%3D", "dynamicCover": "https://p16-sign-sg.tiktokcdn.com/obj/tos-maliva-p-0068/d5de26bc751c49cba54239a49f3c9412_1597221173?x-expires=1609120800&x-signature=tkqCb8qFXhxxn%2FL%2FfyQbz8%2Ft7no%3D", "playAddr": "https://v16-web.tiktok.com/video/tos/useast2a/tos-useast2a-pve-0068/c56d7f71b5224058a74acc13dacb9098/?a=1988&br=1076&bt=538&cd=0%7C0%7C1&cr=0&cs=0&cv=1&dr=0&ds=3&er=&expire=1609122773&l=202012272032350101902080431FA4E276&lr=tiktok_m&mime_type=video_mp4&policy=2&qs=0&rc=MzRuOG5scjt0djMzZjczM0ApOWgzODM3aTw5NzRkNTY8N2debS02Ly1uZm1fLS01MTZzc2NeY15eNV8vYzBjNmJjX2A6Yw%3D%3D&signature=7bff03dc1a5ae0e8a4faa4917bbab639&tk=tt_webid_v2&vl=&vr="}, "music": {"id": "6860012637032385285", "title": "original sound", "playUrl": "https://sf58-sg.tiktokcdn.com/obj/musically-maliva-obj/6860012565314112261.mp3", "coverThumb": "https://p16-sign-va.tiktokcdn.com/musically-maliva-obj/ce1f1ca447750ce3bec49399a4e2b74f~c5_100x100.jpeg?x-expires=1609185600&x-signature=viKmKhrXLr%2FtPsY%2Fkh3G54%2BMfBI%3D", "coverMedium": "https://p16-sign-va.tiktokcdn.com/musically-maliva-obj/ce1f1ca447750ce3bec49399a4e2b74f~c5_720x720.jpeg?x-expires=1609185600&x-signature=WoaQhvTfJ7RMo6lnwb2guFawQlY%3D", "coverLarge": "https://p16-sign-va.tiktokcdn.com/musically-maliva-obj/ce1f1ca447750ce3bec49399a4e2b74f~c5_1080x1080.jpeg?x-expires=1609185600&x-signature=awrfRbv8YPpvcwyLN%2FcAWVlkthw%3D", "authorName": "Jacob Plank", "original": true}, "statistics": {"diggCount": 2600000, "shareCount": 414900, "commentCount": 84400, "playCount": 11600000}}
    """
    video = json.loads(video)

    video_pipeline(video)

    print(video)
