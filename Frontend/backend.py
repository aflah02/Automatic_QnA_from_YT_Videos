from youtube_transcript_api import YouTubeTranscriptApi
import os
from config_keys import *
import openai

openai.api_key = open_ai_key

def get_video_id(url):
    if "youtu.be" in url:
        video_id = url.split("/")[-1]
    elif "youtube.com" in url:
        video_id = url.split("=")[-1]
    return video_id

def get_transcript(url):
    video_id = get_video_id(url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    return transcript

def parse_transcript_into_chunks(transcript, chunk_size=5):
    max_time = transcript[-1]['start'] + transcript[-1]['duration']
    time_per_chunk = max_time / chunk_size
    curr_start = 0
    curr_end = time_per_chunk
    chunks = []
    chunk_time_stamps = []
    curr_str = ""
    for i in range(len(transcript)):
        if transcript[i]['start'] >= curr_end:
            chunks.append(curr_str)
            chunk_time_stamps.append((curr_start, curr_end))
            curr_str = ""
            curr_start = curr_end
            curr_end += time_per_chunk
        curr_str += transcript[i]['text'] + " "
    return chunks, chunk_time_stamps

def get_question_and_answer(chunks, chunk_time_stamps):
    all_qna = []
    for chunk in chunks:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": """Generate 5 questions on the following paragraph in the form "Question":, "Answer":. The text is a piece of youtube video transcript so ignore all noisy information which is irrelevant and only focus on the educational material."""},
                    {"role": "assistant", "content": "Sure provide the piece of text to generate questions from"},
                    {"role": "user", "content": f"Text: {chunk}"}
                ]
            )
        ls_qna = resp["choices"][0]["message"]["content"].split('\n')
        # remove all empty strings
        ls_qna_filtered = []
        for qna in ls_qna:
            if qna != '':
                ls_qna_filtered.append(qna)
        all_qna.append(ls_qna_filtered)
    return all_qna, chunk_time_stamps

def get_placeholder_qna(chunks, chunk_time_stamps):
    ls_qna = []
    for chunk in chunks:
        # generate 5 random strings for question and 5 random strings for answer
        sub_ls_qna = []
        for i in range(5):
            sub_ls_qna.append(f"Question {i}: Placeholder Question")
            sub_ls_qna.append(f"Answer {i}: Placeholder Answer")
        ls_qna.append(sub_ls_qna)
    print("Done!")
    return ls_qna, chunk_time_stamps

# transcript = get_transcript("https://www.youtube.com/watch?v=Z6nkEZyS9nA")

# chunks, chunk_time_stamps = parse_transcript_into_chunks(transcript, chunk_size=5)

# for i in range(len(chunks)):
#     print("Chunk", i, ":", chunks[i])
#     print("Chunk", i, "Time Stamps:", chunk_time_stamps[i])
#     print()

if __name__ == "__main__":
    get_placeholder_qna("https://youtu.be/ylWORyToTo4")