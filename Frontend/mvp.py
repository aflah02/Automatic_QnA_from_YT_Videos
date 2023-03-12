import streamlit as st
import time
from backend import *
from streamlit_player import st_player

# Define a function to count the number of consonants and vowels in a string
def get_questions_and_answers(url):
    transcript = get_transcript(url)
    chunks, chunk_time_stamps = parse_transcript_into_chunks(transcript)
    ls_qna, chunk_time_stamps = get_placeholder_qna(chunks, chunk_time_stamps)
    # ls_qna, chunk_time_stamps = get_question_and_answer(chunks, chunk_time_stamps)
    return chunks, ls_qna, chunk_time_stamps

# Define the function for the Welcome Page
def welcome_page():
    st.title("Welcome Page")
    # Add an input box for the user to enter a value
    input_value = st.text_input("Enter a url:")
    # Add a button to compute the value and navigate to the Video Display Page
    if st.button("Compute and Go to Video Display Page"):
        # Display a spinner while the computation is in progress
        with st.spinner("Analyzing Video"):
            results = get_questions_and_answers(input_value)
            print("Done")
        # Set the session state variables for the results and page
        st.session_state["results"] = results
        # save URL to session state
        st.session_state["url"] = input_value
        st.session_state["page"] = "Video Display Page"
        st.experimental_rerun()

# Define the function for the Video Display Page
def video_display_page():
    st.title("Video Display Page")
    # 2 columns
    c1, c2 = st.columns([5, 3])

    with c2:
        playing_bool = False if st.session_state.get("playing_bool", None) is None else st.session_state.playing_bool
        st.session_state.playing_bool = playing_bool
        st.write(playing_bool)
        options = {
            "events": ["onProgress"],
            "progress_interval": 1000,
            "playing": st.checkbox("Playing", playing_bool),
        }
        st.session_state.playing_bool = options["playing"]
        st.write(options)


    with c1:
        url = st.session_state.get("url")
        event = st_player(url, **options, key="youtube_player")
        st.write(event)
        # while event is None or event.data is None or event.data['playedSeconds'] is None:
        #     continue
        print(event.data['playedSeconds'])

        # Get the results from the session state
        results = st.session_state["results"]
        # Display the results on the page
        st.write(results)

# Define the main function
def main():
    # Initialize the session state
    if "page" not in st.session_state:
        st.session_state["page"] = "Welcome Page"

    # Display the appropriate page based on the session state
    if st.session_state["page"] == "Welcome Page":
        welcome_page()
    elif st.session_state["page"] == "Video Display Page":
        video_display_page()

# Run the app
if __name__ == "__main__":
    main()
