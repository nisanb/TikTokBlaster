import requests
from json import loads


headers = {
    'x-rapidapi-key': "e1b2a4bdc1msh6a8aeac7805f45dp1a15b0jsn88dd526731b0",
    'x-rapidapi-host': "tiktok.p.rapidapi.com"
    }


def get_videos_by_hash_tag(hash_tag: str = "puppy", limit: int = 5):
    url = "https://tiktok.p.rapidapi.com/live/hashtag/feed"
    querystring = {
        "name": hash_tag,
        "limit": limit
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return loads(response.text)


def get_no_watermark_video(author_id: str, video_id: str):
    url = "https://tiktok.p.rapidapi.com/live/post/nomark"
    querystring = {"video": f"https://www.tiktok.com/{author_id}/video/{video_id}"}
    response = requests.request("GET", url, headers=headers, params=querystring)

    return loads(response.text)
