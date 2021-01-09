import os
import sys

print(f"Commandline: {sys.argv}")

import random
from multiprocessing.pool import ThreadPool

from api import tiktok, downloader, compiler, storage, datastore
import argparse
import configuration

import logging

def _set_logging(output_path: str):
    # create logger with 'spam_application'
    log_console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_console_format)

    file_handler =  logging.FileHandler(os.path.join(configuration.Paths.output_path, "run.log"), "w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_console_format)

    handlers = (
        console_handler,
        file_handler,
    )

    logging.basicConfig(
        handlers=handlers,
        level=logging.DEBUG,
    )


def parse_args():
    parser = argparse.ArgumentParser("TikTokBlaster")

    parser.add_argument(
        "--hash-tag",
        type=str,
        default=None,
        required=False
    )

    parser.add_argument(
        "--count",
        type=int,
        default=5,
        required=False,
    )

    parser.add_argument(
        "--output",
        type=str,
        default=os.path.join(os.getcwd(), "output"),
        required=False,
    )

    parser.add_argument(
        "--threads",
        "-t",
        type=int,
        default=20,
        required=False,
    )

    return parser.parse_args()


def _create_if_not_exist(path: str) -> None:
    if not os.path.isdir(path):
        os.mkdir(path)


def resolve_configurations(output_path: str):
    configuration.Paths.output_path = output_path if "OUTPUT_PATH" not in os.environ else os.environ["OUTPUT_PATH"]
    _create_if_not_exist(configuration.Paths.output_path)

    configuration.Paths.tmp_path = os.path.join(configuration.Paths.output_path, "tmp")
    _create_if_not_exist(configuration.Paths.tmp_path)

    _set_logging(output_path=configuration.Paths.output_path)


if __name__ == "__main__":
    args = parse_args()
    resolve_configurations(output_path=args.output)

    # Create a new request
    request_entity = datastore.create_request(hash_tag=args.hash_tag, count=args.count)

    videos = tiktok.get_videos_by_hash_tag(hash_tag=args.hash_tag, limit=args.count)

    if len(videos) != args.count:
        raise RuntimeError(f"Could not fetch enough videos! Requested #{args.hash_tag} with limit of "
                           f"{args.count}, received {len(videos)}")

    logging.info("Downloading videos..")
    with ThreadPool(args.threads) as pool:
        generated_videos = pool.map(downloader.video_pipeline, videos)
    logging.info("Finished downloading videos")
    generated_videos = list(filter(lambda a: a != "", generated_videos))
    print(generated_videos)
    if len(generated_videos) < args.count:
        logging.warning(f"Did not reach minimum requested videos. required: {args.count}, "
                        f"generated: {len(generated_videos)}")

    logging.info("Compiling video..")
    output_file_path = compiler.generate_video(generated_videos, output_file_name=request_entity.key.name)

    storage.upload_file(output_file_path)

    datastore.update_request(request_entity.key.name, datastore.RequestStatus.SUCCESS)

    logging.info("bon voyage")
