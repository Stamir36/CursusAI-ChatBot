# CursusBot - AI chat script

Chatbot based on Python and Transformers 🤗, with support for working in the terminal and on the Cursus Messenger website.

![CursusBot Banner](https://i.ibb.co/Ny8P19X/cursusbot-ai.png)
> Supports Russian and English.

# Features

- Carry on a light dialogue 💬.
- Translate text from Russian into English and vice versa.
- Generate images from image description using "Openjourney" 🖼️.

## Launch with Google Colab.
To run a project based on Google computers, go to [Official notepad](https://colab.research.google.com/drive/1BnPDnLK52OPSOVL3TyE7S-_zqI2Nakx-?usp=sharing), and run each code in turn. After that, return to CursusBot in the Cursus messenger and start chatting. To execute commands, enter "/" in the text box.

## What for and why?
Anyone who is interested in artificial intelligence and wants to try different models, you are in the right place. This repository has a script for launching a neural model in two modes: in the console and in Cursus Messenger.

>Those who want to try to communicate with the model without installing and running scripts, you can go to https://unesell.com/app/cursus/ and chat with the neural network.

## Guides

Check out the following resources to help you get started with neural chatbots:

- [Cursus Messenger](https://unesell.com/app/cursus/) - Try Chatbot Online (If the script is currently running on at least one computer)
- [Unesell API](https://api.unesell.com/#aimodels) - Instructions for running the script on the local computer.
- [Hugging Face](https://huggingface.co/) - Here you can find any other model to run.

## Installation on a local machine

Visit the [Unesell API](https://api.unesell.com/#aimodels) page for details.

Download the model launch script

```sh
wget https://api.unesell.com/AI/run.py
wget https://api.unesell.com/AI/run.1B.py
```
>The first script with 400M model, the second one with 1B. Choose the one that your local machine can pull.

Install dependencies and run the script

```sh
python -m pip install torch transformers requests langdetect
```
To run in [browser interface](https://unesell.com/app/cursus/)
```sh
python run.py online 
```
To run in terminal
```sh
python run.py local
```

## Image generation
After running the script on Colab or the server, you need to go to the chat of the bot, and run the following command, entering prompts or a description of what you want to receive:
```sh
/imageline {prompt}
```

## Screenshot of online mode
![CursusBot Banner](https://i.ibb.co/LPQQnVw/bot-ai.png)

# License and Author
The source code of the program is open, distribution and modification is allowed only with the consent of the author.<br>
Author: Stanislav Miroshnichenko (from Ukraine with ❤️) <br>
Feedback: s.miroshnichenko.mail@gmail.com<br>