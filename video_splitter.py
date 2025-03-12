from moviepy.video.io.VideoFileClip import VideoFileClip
import os

def split_video(input_video_path, output_folder, clip_duration=120):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Load the video file
    video = VideoFileClip(input_video_path)
    video_duration = int(video.duration)  # Duration in seconds

    # Compute the number of clips
    num_clips = (video_duration // clip_duration) + (1 if video_duration % clip_duration > 0 else 0)

    for i in range(num_clips):
        start_time = i * clip_duration
        end_time = min((i + 1) * clip_duration, video_duration)

        # Extract the clip
        clip = video.subclip(start_time, end_time)

        # Define output file path
        output_file_path = os.path.join(output_folder, f'clip_{i + 1}.mp4')

        # Write the clip to a file
        clip.write_videofile(output_file_path, codec='libx264', audio_codec='aac')

    print(f'Successfully split the video into {num_clips} clips.')

# Example usage
input_video_path = 'Minecraft Parkour Gameplay.WEBM'  # Replace with your input video file path
output_folder = 'Parkour Gameplay'         # Replace with your desired output folder path

split_video(input_video_path, output_folder)