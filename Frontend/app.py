import streamlit as st
from streamlit_player import st_player
from backend import get_placeholder_qna

def main():
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
        ls_qna, chunk_time_stamps = get_placeholder_qna(url)
        event = st_player(url, **options, key="youtube_player")
        st.write(event)
        while event is None or event.data is None or event.data['playedSeconds'] is None:
            continue
        print(event.data['playedSeconds'])
        st.write(ls_qna)
        st.write(chunk_time_stamps)
        # print(event["data"])

        # if event:
        #     if event[1]['playedSeconds'] > 5:
        #         st.write("Played more than 5 seconds")
        #         st.session_state.playing_bool = False


if __name__ == "__main__":
    main()