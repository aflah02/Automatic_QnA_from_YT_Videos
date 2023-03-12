# import streamlit as st

# from streamlit_player import st_player, _SUPPORTED_EVENTS
    
# def main():
#     c1, c2 = st.columns([3, 3])

#     with c2:
#         st.subheader("Parameters")
 
#         options = {
#             "events": st.multiselect("Events to listen", _SUPPORTED_EVENTS, ["onProgress"]),
#             "progress_interval": 1000,
#             # "volume": st.slider("Volume", 0.0, 1.0, 1.0, .01),
#             "playing": st.checkbox("Playing", False),
#             # "loop": st.checkbox("Loop", False),
#             "controls": st.checkbox("Controls", False),
#             # "muted": st.checkbox("Muted", False),
#         }


#     with c1:
#         url = st.text_input("First URL", "https://youtu.be/c9k8K1eII4g")
#         event = st_player(url, **options, key="youtube_player")
#         st.write(options['playing'])
#         st.write(options)
#         st.write(event)
#         # list all attributes of the event
#         if event:
#             st.write(dir(event))

#         # Event[0] is onprogress etc.
#         # Event[1] is a dict with time etc.
#         st.write(event[1])


# if __name__ == "__main__":
#     main()

import streamlit as st
from streamlit_player import st_player, _SUPPORTED_EVENTS

def main():
    c1, c2 = st.columns([3, 3])
    
    # Define default options
    options = {
        "events": ["onProgress"],
        "progress_interval": 1000,
        "volume": 1.0,
        "playing": False,
        "loop": False,
        "controls": True,
        "muted": False,
    }

    # Create a button to play and pause
    with c2:
        st.subheader("Parameters")
        if st.button('Play/Pause'):
            options["playing"] = not options["playing"]
        options["volume"] = st.slider("Volume", 0.0, 1.0, 1.0, .01)
        options["loop"] = st.checkbox("Loop", options["loop"])
        options["controls"] = st.checkbox("Controls", options["controls"])
        options["muted"] = st.checkbox("Muted", options["muted"])

    with c1:
        url = st.text_input("First URL", "https://youtu.be/c9k8K1eII4g")
        event = st_player(url, **options, key="youtube_player")
        st.write(options['playing'])
        st.write(options)
        st.write(event)
        # list all attributes of the event
        if event:
            st.write(dir(event))

        # Event[0] is onprogress etc.
        # Event[1] is a dict with time etc.
        st.write(event[1])
        
if __name__ == "__main__":
    main()
