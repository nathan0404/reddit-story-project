# reddit-story-project
This project is designed to automatically convert Reddit stories into narrated video content with gameplay footage. It reads text from a Reddit post, generates speech using Google's Text-to-Speech API, and then combines it with video gameplay to create a visually engaging video that is suitable for YouTube or similar platforms. The process involves several steps, including text extraction, speech synthesis, video editing, and combining the elements into the final output.

Key Features:
Text Extraction: The project begins by extracting relevant details from a Reddit post. It processes a text file containing the subreddit, user, and story content, and formats the text for easier manipulation.

Text-to-Speech (TTS): Using Google's Cloud Text-to-Speech API, each sentence from the extracted Reddit post is converted into audio. The TTS service allows you to customize the voice, speaking rate, and pitch, producing a high-quality narration of the story.

Text Display: The text of the story is displayed dynamically in sync with the speech. Each word or sentence is shown on the screen for a specific duration, ensuring it aligns with the spoken content.

Gameplay Footage: The project integrates gameplay footage (in this case, Minecraft parkour or other clips) as background video. This footage is cropped and resized to fit the vertical video format, providing an immersive experience for the viewer.

Combining Text, Audio, and Video: The generated TTS audio is synchronized with the on-screen text and gameplay footage. The video is composed of the following layers:

The gameplay footage as the background.
The text clips that appear in sync with the TTS audio.
The audio narration playing alongside the text.
Video Export: Finally, the project exports the combined content as a video file (MP4) ready for uploading to platforms like YouTube or sharing with an audience.

Workflow:
Text Processing: The Reddit story is read from a text file. The program processes the text to extract the necessary information, including the subreddit, user, and post content.

Speech Generation: Each sentence is converted into an audio file using Google's Text-to-Speech service. The duration of each audio clip is calculated based on the length of the sentence, ensuring that the audio and the text are synchronized.

Text Clips Creation: Each sentence is displayed as text on the screen, with each word appearing for a specific duration in sync with the audio.

Video Editing: The gameplay footage is trimmed to match the length of the audio and resized to fit the vertical format. The gameplay and text clips are then combined into one video.

Final Video Creation: The final video is composed by combining the gameplay footage with the text and audio clips. The video is exported and saved as a file.

Libraries and Technologies:
Google Cloud Text-to-Speech: Used for converting the text into natural-sounding speech.
MoviePy: A Python library for video editing that helps in processing the gameplay footage, creating text clips, and combining the video and audio elements.
Regular Expressions (re): Used for processing and formatting the text extracted from the Reddit story.
Use Cases:
Reddit Story Videos: Convert Reddit posts, particularly interesting or funny stories, into engaging video content with narration and background gameplay.
Automated Video Creation: Streamline the process of creating videos based on written content by automating text-to-speech, video editing, and content synchronization.
This project demonstrates how to leverage text-to-speech technology and video editing to create multimedia content from text-based sources like Reddit posts.
