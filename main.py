import os
import pprint
from multiprocessing.pool import ThreadPool

from api import tiktok
from api import downloader
from api import compiler
import argparse
import configuration


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


def resolve_configurations():
    # Resolve temporary path
    configuration.Paths.tmp_path = os.path.join(configuration.Paths.root_path, "tmp")
    if not os.path.isdir(configuration.Paths.tmp_path):
        os.mkdir(configuration.Paths.tmp_path)

    print(configuration.Paths.tmp_path)


if __name__ == "__main__":
    args = parse_args()
    resolve_configurations()

    videos = tiktok.get_videos_by_hash_tag(hash_tag=args.hash_tag, limit=args.video_limit)

    with ThreadPool(20) as pool:
        generated_videos = pool.map(downloader.video_pipeline, videos["media"])

    generated_videos = list(filter(lambda a: a != "", generated_videos))
    if len(generated_videos) < args.video_limit:
        print(f"Did not fetch enough videos! required: {args.video_limit}, generated: {len(generated_videos)}")

    compiler.generate_video(generated_videos)