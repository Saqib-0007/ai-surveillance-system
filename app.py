import tempfile
from pathlib import Path
import time
import cv2
import streamlit as st
import pandas as pd
from config import DEFAULT_MODEL, YOLO_MODELS
from core.engine import SurveillanceEngine

# =====================================================
# Page Config
# =====================================================

st.set_page_config(
    page_title="Sentinel Vision",
    page_icon="🎥",
    layout="wide",
)

# =====================================================
# Session State
# =====================================================

if "engine" not in st.session_state:
    st.session_state.engine = None

if "video_path" not in st.session_state:
    st.session_state.video_path = None

if "playing" not in st.session_state:
    st.session_state.playing = False
    
if "counting_line" not in st.session_state:
    st.session_state.counting_line = None

if "first_frame" not in st.session_state:
    st.session_state.first_frame = None

# =====================================================
# Sidebar
# =====================================================

st.sidebar.title("⚙️ Sentinel Vision")

video_source = st.sidebar.radio(
    "Input Source",
    [
        "Upload Video",
        "Webcam",
        "RTSP Camera",
    ],
)

model_choice = st.sidebar.selectbox(
    "Detection Model",
    list(YOLO_MODELS.keys()),
    index=list(YOLO_MODELS.keys()).index(DEFAULT_MODEL),
)

confidence = st.sidebar.slider(
    "Confidence",
    0.10,
    1.00,
    0.50,
    0.05,
)

playback_speed = st.sidebar.selectbox(
    "Playback Speed",
    [0.5, 1.0, 2.0, 4.0],
    index=1,
)

show_heatmap = st.sidebar.checkbox(
    "Show Heatmap",
    value=True,
)

st.sidebar.divider()

load_video = st.sidebar.button(
    "📂 Load Video",
    use_container_width=True,
)

start = st.sidebar.button(
    "▶ Start Surveillance",
    use_container_width=True,
)

stop = st.sidebar.button(
    "⏹ Stop",
    use_container_width=True,
)

# =====================================================
# Main
# =====================================================

st.title("🎥 Sentinel Vision")

st.caption("AI Smart Surveillance System")

uploaded_video = None

if video_source == "Upload Video":

    uploaded_video = st.file_uploader(
        "Upload Video",
        type=[
            "mp4",
            "avi",
            "mov",
            "mkv",
        ],
    )

elif video_source == "Webcam":

    st.info("Webcam support coming soon.")

else:

    st.info("RTSP support coming soon.")

# =====================================================
# Dashboard Layout
# =====================================================

left, right = st.columns([3, 1])

# ----------------------------
# Left - Live Video
# ----------------------------
with left:
    frame_placeholder = st.empty()

# ----------------------------
# Right - Analytics
# ----------------------------
with right:

    st.subheader("📊 Analytics")

    people_metric = st.empty()
    vehicle_metric = st.empty()
    occupancy_metric = st.empty()

    queue_metric = st.empty()
    wait_metric = st.empty()

    fps_metric = st.empty()
    frame_metric = st.empty()

# Divider after top dashboard
st.divider()

# ----------------------------
# Full Width Events Section
# ----------------------------

st.subheader("📋 Recent Events")

events_placeholder = st.empty()

st.divider()

video_info_container = st.empty()
drawing_container = st.empty()

# =====================================================
# First Frame Preview
# =====================================================

if st.session_state.first_frame is not None:

    st.subheader("Video Preview")

    preview = cv2.cvtColor(
        st.session_state.first_frame,
        cv2.COLOR_BGR2RGB,
    )

    drawing_container.image(
        preview,
        channels="RGB",
        use_container_width=True,
    )

# =====================================================
# Start
# =====================================================

if load_video:

    if uploaded_video is None:

        st.warning("Please upload a video.")

        st.stop()

    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp4",
    )

    temp.write(uploaded_video.read())

    temp.close()

    st.session_state.video_path = temp.name

    st.session_state.engine = SurveillanceEngine(
        model_name=YOLO_MODELS[model_choice],
        confidence=confidence,
    )

    st.session_state.engine.open_video(
        st.session_state.video_path
    )

    st.session_state.playing = True
    
if start:

    if st.session_state.engine is None:

        st.warning("Please load a video first.")

        st.stop()

    st.session_state.playing = True
    
