# Paper-to-Pod Converter 🎙️📄

Convert research papers (PDF) into engaging audio podcasts using AI.

## Overview

This tool takes a PDF file (e.g., a research paper from arXiv), extracts the text, generates a concise 2-minute podcast script using **OpenAI GPT-4o**, and converts it into lifelike audio using **OpenAI TTS**.

It features a **Cinematic Dark UI** for a premium user experience.

## Features

-   **PDF Text Extraction**: Fast and accurate extraction using `pymupdf`.
-   **AI Summarization**: Transform technical academic text into a conversational podcast script.
-   **Text-to-Speech**: High-quality audio generation with selectable voices (Alloy, Echo, Nova, etc.).
-   **Modern Web UI**: Built with Streamlit, featuring a glassmorphism design and "Cinematic Dark" theme.
-   **CLI Support**: Run conversions directly from your terminal.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/dannymairena01/paper-to-pod.git
    cd paper-to-pod
    ```

2.  Create a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Set up your OpenAI API key:
    -   Create a `.env` file in the root directory.
    -   Add your key: `OPENAI_API_KEY=sk-your-key-here`

## Usage

### Web Interface (Recommended)

Run the interactive web app:

```bash
streamlit run app.py
```

-   Upload your PDF.
-   Select a voice from the sidebar.
-   Click **Generate Podcast**.

### Command Line

Run the converter on any PDF file:

```bash
python main.py path/to/paper.pdf --output-audio my_podcast.mp3
```

## Tech Stack

-   **Python 3.11+**
-   **Streamlit** (Web UI)
-   **OpenAI API** (GPT-4o & TTS-1)

## Deployment

The easiest way to deploy this app is with **Streamlit Community Cloud**:

1.  Push your code to GitHub.
2.  Go to [share.streamlit.io](https://share.streamlit.io/).
3.  Click **New app** and select your repository (`paper-to-pod`).
4.  Set the **Main file path** to `app.py`.
5.  **Important:** Go to **Advanced settings** -> **Secrets** and add your API key:
    ```toml
    OPENAI_API_KEY = "sk-..."
    ```
6.  Click **Deploy**! 🚀
