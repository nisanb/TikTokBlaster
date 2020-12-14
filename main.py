from api import tiktok
import argparse


def parse_args():
    parser = argparse.ArgumentParser("TikTokBlaster")

    parser.add_argument(
        "--hash-tag",
        type=str,
        default=None,
        required=True
    )

    parser.add_argument(
        "--video-limit",
        type=int,
        default=5,
        required=False
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    videos = tiktok.get_videos_by_hash_tag(hash_tag=args.hash_tag, limit=args.video_limit)

    for video in videos["media"]:
        author_id = video["author"]["uniqueId"]
        video_id = video["video_id"]

        url = tiktok.get_no_watermark_video(author_id=author_id, video_id=video_id)
        print(url)
