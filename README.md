# 🤖 Pasquale, Your Local Grammar Checking Bot 

Tired of typos sneaking into your writing? This repository contains everything you need to run your **own**, **locally hosted**, **AI-powered** grammar, style, and spelling assistant.

No need to send your text off into the cloud—keep everything private and on your own machine. 🏡

&nbsp;

**Using Pasquale with [TeXstudio](https://github.com/texstudio-org/texstudio):**

https://github.com/user-attachments/assets/0dd077c0-dae1-434c-910e-a4f4b0e4490a

**Note:** This example required less than 1.5GB of VRAM.

---

&nbsp;

## ✨ Features ✨

* **Local-first and private:** 
  All processing happens on your machine. Using local LLMs, your text stays yours.

* **AI-powered corrections:** 
  Uses modern language models to catch grammar, spelling, and style issues beyond traditional checkers.

* **Explanations included:** 
  Suggestions come with reasoning, so you can understand and decide what to accept.

* **Lightweight by design:**
  Built to work well with small, efficient LLMs without consuming excessive resources.

* **Multi-language support (in progress):** Ongoing work to support multiple languages effectively, even with smaller models.

&nbsp;

## 📜 Prerequisites 📜

* **Python 3.7 or newer**  
  Check with `python --version` or `python3 --version`.

* **Local LLM server and model**  
  Any server compatible with the OpenAI API format will work.

* **Python dependencies**  
  - Flask  
  - OpenAI package  

&nbsp;

## 📝 Running Pasquale 📝

### 🛠️ Setup (Linux command line)

1. **Install an LLM inference server and model**

   You’ll need a local LLM backend. Popular options include:
   - ollama
   - llama.cpp
   - LM Studio

   Example for gemma3 1B using ollama:

    ```bash
    # install ollama
    curl -fsSL https://ollama.com/install.sh | sh

    # download model
    ollama pull gemma3:1b-it-qat
    ````

2. **Clone the repository**

    ```bash
    git clone https://github.com/joaopaulo7/pasquale.git
    cd pasquale
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

 

### 🙋‍♀️ Using Pasquale 

1. **Start the server**

   Either run directly with python3 command:
   ```bash
   python3 src/simple_server.py
   ```
   or use a docker container:
   ```bash
   docker build -t pasquale . && docker run --rm -p 5000:5000 pasquale
   ```

   You should see something like:
   `Running on http://127.0.0.1:5000`

   Note: The server runs over HTTP (not HTTPS), which is fine for local use.


2. **Configure credentials and inference options**

   Access `http://127.0.0.1:5000/config` (or directly edit your `config.yaml` before running) to change the default options:

   * **Credentials:**
     * **base_url:** URL to an openAI-compatible endpoint
     * **api_key:** API key for your LLM server
     * **model:** Model available on your server
   * **Inference options:**
     * **genres:** Writing style 
     * **extra_prompt:** Additional instructions for the model
     * **thinking:** enable or disable thining (disabled for faster results)
     * **temperature:** Controls randomness
     * **max_tokens:** Limits response length

3. **Connect a client**

   Pasquale is API-compatible with LanguageTool, so most editors can use it with minimal setup.

   Just replace the LanguageTool server URL with your local Pasquale URL.

   Example (TeXstudio):

   * Go to *Options > Configure TeXstudio > Language Checking*
   * Set the server URL to: `http://localhost:5000/`

   You should start seeing suggestions as you type.

 

## 🏗️ Work in Progress 🏗️

Pasquale is an early-stage, single-developer project—expect frequent changes.

Planned improvements:

* Evaluate and improve integration with other clients
* Expanded language support
* More model-specific prompting

 

---

Hopefully there aren’t any typos in this README.