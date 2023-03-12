import streamlit as st

from streamlit_player import st_player


def main():
    c1, c2 = st.columns([5, 3])

    with c2:
        playing_bool = True if st.session_state.get("playing_bool", None) is None else st.session_state.playing_bool
        st.write(playing_bool)
        options = {
            "events": ["onProgress"],
            "progress_interval": 1000,
            "playing": st.checkbox("Playing", playing_bool),
        }
        st.session_state.playing_bool = options["playing"]
        st.write(options)


    with c1:
        url = st.text_input("Video URL", "https://youtu.be/c9k8K1eII4g")
        event = st_player(url, **options, key="youtube_player")
        if event:
            if event[1]['playedSeconds'] > 5:
                st.write("Played more than 5 seconds")
                st.session_state.playing_bool = False

if __name__ == "__main__":
    main()