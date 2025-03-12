import re

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

# Test the function
text = "My husband 40 male was recently asked by his 52 year-old female boss if she could take him out for lunch at Hell‘s kitchen. I admittedly was a little upset to hear that he had taken her up on this offer because him and I always planned to go to Hell’s kitchen together. We watch the show together. We’re both fans of Gordon Ramsay and we always talked about going together for the first time one day. The only issue was money saving up for it, but she can afford it easily. His boss lost her husband unexpectedly a few years ago and has one son who she doesn’t get along with. She is very attractive for her age and seems to really favor my husband. Am I the A hole for getting upset with him for accepting this offer, or am I being jealous and dramatic? We’ve been arguing about it for a couple of days now."
result = split_and_group_words_and_numbers(text)
