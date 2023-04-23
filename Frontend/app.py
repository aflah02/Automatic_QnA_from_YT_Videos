import streamlit as st
from backend import *
from streamlit_player import st_player
from time import sleep
from streamlit_extras.stoggle import stoggle
import os
import pickle

def get_questions_and_answers(url, option):
    video_id = get_video_id(url)
    cache_set = set(list(os.listdir("cache")))
    file_name = video_id + "_" + option
    if file_name in cache_set:
        print("Loading from cache")
        response = pickle.load(open("cache/" + video_id + "_" + option, "rb"))
        return response
    else:
        print("Loading from API")
        transcript = get_transcript(url)
        chunks, chunk_time_stamps = parse_transcript_into_chunks(transcript)
        # ls_qna, chunk_time_stamps = get_placeholder_qna(chunks, chunk_time_stamps)
        ls_qna, chunk_time_stamps = get_question_and_answer(chunks, chunk_time_stamps, option)
        response = chunks, ls_qna, chunk_time_stamps
        # cache the response
        pickle.dump(response, open("cache/" + video_id + "_" + option, "wb"))
        return response


# Define the function for the Welcome Page
def welcome_page():
    st.session_state["page"] = "Welcome Page"
    st.title("Welcome!")
    # Add an input box for the user to enter a value
    input_value = st.text_input("Choose a Service:")
    url_options = ["OpenAI", "Cohere"]
    option = st.selectbox("Select a URL:", url_options)
    st.session_state["option"] = option
    # Add a button to compute the value and navigate to the Video Display Page
    if st.button("Compute"):
        # Display a spinner while the computation is in progress
        with st.spinner("Analyzing Video"):
            results = get_questions_and_answers(input_value, option)
        # Set the session state variables for the results and page
        st.session_state["results"] = results
        # save URL to session state
        st.session_state["url"] = input_value
        st.session_state["page"] = "Video Display Page"
        st.experimental_rerun()

# Define the function for the Video Display Page
def video_display_page():
    st.session_state["page"] = "Video Display Page"

    # Define session state variable
    if "is_playing" not in st.session_state:
        st.session_state.is_playing = False

    # Define callback functions
    def on_pause():
        print("Player is paused")
        st.session_state.is_playing = False
        st.write("Player is paused")

    def on_play():
        print("Player is playing")
        st.session_state.is_playing = True
        st.write("Player is playing")

    results = st.session_state.get("results")

    time_stamps = results[-1]

    pause_times = [time_stamps[i][1] for i in range(len(time_stamps))]

    # end_times = [time_stamps[i][1] for i in range(len(time_stamps))]
    # end_times = [5*(i+1) for i in range(len(time_stamps))] if st.session_state.get("end_times", None) is None else st.session_state.end_times

    # paused_at_given_end = [False for i in range(len(end_times))] if st.session_state.get("paused_at_given_end", None) is None else st.session_state.paused_at_given_end

    # st.session_state.end_times = end_times
    # st.session_state.paused_at_given_end = paused_at_given_end

    st.session_state.last_pause_time = 0 if st.session_state.get("last_pause_time", None) is None else st.session_state.last_pause_time

    st.title("Video Player with Questions and Answers")
    # 2 columns
    c1, c2 = st.columns([9,1])

    with c2:
        playing_bool = False if st.session_state.get("playing_bool", None) is None else st.session_state.playing_bool
        st.session_state.playing_bool = playing_bool
        # st.write(st.session_state.playing_bool)
        options = {
            # Onprogress is needed to get the time data
            "events": ["onPlay", "onPause", "onProgress"],
            "progress_interval": 5000,
            # "playing": st.checkbox("Playing", st.session_state.playing_bool),
            "controls": True,

        }
        # st.write(options)


    with c1:
        url = st.session_state.get("url")
        event = st_player(url, **options, key="youtube_player")

        if event.data is not None and 'playedSeconds' in event.data:
            # st.write("Time Played: ")
            # st.write(event.data['playedSeconds'])
            st.session_state.last_on_progress_time = event.data['playedSeconds']

        # if 'last_on_progress_time' in st.session_state:
        #     st.write("Last on progress time: ")
        #     st.write(st.session_state.last_on_progress_time)
        # Check if player event was triggered
        if event.name == "onPause" and st.session_state.playing_bool == True:
            print("onPause triggered")
            on_pause()
            st.session_state.playing_bool = False
            st.experimental_rerun()
        elif event.name == "onPlay" and st.session_state.playing_bool == False:
            print("onPlay triggered")
            on_play()
            st.session_state.playing_bool = True
            st.experimental_rerun()
        elif event.name == "onProgress" and st.session_state.playing_bool == True:
            print("onProgress triggered")
            # st.session_state.playing_bool = True
            # st.experimental_rerun()
        qnas = results[1]

        if st.session_state.get("last_on_progress_time", None) is None:
            current_time = 0
        else:
            current_time = st.session_state.last_on_progress_time

        current_time_slot = 0
        for i in range(len(pause_times)):
            if i == 0:
                if current_time < pause_times[i]:
                    current_time_slot = i
                    break
            if current_time < pause_times[i] and current_time >= pause_times[i-1]:
                current_time_slot = i
                break

        questions_AND_answers = qnas[current_time_slot]

        # Remove empty strings
        questions_AND_answers = [i for i in questions_AND_answers if len(i) != i.count(" ")]

        # L and R Strip
        questions_AND_answers = [i.strip() for i in questions_AND_answers]

        questions = []
        answers = []
        for i in range(len(questions_AND_answers)):
            if i % 2 == 0:
                questions.append(questions_AND_answers[i])
            else:
                answers.append(questions_AND_answers[i])

        # print(questions)
        # print(answers)

        # st.write("Current Time Slot: ")
        # st.write(current_time_slot)
        # st.write("Current Time: ")
        # st.write(current_time)
        for i in range(len(questions)):
            st.write(questions[i])
            stoggle("Click to see answer", answers[i])
            st.write("")
                


# Define the main function
def main():
    print("Running main function")
    # Initialize the session state
    if "page" not in st.session_state:
        print("Initializing session state")
        st.session_state["page"] = "Welcome Page"
    print("Current page:", st.session_state["page"])
    if st.session_state["page"] == "Welcome Page":
        welcome_page()
    elif st.session_state["page"] == "Video Display Page":
        video_display_page()

# Run the app
if __name__ == "__main__":
    main()