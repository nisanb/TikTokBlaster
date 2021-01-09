import os
import subprocess
from typing import Iterable

import configuration


def convert_to_ts(video_file_path):
    file_path = os.path.dirname(video_file_path)
    file_name = os.path.splitext(os.path.basename(video_file_path))[0]
    output_file_path = os.path.join(file_path, f"{file_name}.ts")

    cmdline = f"ffmpeg -i {video_file_path} -c copy -bsf:v h264_mp4toannexb -f mpegts {output_file_path} -y"

    status = subprocess.call(cmdline, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if status != 0:
        return None

    return output_file_path


def generate_video(videos: Iterable, output_file_name: str = "output"):
    output_file_name += ".mp4"
    output_file_path = os.path.join(configuration.Paths.output_path, output_file_name)

    video_list_file_path = os.path.join(configuration.Paths.tmp_path, 'videos.list')
    with open(video_list_file_path, "w") as video_list_file_handler:
        for video in videos:
            video_list_file_handler.write(f"file \'{video}'\n")

    _compile_video(video_list_file=video_list_file_path, output_file_path=output_file_path)

    return output_file_path


def _compile_video(video_list_file, output_file_path):
    if not os.path.isfile(video_list_file):
        raise ValueError(f"File {video_list_file} does not exist!")

    concat_cmdline = f"ffmpeg -f concat -safe 0 -i {video_list_file} -vcodec copy -acodec copy {output_file_path} -y"
    status = subprocess.call(concat_cmdline, shell=True)#, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if status != 0:
        raise RuntimeError(f"Process exit with status: {status}\n{concat_cmdline}")


if __name__ == "__main__":
    # Used for testing
    test_videos = ['C:\\Users\\Nisan\\PycharmProjects\\TikTokBlaster\\tmp2\\6746577129057684742.mp4', 'C:\\Users\\Nisan\\PycharmProjects\\TikTokBlaster\\tmp2\\6779308572657372422.mp4']

    generate_video(test_videos)
