import os, re
from google.cloud import texttospeech
from moviepy.editor import VideoFileClip, ColorClip, TextClip, AudioFileClip, AudioClip, concatenate_videoclips, concatenate_audioclips, CompositeVideoClip
from moviepy.video.fx.all import crop

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'redditai-bot-stories-97723579a403.json'
client = texttospeech.TextToSpeechClient()

    
def process_reddit_text(file_path):
    # Read all lines from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Remove empty lines and strip leading/trailing whitespace
    #lines = [line.strip() for line in lines if line.strip()] taken out and formatting when put into text file
    
    # Check if we have at least two lines
    if len(lines) < 3:
        return "Insufficient data in the file."

    # Extract subreddit (first line) and user (second line)
    subreddit = lines[0]
    if not lines[1].strip():
        user = "anonymous"    #initlize empty user if no user or if wanted to remove user
    else: 
        user = lines[1] 
    title = lines[2]
    
    # Sanitize subreddit and user
    subreddit = re.sub(r'[r/]', '', subreddit)
    user = re.sub(r'[u/]', '', user)
    
    # Extract text (everything after the second line)
    text = ''.join(lines[3:]).strip()  # Join all remaining lines and strip leading/trailing whitespace

    # Format the output
    output = f"Post on Subreddit. r slash {subreddit}. Written by User. u slash {user}. {title}. {text}"
    #output 2 is subreddit name, output 4 is username
    return output


def split_text(text_block):
    # Split text on periods, commas, exclamation marks, question marks, and newlines
    sentences = re.split(r'[.,!?]\s*|\n+', text_block)
    
    split_sentences = []
    for sentence in sentences:
        sentence_parts = split_and_group_words_and_numbers(sentence)
        if isinstance(sentence_parts, list):
            for item in sentence_parts:
                if item.strip():  # Exclude empty strings or strings that are only whitespace
                    split_sentences.append(item.strip())
        else:
            if sentence_parts.strip():  # Exclude empty strings or strings that are only whitespace
                split_sentences.append(sentence_parts.strip())
    return split_sentences

def split_and_group_words_and_numbers(text):
    text = list(text)
    i = 0
    while len(text)-1 > i:
        if text[i].isalpha() and text[i+1].isalpha():
           text[i] = text[i] + text[i+1]
           del text[i+1]
        elif text[i].isdigit() and text[i+1].isdigit():
           text[i] = text[i] + text[i+1]
           del text[i+1]
        else:
           i+=1
    print(text)
    text = combine_words(text)
    print(text)
    return text
def combine_words(text):
    i = 0
    while len(text)-1 > i:
        if text[i] == '(':
            while  i < len(text)-1 and text[i+1] != ')':
                text[i] = text[i] + text[i+1]
                del text[i+1]
            if i < len(text)-1 and text[i+1] == ')':
                text[i] = text[i] + text[i+1]
                del text[i+1]
            i+=1
        elif text[i] == 'u' and text[i+2] == 'slash':
            while i < len(text)-1:
                text[i] = text[i] + text[i+1]
                del text[i+1]
            i+=1
        elif not text[i].isdigit() and not text[i+1].isdigit() and not text[i+1] == '(':
            text[i] = text[i] + text[i+1]
            del text[i+1]
        else:
           i+=1
    return text

def text_to_speech(sentence, title):
    file_name = f"audio_clip {title}.mp3"
    synthesis_input = texttospeech.SynthesisInput(text=sentence) 
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name='en-US-Standard-E'
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.2, #changed from 1
        pitch=0.0
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    #saves audio to computer
    with open(file_name, "wb") as output:
        output.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
    return file_name

def load_audio(audio_name):
    #Load an audio file (f"audio_clip {sentence}.mp3")
    audio_clip = AudioFileClip(audio_name)
    return audio_clip

def audio_length(sentence, audio_name):
    # Define the words you want to display
    if 1 < len(sentence):
        words = sentence.split()
    else:
        words = sentence
    audio_clip = load_audio(audio_name)
    #find duration of clip in seconds
    duration_s = audio_clip.duration
    # Duration for each word to appear 
    word_duration = 1
    subtrahend = 0
    divisor = len(words)
    if audio_name in ['audio_clip 1.mp3', 'audio_clip 3.mp3']: #if case for subreddit and user
        while word_duration > 0.308: #0.37
            word_duration = (duration_s - subtrahend) / divisor
            subtrahend += 0.02
    elif len(words) == 1: #if case single word, so should take up entire duration 
        while word_duration > 0.25: #if case, splits words through entire duration 0.23
            word_duration = (duration_s - subtrahend) / divisor
            subtrahend += 0.02  
    elif len(words) == 3 and words[0] in ["u", "r"]: #if case, for reading subreddit and user, should take up etnire duration
        word_duration = duration_s - 0.4
    elif len(words) < 6:
        while word_duration > 0.18: #if case, splits words through entire duration 0.23
            word_duration = (duration_s - subtrahend) / divisor
            subtrahend += 0.02 
    else:
        word_duration = (duration_s - 1) / divisor
    '''
    elif len(words) < 10:
        while word_duration > 0.19: #if case, splits words through entire duration 0.23
            word_duration = (duration_s - subtrahend) / divisor
            subtrahend += 0.02
    elif len(words) < 15:
        while word_duration > 0.175: #if case, splits words through entire duration 0.23
            word_duration = (duration_s - subtrahend) / divisor
            subtrahend += 0.02
    else:
        while word_duration > 0.165: #else case, splits words through entire duration, for too long of a sentence 0.3
            word_duration = (duration_s - subtrahend) / divisor
            subtrahend += 0.02'''
    
    print(word_duration) # seconds
    return word_duration #returned in seconds

