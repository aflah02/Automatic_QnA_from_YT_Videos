from youtube_transcript_api import YouTubeTranscriptApi
import os
from config_keys import *
import openai

openai.api_key = open_ai_key
# resp = [['1. "What is Song Glorious and how is it unique from traditional gift options?" ', '2. "How much does it cost to order a personalized song from Song Glorious?" ', '3. "How did the founders come up with the idea for Song Glorious?" ', '4. "How has the business been doing in terms of sales and profit?" ', '5. "What are the founders\' plans for expanding the business in the future?"'], ['Question 1: What does the company Synthesia do?', 'Answer: Synthesia replicates voices for various languages using artificial intelligence.', "Question 2: What was Peter's offer for the partnership?", 'Answer: Peter offered to buy a third of the business for $400,000.', 'Question 3: What does Damon request in the partnership negotiation?', 'Answer: Damon requests a 7% ownership stake in the business.', 'Question 4: What does range Beauty offer?', 'Answer: range Beauty offers clean beauty products with botanicals specially made for eczema and acne-prone skin.', 'Question 5: What do the founders of range Beauty seek in their pitch to the sharks?', 'Answer: The founders seek $150,000 for a 6% equity stake in their company to expand their inclusive makeup and natural skincare line.'], ['Question: What is the main focus of the makeup line discussed in the text? ', 'Answer: The makeup line is focused on creating products that cater to people with eczema and acne, and creating makeup shades that are inclusive of different skin tones, specifically prioritizing black women and women of color. ', 'Question: What experience led the founder of the makeup brand to create a line that focuses on eczema and acne? ', 'Answer: The founder of the makeup brand had cystic acne and eczema, and noticed that a lot of black models on runway shows and campaign shoots had to bring their own makeup because the makeup artists did not have shades that catered to their skin tones. ', 'Question: How did the makeup brand utilize e-commerce to grow their business? ', 'Answer: The makeup brand created a sample kit that customers could purchase online to find their perfect shade, and offered $5 towards a full-size product if they bought the sample. 80% of customers who purchased the sample kit came back to buy a full-size product. ', "Question: What contributed to the makeup brand's increase in sales in 2019? ", 'Answer: The makeup brand was featured by Beyonce on her website and covered by major publications. Additionally, there was a spotlight on black-owned businesses, which gave the brand exposure that they did not have the marketing budget for. ', "Question: How many shades does the makeup brand's foundation come in? ", "Answer: The makeup brand's foundation comes in 21 shades, ranging from fair to deep."], ['Question: What is the 15 pledge and how does it help black owned businesses?', 'Answer: The 15 pledge is a non-profit which helps increase the level of sales with black owned businesses, and it means that all of these businesses are looking at how to increase their sales.', 'Question: What does it mean when they say "making it work on the shop floor?"', 'Answer: "Making it work on the shop floor" means making the product successful and generating sales once it is made available for purchase.', 'Question: What is Black Sands Entertainment?', "Answer: Black Sands Entertainment is a black-owned publishing house which creates content and characters that represent the black community's historical achievements before slavery. ", 'Question: What is the revenue stream of Black Sands Entertainment?', 'Answer: Most of the revenue stream for Black Sands Entertainment is from physical books, and they are on track to sell around 120,000 units this year directly to consumers. ', 'Question: What is the benefit of having Two Sharks on board?', 'Answer: The benefit of having Two Sharks on board is to get all their knowledge and expertise in every arena which can really help a business a lot.']]

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
                    {"role": "user", "content": """Generate 5 questions on the following paragraph in the form "Question":, "Answer":. Strictly follow this template for replying and do not add any other information. The text is a piece of youtube video transcript so ignore all noisy information which is irrelevant and only focus on the educational material. Any information which seems to be irrelevant and only part of small talk MUST NOT be included in the Questions and Answers. I will provide the paragraph so kindly await my response. Reply with 'Sure provide the piece of text to generate questions from' if you undestood the task"""},
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
    # print("Done!")
    return ls_qna, chunk_time_stamps

# transcript = get_transcript("https://www.youtube.com/watch?v=Z6nkEZyS9nA")

# chunks, chunk_time_stamps = parse_transcript_into_chunks(transcript, chunk_size=5)

# for i in range(len(chunks)):
#     print("Chunk", i, ":", chunks[i])
#     print("Chunk", i, "Time Stamps:", chunk_time_stamps[i])
#     print()

if __name__ == "__main__":
    get_placeholder_qna("https://youtu.be/ylWORyToTo4")