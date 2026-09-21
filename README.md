🤖 Telegram Multi-Tool Bot

A multifunctional Telegram bot built with Python and pyTelegramBotAPI, designed to provide several useful tools in one place.

✨ Features

- 🔐 Password Generator — Generate secure random passwords.
- 🔢 Average Tool — Calculate the average of numbers
- 💲 Currency Prices — Show the price of currency (like Bitcoin). This tool works in groups too.
- ⚖️ BMI Calculator — Calculate BMI based on height and weight.
- 📅 Date Difference — Calculate the difference between dates with support for Gregorian and Persian (Jalali) dates.
- 🎲 Lottery Tool — Randomly select numbers or participants.
- 🔁 Format converter — PDF to PNG, JPG to PNG, image to PDF etc.
- ▶️ Text-to-speech — Convert text to mp3 file.
- 💠 Inline keyboard button maker — Use to create a message with buttons and share it.
- 🟡 Admin panel for bot management — Normal users do not have access to the panel
- 🧰 Multi-Tool Menu — Access all available tools through an easy-to-use Telegram interface.

🔐 Required Channel Membership

The bot includes a mandatory channel membership system.

Before using the bot's features, users are required to join the specified Telegram channels. The bot automatically checks the user's membership status before allowing access to protected features.

🛠️ Built With

- 🐍 Python
- 🤖 pyTelegramBotAPI
- 🟥 Requirements



🚀 Installation

Clone the repository:

git clone https://github.com/mahan-py/Backpack.git
cd REPOSITORY

Create a virtual environment:

python -m venv venv

Activate the virtual environment.

Windows

venv\Scripts\activate

Linux / VPS

source venv/bin/activate

Install the required libraries:

pip install -r Requirements.txt

⚙️ Configuration

The bot requires a Telegram Bot Token to run.

Do not put your real Bot Token or API keys directly in the source code or commit them to GitHub.

Use environment variables or another secure configuration method instead.

Example:

import os

TOKEN = os.getenv("BOT_TOKEN")

▶️ Run

After configuring the required environment variables:

python bot.py

🔒 Security

Never commit sensitive information such as:

- Telegram Bot Tokens
- API Keys
- Passwords
- Private credentials
- User data

Use ".gitignore" and environment variables to keep sensitive files out of the repository.

📌 Project Status

This project is actively being developed and new tools and improvements may be added over time.

📄 License

This project does not currently specify a license.

---

⭐ If you find this project useful, feel free to star the repository.