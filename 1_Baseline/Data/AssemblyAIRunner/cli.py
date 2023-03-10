import requests
import json
import os
import youtube_dl
from time import sleep
import urllib, urllib.request, json
from config import *

def fetch_yt_video(url):
    ID = url.split('=')
    VideoID = ID[1]
    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % VideoID}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string
    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        try:
            data = json.loads(response_text.decode())
        except ValueError as e:
            pass
        if data is not None:
            author = data['author_name'].split(' - ')
            author = author[0].rstrip()
            title = data['title']
            # replace all non-alphanumeric characters with _
            title = ''.join(e for e in title if e.isalnum() or e == ' ')
            title = title.replace(' ', '_')
            return author, title

ydl_opts = {
   'format': 'bestaudio/best',
   'postprocessors': [{
       'key': 'FFmpegExtractAudio',
       'preferredcodec': 'mp3',
       'preferredquality': '192',
   }],
   'ffmpeg-location': './',
   'outtmpl': "./Audio_Downloads/%(id)s.%(ext)s",
}



transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
upload_endpoint = 'https://api.assemblyai.com/v2/upload'

headers_auth_only = {'authorization': auth_key}
headers = {
    "authorization": auth_key,
    "content-type": "application/json"
}
CHUNK_SIZE = 5242880

def transcribe_from_link(link, categories: bool):
    _id = link.strip()
    title = fetch_yt_video(link)[1]
    ydl_opts['outtmpl'] = "./Audio_Downloads/" + title + ".%(ext)s"
    def get_vid(_id):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(_id)
    meta = get_vid(_id)
    
    save_location = ydl_opts['outtmpl'].replace('%(ext)s', 'mp3')

    duration = meta['duration']
    print('Saved mp3 to', save_location)
    def read_file(filename):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(CHUNK_SIZE)
                if not data:
                    break
                yield data
  
    upload_response = requests.post(
        upload_endpoint,
        headers=headers_auth_only, data=read_file(save_location)
    )
    audio_url = upload_response.json()['upload_url']
    print('Uploaded to', audio_url)
    transcript_request = {
        'audio_url': audio_url,
        'iab_categories': 'True' if categories else 'False',
    }
 
    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    transcript_id = transcript_response.json()['id']
    polling_endpoint = transcript_endpoint + "/" + transcript_id
    print("Transcribing at", polling_endpoint)
    polling_response = requests.get(polling_endpoint, headers=headers)
    while polling_response.json()['status'] != 'completed':
        sleep(30)
        try:
            polling_response = requests.get(polling_endpoint, headers=headers)
        except:
            print("Expected wait time:", duration*2/5, "seconds")
            print("After wait time is up, call poll with id", transcript_id)
            return transcript_id
   # Save Polling Response.json()
    title = fetch_yt_video(link)[1]
    # replace all non-alphanumeric characters with _
    
    result = polling_response.json()
    with open(f"../Transcripts/{title}_json", 'w') as f:
        json.dump(result, f)
    with open(f"../Transcripts/{title}_text", 'w') as f:
        f.write(polling_response.json()['text'])
    print('Transcript saved to', title)

links = [
    "https://www.youtube.com/watch?v=Yocja_N5s1I",
    "https://www.youtube.com/watch?v=n7ndRwqJYDM",
    "https://www.youtube.com/watch?v=nbuM0aJjVgE",
    "https://www.youtube.com/watch?v=nxmWfbXS4Pw",
    "https://www.youtube.com/watch?v=T_sGTspaF4Y",
]

for link in links:
    transcribe_from_link(link, True)