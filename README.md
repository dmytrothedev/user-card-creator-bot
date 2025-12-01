# Telegram Profile Card Bot

A Telegram bot that creates a personal profile card through a step-by-step conversation.  
The bot asks for the user's name, age, city and short bio, then generates a complete profile card with an option to confirm or edit the details.

---

## ✨ Features

- Step-by-step conversation flow (FSM-style logic)
- Inline buttons for user interaction
- Preview of the final profile card
- Ability to edit information before confirmation
- Simple and beginner-friendly structure (single-file project)

---

## 🧱 Tech stack

- Python 3.x  
- [python-telegram-bot 20.x](https://docs.python-telegram-bot.org/)  

---

## 🚀 How to run locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/telegram-profile-card-bot.git
   cd telegram-profile-card-bot
   
## Install dependencies

    
    pip install -r requirements.txt

## Configure the bot. Create a new file config.py in the project folder using config_example.py as a template:

    
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    
## Run
    
    python main.py

## Project structure

main.py             - the bot entry point and full logic

config_example.py   - configuration template (copy to config.py locally)

requirements.txt    - dependencies

.gitignore          - ignored files

README.md           - documentation


## 🔧 Customization ideas
This bot can be easily adapted for other purposes.
Possible modifications:

- Add more questions or fields

- Store user data in a database

- Send the profile card to an administrator

- Export user data to Google Sheets

- Use the collected profile as an onboarding form


## 💼 Suitable for

Personal introductions

Communities & clubs

Onboarding for closed groups / teams

Surveys and questionnaires

Profile generation for events or meetups


## ⭐ About the project

This bot was built as a lightweight example of Telegram onboarding using step-by-step form logic.
Feel free to fork the repository and modify it for your own use-case.


















