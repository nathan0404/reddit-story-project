from video_processing import process_reddit_text, split_text, text_to_speech, create_text_clip, audio_length, combine_text_audio, combine_clips, load_gameplay, combine_video, download_video

def main():
    # Example text block
    text_file = "Reddit Story.txt"
    gameplay_name = "clip_7.mp4"

    text_block = process_reddit_text(text_file)

    # Split text into sentences
    sentences = split_text(text_block)

   # Combine text and audio clips
    combined_clips = []
    title = 1
    for sentence in sentences:
        file_name = text_to_speech(sentence, title)
        word_duration = audio_length(sentence, file_name)
        text_clip = create_text_clip(sentence, word_duration)
        concatenated_clip = combine_text_audio(text_clip, file_name)
        #buffered_concatenated_clip = add_buffer_clip(concatenated_clip)
        combined_clips.append(concatenated_clip)
        title += 1
        print()

    #combine all tts clips together
    final_tts = combine_clips(combined_clips)
    
    # Load gameplay footage
    gameplay = load_gameplay(gameplay_name, final_tts)
    
    # Combine TTS and gameplay footage
    final_clip = combine_video(gameplay, final_tts)
    
    # Download the final video
    download_video(final_clip, "final_output.mp4")

if __name__ == "__main__":
    main()
