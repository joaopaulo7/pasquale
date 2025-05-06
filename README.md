# 🤖 Pasquale, Your Very Own Local Grammar Teacher ✨

Tired of typos sneaking into your brilliant prose? Fear not! This repository holds the secret to running your **very own**, **locally hosted**, **AI-powered** grammar, style and spelling professor!

No more sending your precious words off into the internet ether – keep them safe and sound on your own digital turf! 🏡

&nbsp;

**Using Pasquale with [TeXstudio](https://github.com/texstudio-org/texstudio):**


https://github.com/user-attachments/assets/0dd077c0-dae1-434c-910e-a4f4b0e4490a


**Ps. this example required less than 1.5GB of VRAM to run.** 🙀🙀

---


&nbsp;


## ✨ What Are Pasquale's Awesome Features? ✨

* **Keeps Your Secrets Secret!** 🤫 All the grammar wizardry happens right on your computer. Your words are yours and yours alone!
  
* **Brainy Pants AI Inside!** 🧠 This isn't your grandma's spell checker (though we love you, Grandma!). We're talking about real, honest-to-goodness AIs that can catch those spelling ghosts and grammar ghouls.

* **Not Only *How*, But Also *Why*** 👨‍🏫 Pasquale is designed to be your teacher, not your dictator! It will provide a reason for every change it proposes. It's up to you to accept or reject.
  
* **Doesn't Hog All The ~Pastels~ Pies!** 🥧 The goal is for Pasquale to be a **mean** but *lean* grammar-checking machine that works well with tiny LLMs and won't gobble up all your resources.
  
* **Multiple Languages?** 🌎 Working on it!! Our goal is to find the best prompts for each language, so that even the smallest LLMs become great teachers.

&nbsp;

## 📜 Prerequisites 📜

* **Python 3.7 or Newer:** Check with a quick `python --version` or `python3 --version` in your terminal.
  
* **Local LLM server and model:** Any local LLM server compatible with OpenAI's API format will do just fine. Even better if they offer good quantization. 😉
  
* **Flask package:** To run the local API server. 🍾
  
* **OpenAI package:** To communicate with the LLM server. 🦙

&nbsp;
  
## 📝 How to run? 📝

Pasquale is currently still in development, so the only way to run it is directly via the source code.

### 🛠️ Setup (Linux) 🛠️

1.  **Install LLM server and download model**

    You should have a way to run the AI core locally to get the most out of Pasquale.

    This process depends on the server you wish to use.
    You may install any of the most famous LLM servers, like [ollama](https://www.ollama.com/) or [llamaccp](https://github.com/ggml-org/llama.cpp)
    and then choose and download at least one LLM model to run Pasquale's core.

    For running gemma3-1B with ollama, which we recommend the most for weaker machines, you'd do something like this:
    ```bash
    # download ollama server
    curl -fsSL https://ollama.com/install.sh | sh

    # download gemma3-1B model
    ollama pull gemma3:1b-it-qat
    ```

    
3.  **Install Prerequisites**
    
    The python prerequisites are pretty simple:
    ```bash
    pip install openai flask
    ```

4.  **Clone Repository:**

    ```bash
    git clone https://github.com/joaopaulo7/pasquale.git
    cd pasquale
    ```

   
&nbsp;

### 🙋‍♀️ Asking for Pasquale's help (starting and using the server) 🙋‍♀️

1. **Adjust configurations (optional)**
   
   If you are using the recommended LLM server and model, you're mostly good to go; however. it still might be interesting to tweak some settings.
   
   To do that, you can edit the `config.json` file directly, which should look something like this:
   ```json
   {
       "creds": {
           "base_url": "http://localhost:11434/v1/",
           "api_key": "ollama" 
       },
       "config": {
           "model": "gemma3:1b-it-qat",
           "genres": "formal; academic",
           "extra_prompt": "",
           "thinking": false,
           "temperature": 0.0,
           "max_tokens": 8000
      }
   }
   ```
   Most of the options are self-explanatory, but here are their descriptions anyway:
   - **base_url and api_key:** These are your credentials to access the LLM server. **Important: choose the server's openAI-compatible url; otherwise, it won't work.**
     
   - **model:** The model you want to use. Make sure you have it set up in the server.
     
   - **genres:** The literary genres of the texts. These are fed to the AI directly, serving as a guide on what to look out for.
     You can make them whatever you want, but widely known genres work best. Use either commas or semicolons as separators.
   
   - **extra_prompt:** An extra prompt to be provided to the AI core with every query. One clear use for this is adding a "/no_think" option to disable thinking in hybrid models.
     
   - **thinking:** Indicates the model is a thinking model and that the `<think></think>` tags should be excluded from the output.
     
   - **temperature:** The amount of ~randomness~ creativity in the AI's suggestions. 0.0 is deterministic, best for consistent results; higher values are more random, best if you want more creative suggestions.
  
   - **max_tokens:** Maximum amount of tokens in a response. May be useful if the AI core starts hallucinating.


2.  **Run server script:**

    Starting the server is pretty straightforward. Just run `server_simple.py`:
    ```bash
    python3 server_simple.py
    ```

    After running the script, you should be given the port on which the server is running, something like `Running on http://127.0.0.1:5000`. This is the url you'll be using to access the API.

    Ps. make note that the server runs on http, not https. This isn't an issue since we're only running it locally, but you should pay attention to it when typing the url.

4.  **Client-side setup:**

    As a *server*, Pasquale is designed to *serve* a client, usually a local text editor, so we need to tell these apps where to get grammar suggestions from.
    
    **By sheer dumb luck coincidence**, Pasquale is compatible with the format of the very popular LanguageTool API.
    So, for most clients, setting it up is as easy as swapping a url,  just find the LanguageTool API url in your text editor's configurations and swap the original domain to the one the server is running on.

    For example, for using it with:
    - **TeXstudio:** go to *>Options>Configure TeXstudio>Language Checking*, then, find and change the server URL field to `http://localhost:5000/`:

      ![Screenshot from 2025-05-06 13-50-57](https://github.com/user-attachments/assets/7abcc957-fe75-4238-8b85-a4404313fa8b)
     
     Pronto! You should be getting hits in the server as soon as you start typing.

&nbsp;

## 🏗️ Work in Progress 🏗️

Pasquale is a one-man operation, still a work in progress and very preliminary, so expect large and frequent changes.

Currently, the main improvements for the future are:
- Consolidate the compatibility with text editors even further;
- Explore the compatibility of different LLMs;
- Develop an easier way to set up and configure the server;
- Expand and solidify the language catalog; ~Desculpa, professor!~ 😓
- Create model-specific prompts;

&nbsp;


---

&nbsp;
&nbsp;

God, I hope there aren't any typos in this readme.
