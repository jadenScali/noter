# Noter

**Noter** turns lecture audio into detailed summary sheets.

## Features

- **Transcribe lectures**: Whether it's a live recording or prerecorded, **Noter** can transcribe it into a .txt file.
- **Summarize lectures**: **Noter** uses GPT-4o to create (.md) files with summaries, definitions, and step-by-step examples covered in a lecture. Summary sheets can be created from all modern video or audio formats or a transcript (.txt) file.
- **Playback lectures**: Relisten to lectures with the (.mp3) files automatically sorted by class code and date.

## Installation
### macOS (M1 or later)

### Prerequisites 📋
- **`Git`**
- **Python 3.10 (`miniconda` reconmended)**
- **`ffmpeg`**

If you don't already have these installed here's how you can do so!

1. Install `Homebrew`
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```

2. Install `Git`
     ```bash
     brew install git
     ```
     
3. Install `miniconda` (strongly reconmended to avoid python version conflicts)

   Download `miniconda`
     ```bash
     mkdir -p ~/miniconda3
     curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o ~/miniconda3/miniconda.sh
     bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
     rm -rf ~/miniconda3/miniconda.sh
     ```

   Initialize `miniconda`
     ```bash
     ~/miniconda3/bin/conda init zsh
     ```

4. Install `ffmpeg`
     ```bash
     brew install ffmpeg
     ```
  
### Setting up this repo 😇

1. **Clone the Repository**:

    Clone in the directory you want this project in!
    ```bash
    git clone https://github.com/jadenScali/noter.git
    ```

    Move into this project
    ```bash
    cd noter
    ```
    
2. **Create and activate a conda Environment (Optional) (Reconmended)**:

   Python 3.10 is required for this project. You may install it manually but it may cause python versioning conflicts. We strongly reconmend you use `miniconda`.
    ```bash
    conda create -n noter python=3.10
    conda activate noter
    ```

3. **Create Whisper (speech to text) model locally**:

   Install requirements and make model
    ```bash
    pip install -r requirements.txt
    git clone https://github.com/ggerganov/whisper.cpp.git
    cd whisper.cpp
    make medium.en
    ```

   Install coreML support for faster runtimes on M-series chips
   
   To ensure `coremltools` operates correctly, please confirm that [Xcode](https://developer.apple.com/xcode/) is installed and execute `xcode-select --install` to install the command-line tools.
     ```bash
     ./models/generate-coreml-model.sh medium.en
     make clean
     WHISPER_COREML=1 make -j
     ```

   Cleanup folders
     ```bash
     cd ..
     mkdir -p whisper/models
     mv whisper.cpp/main whisper/
     mv whisper.cpp/models/coreml-encoder-medium.en.mlpackage whisper/models
     mv whisper.cpp/models/ggml-medium.en-encoder.mlmodelc whisper/models
     mv whisper.cpp/models/ggml-medium.en whisper/models
     rm -rf whisper.cpp
     ```

4. **Setup AI features using OpenAI**

   Create an openAI account and follow these [instructions](https://help.openai.com/en/articles/8867743-assign-api-key-permissions) to generate an API key

   Create a `.env` file in the root of the project directory:
     ```bash
     touch .env
     ```
   Open the `.env` file in a text editor and add your OpenAI API key:
     ```env
     OPENAI_API_KEY="your_openai_api_key_here"
     ```