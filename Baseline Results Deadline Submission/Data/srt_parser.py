from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import os

def get_transcript(video_id, video_title):
    video_title = video_title.replace(" ", "_")
    ls = YouTubeTranscriptApi.get_transcript(video_id)
    ls2 = []
    # mkfilr
    with open(f"Transcripts/transcript_{video_title}.txt", "w") as f:
        for i in ls:
            f.write("Text " + str(i['text']).replace("\n","") + " Start Time " + str(i['start']) + " Duration " + str(i['duration']) + "\n")
            ls2.append([i['text'].replace("\n","") , i['start'] , i['duration']])
    df = pd.DataFrame(ls2)
    df.columns =['Text', 'Start Time', 'Duration']
    df.to_csv(f"Transcripts/transcript_{video_title}.csv", index=False)

if __name__ == '__main__':
    get_transcript("Yocja_N5s1I", "The Agricultural Revolution")
    get_transcript("n7ndRwqJYDM", "Indus Valley Civilization")
    get_transcript("sohXPx_XZ6Y", "Mesopotamia")
    get_transcript("Z3Wvw6BivVI", "Ancient Egypt")
    get_transcript("0LsrkWDCvxg", "Alexander the Great")

