import os
import subprocess

from tempfile import TemporaryDirectory
from typing import Optional, Iterable


def generate_video(videos: Iterable, output_file_name: str = "output.mp4"):

    with TemporaryDirectory() as td:
        video_list_file_path = os.path.join(td, 'videos.list')
        with open(video_list_file_path, "w") as video_list_file_handler:
            for video in videos:
                video_list_file_handler.write(f"file \'{video}'\n")

        _compile_video(video_list_file=video_list_file_path, output_file_name=output_file_name)


def _compile_video(video_list_file, output_file_name="output.mp4"):
    if not os.path.isfile(video_list_file):
        raise ValueError(f"File {video_list_file} does not exist!")

    concat_cmdline = f"ffmpeg -f concat -safe 0 -i {video_list_file} -c copy {output_file_name} -y"
    status = subprocess.call(concat_cmdline, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if status != 0:
        raise RuntimeError(f"Process exit with status: {status}\n{concat_cmdline}")


if __name__ == "__main__":
    # Used for testing
    test_videos = ['C:\\Users\\Nisan\\PycharmProjects\\TikTokBlaster\\tmp2\\6746577129057684742.mp4', 'C:\\Users\\Nisan\\PycharmProjects\\TikTokBlaster\\tmp2\\6779308572657372422.mp4']

    generate_video(test_videos)
