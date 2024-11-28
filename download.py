import csv
import os
import subprocess

# Function to download the video using youtube-dl and extract the segment
def download_and_extract_video(video_url, start_time, output_dir,video_id):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    complete_video_filename = os.path.join(output_dir,video_id, f"{video_id}_video_complete.mp4")
    video_filename = os.path.join(output_dir,video_id, f"{video_id}_video.mp4")
    audio_filename = os.path.join(output_dir,video_id, f"{video_id}_audio.wav")


    # Download the video with youtube-dl, starting from the specified start time
    download_command = [
        "youtube-dl",
        video_url,
        "-f", "best",  # Download the best video quality
        "--output", complete_video_filename,
        "--user-agent", "Mozilla/5.0 (Android 14; Mobile; rv:128.0) Gecko/128.0 Firefox/128.0"
    ]
    ffmpeg_video_command = [
        "ffmpeg",
        "-i", complete_video_filename,  # Input video file
        "-ss", start_time,      # Start time for the trim
        "-t", "10",             # Duration of the clip (10 seconds)
        "-c:v", "copy",         # Copy the video stream without re-encoding
        "-c:a", "copy",         # Copy the audio stream without re-encoding
        video_filename ,       # Output file name
    ]
    
    
    subprocess.run(download_command, check=False)
    print(f"Video downloaded to {video_filename}")
    
    # Run the ffmpeg command
    subprocess.run(ffmpeg_video_command, check=False)
    print(f"Video trimmed and saved to {video_filename}")

    # Convert the downloaded video to WAV using ffmpeg
    ffmpeg_command = [
        "ffmpeg",
        "-i", video_filename,  # Input video file
        "-vn",  # Disable video (no need to re-encode video)
        "-acodec", "pcm_s16le",  # Use pcm_s16le codec for WAV
        "-ar", "16000",  # Set audio sample rate to 16000Hz
        "-ac", "2",  # Set stereo audio
        audio_filename,  # Output audio file
    ]
    
    subprocess.run(ffmpeg_command, check=False)
    print(f"Audio extracted and saved to {audio_filename}")

# Read CSV file and process each line
def process_csv(csv_filename, output_dir):
    with open(csv_filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            video_id = row[0]
            start_time = row[1]
            
            # Construct the video URL (assuming it's a YouTube video)
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            print(f"Processing video {video_id} starting at {start_time}s...")
            download_and_extract_video(video_url, start_time, output_dir,video_id)

if __name__ == "__main__":
    csv_filename = "vggsound.csv"  # Path to your CSV file
    output_dir = "output_videos"  # Output directory for downloaded videos and audio

    process_csv(csv_filename, output_dir)
