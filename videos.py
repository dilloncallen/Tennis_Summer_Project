# videos.py

import json
import youtube_dl
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
import argparse

def download_video(url, output_path):
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def crop_video(input_path, output_path, start_time, end_time):
    ffmpeg_extract_subclip(input_path, start_time, end_time, targetname=output_path)

def time_to_seconds(time_str):
    if time_str is None:
        return None
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--videos_json', type=str, required=True, help='videos.json')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to save the downloaded and cropped videos')
    args = parser.parse_args()

    with open(args.videos_json, 'r') as f:
        videos = json.load(f)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    for video_name, video_info in videos.items():
        url = video_info['url']
        crop_start = time_to_seconds(video_info['crop_start'])
        crop_end = time_to_seconds(video_info['crop_end'])

        video_output_path = os.path.join(args.output_dir, f"{video_name}.mp4")
        cropped_output_path = os.path.join(args.output_dir, f"{video_name}_cropped.mp4")

        print(f"Downloading {video_name} from {url}...")
        download_video(url, video_output_path)

        if crop_start is not None or crop_end is not None:
            print(f"Cropping {video_name} from {crop_start} to {crop_end} seconds...")
            crop_video(video_output_path, cropped_output_path, crop_start, crop_end)
        else:
            os.rename(video_output_path, cropped_output_path)

        print(f"Saved cropped video to {cropped_output_path}")
