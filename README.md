# 🤖 Pasquale, Your Very Own Local Grammar Teacher ✨

Tired of typos sneaking into your brilliant prose? Fear not! This repository holds the secret to running your **very own**, **locally hosted**, **AI-powered** grammar, style and spelling professor! No more sending your precious words off into the internet ether – keep them safe and sound on your own digital turf! 🏡

&nbsp;

**Using Pasquale in [TexStudio](https://github.com/texstudio-org/texstudio):**


https://github.com/user-attachments/assets/0dd077c0-dae1-434c-910e-a4f4b0e4490a


**Less than 2GB of VRAM usage, running with gemma3-1B-it-qat.** 🙀🙀

---


&nbsp;


## ✨ What Are Pasquale's Awesome Features? ✨

* **Keeps Your Secrets Secret!** 🤫 All the grammar wizardry happens right here on your computer. Your words are yours and yours alone!
  
* **Brainy Pants AI Inside!** 🧠 This isn't your grandma's spell checker (though we love you, Grandma!). We're talking about a real, honest-to-goodness AI that can catch those tricky spelling ghosts and grammar ghouls.
  
* **Doesn't Hog All the ~pastels~ pies!** 🥧 We're aiming for this to be a **lean**, **mean**, grammar-checking machine that works well with tiny LLMs and that won't gobble up all your computer's resources.
  
* **Multiple languages?** 🌎 Totally possible!!... Is it viable? Depends on the LLM used . ~Desculpa, professor!~ 😓

&nbsp;

## 📜 Prerequisites 📜

* **Python 3.7 or Newer:** Check with a quick `python --version` or `python3 --version` in your terminal.
  
* **Local LLM server and model:** Any local LLM server compatible with OpenAI's API format will do just fine. Even better if they offer good quantization. 😉
  
* **Flask package:** To run the local API server. 🍾
  
* **OpenAI package:** To communicate with the LLM server. 🦙

&nbsp;
  
## 🛠️ How to run? 🛠️

Pasquale is still in development, so only way to run is directly via the python command.

1.  **Install LLM server**

    You should have a way to run the LLMs locally to get the best of Pasquale.
    You can download any of most the famous LLM servers, like [ollama](https://www.ollama.com/) or [llamaccp](https://github.com/ggml-org/llama.cpp).
    
    
3.  **Install Prerequisites**
    ```bash
    pip install openai flask
    cd [your-repository-name]
    ```

4.  **Clone Repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)[your-username]/[your-repository-name].git
    cd [your-repository-name]
    ```

    
&nbsp;
&nbsp;


God, I hope there aren't any typos in this readme.


## WORK IN PROGRESS

Oops. I ran out of time!

I'll finish later.

xoxo,

Jão

<!---
### 🧙‍♂️ Summoning the Server (Running the Server) 🧙‍♀️

1.  **Unleash the AI Brain (Download the Model - If Needed):**
    * *(Heads up! If the AI's brain is already chilling in the repository, you can skip this step! 🎉)*
    * Depending on the specific AI we're using, you might need to go on a mini treasure hunt to download its brain files. Fear not! A special `MODEL_SETUP.md` scroll or some instructions within the code will guide your quest. Place the brain in its designated chamber (maybe a folder called `models/`).

2.  **Chant the Startup Spell:**
    ```bash
    python main.py
    ```
    *(If your main server file has a different name, use that instead of `main.py`!)*

3.  **Behold! The Server Awakens!** ✨
    Your terminal should now be glowing with signs that the server has sprung to life and is listening for your commands (usually at `http://localhost:5000`).

## 💬 Talking to Your Grammar Buddy (Using the API) 🗣️

Once the server is up and grooving, you can send it messages to check your text! Think of it like sending a note to your super-smart friend.

### 📬 The Secret Address (Endpoint) 📬

`/check`

### ✉️ How to Send the Message (HTTP Method) ✉️

`POST` (Like sending a letter!)

### 📜 What to Write in Your Message (Request Body - JSON) 📜

```json
{
  "text": "Eye wnt too chek gramar."
}

--->
