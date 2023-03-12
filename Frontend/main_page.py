import streamlit as st
from streamlit_player import st_player
from backend import *
from time import sleep


def main():

    st.session_state.videoReady = False if st.session_state.get("videoReady", None) is None else st.session_state.videoReady

    st.session_state.qna = None if st.session_state.get("qna", None) is None else st.session_state.qna

    if st.session_state.videoReady:

        c1, c2 = st.columns([5, 3])

        with c2:
            playing_bool = False if st.session_state.get("playing_bool", None) is None else st.session_state.playing_bool
            st.write(playing_bool)
            options = {
                "events": ["onProgress"],
                "progress_interval": 1000,
                "playing": st.checkbox("Playing", playing_bool),
            }
            st.session_state.playing_bool = options["playing"]
            st.write(options)


        with c1:
            url = st.text_input("Video URL", "https://youtu.be/ylWORyToTo4")
            event = st_player(url, **options, key="youtube_player")
            st.write(event)
            while event is None or event.data is None or event.data['playedSeconds'] is None:
                continue
            print(event.data['playedSeconds'])
            st.write(st.session_state.qna)
            # print(event["data"])

            # if event:
            #     if event[1]['playedSeconds'] > 5:
            #         st.write("Played more than 5 seconds")
            #         st.session_state.playing_bool = False
    
    else:
        st.write("Video not ready")
        url = st.text_input("Video URL", "https://youtu.be/ylWORyToTo4")
        progress_text = "Getting transcript..."
        my_bar = st.progress(0, text=progress_text)
        percent_complete = 0
        while percent_complete < 100:
            if percent_complete < 25:
                transcript = get_transcript(url)
                progress_text = "Parsing transcript..."
                sleep(1)
                percent_complete = 25
                print(percent_complete)
                my_bar.progress(percent_complete, text=progress_text)
            elif percent_complete < 50 and percent_complete >= 25:
                chunks, chunk_time_stamps = parse_transcript_into_chunks(transcript)
                progress_text = "Getting Q&A..."
                sleep(1)
                percent_complete = 50
                print(percent_complete)
                my_bar.progress(percent_complete, text=progress_text)
            elif percent_complete < 75 and percent_complete >= 50:
                # ls_qna, chunk_time_stamps = get_question_and_answer(chunks, chunk_time_stamps)
                ls_qna, chunk_time_stamps = get_placeholder_qna(chunks, chunk_time_stamps)
                st.session_state.qna = ls_qna
                sleep(1)
                progress_text = "Done!"
                percent_complete = 75
                print(percent_complete)
                my_bar.progress(percent_complete, text=progress_text)
            else:
                progress_text = "Done!"
                percent_complete = 100
                sleep(1)
                print(percent_complete)
                my_bar.progress(percent_complete, text=progress_text)

        st.write("Video ready")
        st.write(st.session_state.qna)
        st.session_state.videoReady = True

        # wait for 5 seconds
        # time.sleep(5)
        # reload the page
        # st.experimental_rerun()



if __name__ == "__main__":
    main()