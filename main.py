import streamlit as st
from streamlit_webrtc import webrtc_streamer,RTCConfiguration
import cv2
import av
import pandas as pd
import numpy as np
from utilities.util import VideoProcessor


def main():
    st.header("Streaming")
    webrtc_streamer(key = 'key', video_processor_factory = VideoProcessor,
                    rtc_configuration=RTCConfiguration(
                        {"iceServers":[{"urls":["stun:stun.l.google.com:19302"]}]}
                        )
                    )

if __name__ == "__main__":
    main()