def combine_text_words(words):
    target_words = ["my", "he", "she", "you", "me", "I", "we", "us", "this", "them", "that", 
                    "am", "is", "are", "was", "were", "be", "being", "been"]
    i = 0
    while i < len(words):
        word = words[i]
        if word in target_words and i + 1 < len(words):
            # Combine 'my' with the following word
            words[i] = f"{word} {words[i + 1]}"
            del words[i + 1]  # Remove the next word since it's combined
        elif word in ["u", "r"] and i + 2 < len(words) and words[i + 1] == "/":
            # Combine 'my' with the following word
            words[i] = f"{word}{words[i + 1]}{words[i+2]}"
            del words[i + 2]  # Remove the next word since it's combined
            del words[i + 1]  # Remove the next word since it's combined
        else:
            i += 1
    return words

def create_text_clip(sentence, word_duration):
    # Define the words you want to display
    words = sentence.split()
    words = [word.replace('slash', '/') for word in words]
    words = combine_text_words(words)
    print(words)
    #where to put texts
    text_clips = []

    for word in words:
        text_clip = TextClip(word, fontsize=150, font= 'Impact', color='white', stroke_color = 'black', stroke_width = 5, method='caption', bg_color='transparent', size=(1080, 1920), align='center', kerning = -10)
        if ' ' in word and 1 < len(words):
            text_clip = text_clip.set_duration(word_duration*2)
        else:
            text_clip = text_clip.set_duration(word_duration)
        text_clip = text_clip.set_position('center')
        text_clips.append(text_clip) 

    concatenated_text = concatenate_videoclips(text_clips, method="compose")
    return concatenated_text #returns a text clip of entire sentence

def combine_text_audio(text_clips, audio_name):
    # Load the audio clip
    audio_clip = load_audio(audio_name)
    # Combine the text clips with the audio
    concatenated_clip = text_clips.set_audio(audio_clip)
    # Get the file size of the audio clip in bytes
    file_size = os.path.getsize(audio_name)
    # Define size threshold (e.g., 10 KB)
    size_threshold = 10 * 1024  # 10 KB in bytes
    # Add buffer if file size exceeds the threshold
    if file_size > size_threshold:
        added_buffer = add_buffer_clip(concatenated_clip)
    else:
        added_buffer = add_smaller_buffer_clip(concatenated_clip)
    return added_buffer

def create_smaller_buffer_clip():
#create buffer clip to be placed inbetween clips
    buffer_audio = AudioClip(lambda t: 0, duration=0.1) #0.75
    buffer_video = ColorClip(size=(720, 720), color=(0,0,0,0), duration=0.1)
    buffer_clip = buffer_video.set_audio(buffer_audio)
    return buffer_clip
def add_smaller_buffer_clip(concatenated_clip):
    buffer_clip = create_smaller_buffer_clip()
    added_buffer = concatenate_videoclips([concatenated_clip, buffer_clip])
    return added_buffer

def create_buffer_clip():
#create buffer clip to be placed inbetween clips
    buffer_audio = AudioClip(lambda t: 0, duration=0.4) #0.75
    buffer_video = ColorClip(size=(720, 720), color=(0,0,0,0), duration=0.4)
    buffer_clip = buffer_video.set_audio(buffer_audio)
    return buffer_clip
def add_buffer_clip(concatenated_clip):
    buffer_clip = create_buffer_clip()
    added_buffer = concatenate_videoclips([concatenated_clip, buffer_clip])
    return added_buffer

def combine_clips(concatenated_clips):
    #initilize all concatenated clips
    tts = concatenate_videoclips(concatenated_clips, method="compose")
    return tts
  
def load_gameplay(file_name, final_tts):
    #"Minecraft Parkour Gameplay.WEBM"
    #load video clip/gameplay
    video_clip = VideoFileClip(file_name)
    # Duration for each word to appear
    duration_final_tts = final_tts.duration
    # getting subclip as video is large 
    sub_clip = video_clip.subclip(0, duration_final_tts)
    #resizing to veritcal
    resized_clip = resize_to_vertical_video(sub_clip)
    return resized_clip
def resize_to_vertical_video(video_clip_name):
    video = video_clip_name.resize(height=1920)
    resized_clip = video.crop(x1=1166.6,y1=0,x2=2246.6,y2=1920)
    return resized_clip 

def combine_video(gameplay, tts):
    #combine audio+text and gameplay
    final_clip = CompositeVideoClip([gameplay, tts])
    return final_clip

def download_video(final_clip, name_of_file):
    # Write the final video to a file
    final_clip.write_videofile(name_of_file, fps=30)
