import streamlit as st
import os
import tempfile
from text_processing import extract_text_from_pdf
from ai_engine import summarize_text, generate_audio

st.set_page_config(
    page_title="Paper-to-Pod | AI Audio Research Assistant",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a modern look
st.markdown("""
<style>
    /* 1. Import Open Sans from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap');

    :root {
        --bg-color: #050505;
        --card-bg: rgba(255, 255, 255, 0.03);
        --border-color: rgba(255, 255, 255, 0.1);
        --accent-glow: radial-gradient(circle at 50% -20%, #1e1f24, #050505);
    }

    /* 2. Apply Open Sans to the entire App */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Open Sans', sans-serif !important;
        background: var(--bg-color);
        background-image: var(--accent-glow);
        color: #ffffff;
    }

    /* 3. Refined Typography for Open Sans */
    h1, h2, h3 {
        font-family: 'Open Sans', sans-serif !important;
        font-weight: 700;
        letter-spacing: -0.02em; /* Tighter spacing for a modern look */
        background: linear-gradient(to bottom, #fff 40%, rgba(255,255,255,0.6));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    p, span, label {
        font-family: 'Open Sans', sans-serif !important;
        font-weight: 400;
        color: #a1a1aa;
    }

    /* 4. Sleek Card Container */
    .block-container {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 28px;
        padding: 4rem 3rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 40px 100px -20px rgba(0, 0, 0, 0.8);
        max-width: 850px;
        margin: 2rem auto;
    }

    /* 5. Custom File Uploader to match your latest screenshot */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.01);
        border: 1px dashed rgba(255, 255, 255, 0.2) !important;
        border-radius: 16px !important;
    }

    [data-testid="stFileUploader"] section {
        background-color: transparent !important;
    }

    /* 1. Fix the Sidebar/Main Content Conflict */
    [data-testid="stAppViewContainer"] {
        display: flex;
        flex-direction: row;
        width: 100vw;
    }

    /* 2. Target the Sidebar specifically without breaking the toggle */
    section[data-testid="stSidebar"] {
        background-color: #0e1117 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        /* Remove any 'width' or 'position' overrides here to let Streamlit handle the toggle */
    }

    /* 3. Ensure the main content doesn't "disappear" when sidebar closes */
    [data-testid="stMainViewContainer"] {
        flex: 1;
        width: 100%;
        background: transparent;
    }

    /* 4. Fix sidebar toggle text glitch */
    /* Aggressively target the button and all its children to hide text */
    button[kind="headerNoPadding"],
    button[kind="headerNoPadding"] div,
    button[kind="headerNoPadding"] span,
    button[kind="headerNoPadding"] svg {
        font-size: 0 !important;
        color: transparent !important;
        border: none !important; 
        background: transparent !important;
    }

    /* Re-add a clean, centered arrow */
    button[kind="headerNoPadding"]::after {
        content: '❯'; 
        font-size: 20px !important;
        color: rgba(255, 255, 255, 0.5) !important;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        display: block !important;
    }

    /* Ensure header is transparent */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* 5. Keep the content centered and Open Sans font */
    .block-container {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 28px;
        padding: 3rem;
        max-width: 800px;
        margin: 4rem auto; 
        font-family: 'Open Sans', sans-serif;
        backdrop-filter: blur(12px);
        box-shadow: 0 40px 100px -20px rgba(0, 0, 0, 0.8);
    }
    
    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: 600;
        height: 3.5em;
        background: #ffffff;
        color: #000000;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
        background-color: #e4e4e7;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/clouds/200/microphone.png", width=150)
        st.title("Settings")
        st.markdown("Customize your podcast experience.")
        
        voice_option = st.selectbox(
            "Select Voice",
            ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown(
            "This tool uses **GPT-4o** to summarize research papers and **OpenAI TTS** to Voicify them."
        )

    # Main Content
    st.title("🎧 Paper-to-Pod Converter")
    st.markdown("### Turn complex research papers into engaging audio podcasts in seconds.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.info("Upload a PDF to get started.")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", label_visibility="collapsed")

    if uploaded_file is not None:
        with col2:
            st.success(f"File uploaded: **{uploaded_file.name}**")
            st.metric(label="File Size", value=f"{uploaded_file.size / 1024:.2f} KB")
        
        st.markdown("---")
        
        if st.button("🚀 Generate Podcast"):
            
            # Use a nice status container
            with st.status("Processing your paper...", expanded=True) as status:
                try:
                    # Save uploaded file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name

                    # 1. Extract
                    status.write("📄 Extracting text from PDF...")
                    text = extract_text_from_pdf(tmp_path)
                    status.write(f"✅ Text extracted ({len(text)} characters).")
                    
                    # 2. Summarize
                    status.write("🧠 Generating script with GPT-4o...")
                    script = summarize_text(text)
                    status.write("✅ Script ready.")
                    
                    # 3. Audio
                    status.write(f"🎙️ Synthesizing audio (Voice: {voice_option})...")
                    output_audio_path = "podcast_output.mp3"
                    
                    generate_audio(script, output_audio_path, voice=voice_option)
                    
                    status.update(label="Conversion Complete!", state="complete", expanded=False)
                    
                    st.divider()
                    st.subheader("🎧 Your Podcast is Ready!")
                    st.audio(output_audio_path, format="audio/mp3")
                    
                    with st.expander("📝 View Podcast Script"):
                        st.markdown(script)
                        
                    # Cleanup
                    os.remove(tmp_path)

                except Exception as e:
                    status.update(label="Error", state="error")
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