# Extract First Frame
# -------------------------
    cap = cv2.VideoCapture(st.session_state.video_path)

    success, first_frame = cap.read()

    cap.release()

    if success:
        st.session_state.first_frame = first_frame

    st.session_state.playing = True

# =====================================================
# Stop
# =====================================================

if stop:

    if st.session_state.engine is not None:

        st.session_state.engine.stop()

    st.session_state.playing = False

# =====================================================
# Processing
# =====================================================

if (
    st.session_state.playing
    and st.session_state.engine is not None
):
    last_analytics = None

    info = st.session_state.engine.video_info

    video_info_container.info(
        f"""
Resolution : {info['width']} x {info['height']}

FPS : {info['fps']:.2f}

Duration : {info['duration']:.2f} sec

Frames : {info['total_frames']}
"""
    )

    while st.session_state.playing:

        annotated_frame, analytics = (
            st.session_state.engine.read_frame()
        )
        
        if analytics is not None:
            last_analytics = analytics

        if annotated_frame is None:

            break

        rgb = cv2.cvtColor(
            annotated_frame,
            cv2.COLOR_BGR2RGB,
        )

        frame_placeholder.image(
            rgb,
            channels="RGB",
            width="stretch",
        )

        people_metric.metric(
            "People",
            f'{analytics["people"]} ({analytics["unique_people"]})',
        )

        vehicle_metric.metric(
            "Vehicles",
            f'{analytics["vehicles"]} ({analytics["unique_vehicles"]})',
        )
        
        occupancy_metric.metric(
            "Zone Occupancy",
            analytics["occupancy"],
        )
        
        queue_metric.metric(
            "Queue Size",
            analytics["queue_size"],
        )

        wait_metric.metric(
            "Average Wait",
            f'{analytics["average_wait"]:.1f} sec',
        )        

        fps_metric.metric(
            "FPS",
            analytics["fps"],
        )

        frame_metric.metric(
            "Frame",
            analytics["frame"],
        )
        
        events = []

        for event in analytics["events"][:100]:
        
            details = event.get("details", "")
        
            if isinstance(details, dict):
                details = ", ".join(
                    f"{k}: {v}"
                    for k, v in details.items()
                )
        
            events.append({
                "Time": event.get("timestamp", "--"),
                "Event": event.get("type", "--"),
                "Object": f"{event.get('label', '--')} #{event.get('object_id', '--')}",
                "Details": details,
            })
        
        df = pd.DataFrame(events)
        
        events_placeholder.dataframe(
            df,
            use_container_width=True,
            height=350,
            hide_index=True,
        )
        
        frame_delay = 1.0 / max(info["fps"], 1)

        time.sleep(frame_delay / playback_speed)

    st.session_state.playing = False

    csv_file = (
        st.session_state.engine
        .processor
        .metrics
        .report
        .export_csv(
            st.session_state.engine
            .processor
            .metrics
            .events
            .get_events()
        )
    )
    
    if last_analytics is None:
        st.error("No analytics available.")
        st.stop()

    report_analytics = {
        "people": last_analytics["people"],
        "vehicles": last_analytics["vehicles"],
        "occupancy": last_analytics["occupancy"],
        "queue_size": last_analytics["queue_size"],
        "average_wait": last_analytics["average_wait"],
    }

    pdf_file = (
        st.session_state.engine
        .processor
        .metrics
        .report
        .export_pdf(
            st.session_state.engine
            .processor
            .metrics
            .events
            .get_events(),
            report_analytics,
        )
    )        

    st.success(f"CSV report saved to: {csv_file}")

    with open(csv_file, "rb") as file:

        st.download_button(
            label="📥 Download CSV Report",
            data=file,
            file_name="sentinel_vision_report.csv",
            mime="text/csv",
            use_container_width=True,
        )
        
    with open(pdf_file, "rb") as file:

        st.download_button(
            label="📄 Download PDF Report",
            data=file,
            file_name="sentinel_vision_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    if st.session_state.engine is not None:
        st.session_state.engine.stop()

    if st.session_state.video_path:

        Path(
            st.session_state.video_path
        ).unlink(
            missing_ok=True
        )

        st.session_state.video_path = None