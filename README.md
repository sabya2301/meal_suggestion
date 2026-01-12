# 🥗 Meal Suggestion Agent

> A smart, agentic AI project that plans your daily meals, remembers what you ate, and sends you the details via WhatsApp.

## 🤖 About The Project

This is a **small Agentic AI project** designed to automate daily meal planning. Unlike simple random generators, this agent maintains **state/memory** of your previous meals to ensure variety. It leverages a local Large Language Model (DeepSeek via Ollama) to generate nutritious meal plans including macros, and proactively pushes the plan to your phone.

## ✨ Key Features

- **🧠 Local Intelligence**: Uses **DeepSeek-R1:7b** running locally via Ollama for privacy and cost-free inference.
- **💾 Memory persistence**: Stores meal history in **SQLite** to prevent repetitive suggestions (looks back 3 days).
- **📱 WhatsApp Notifications**: Sends the finalized meal plan directly to your phone using **Twilio**.
- **📊 Macro Tracking**: Automatically calculates and includes generic macro-nutrient data (Protein, Carbs, Fats, Calories).
- **📝 Robust Logging**: Detailed logging system for debugging and tracking agent decisions.

## 🛠️ Tech Stack

- **Python 3.11+**
- **Ollama** (Local LLM Server)
- **Ollama Python Library / OpenAI SDK**
- **SQLite3**
- **Twilio API**

## 🚀 Getting Started

### Prerequisites

1.  **Ollama**: Install [Ollama](https://ollama.com/) and pull the model:
    ```bash
    ollama run deepseek-r1:7b
    ```
2.  **Twilio Account**: Get your SID, Auth Token, and Sandbox number from [Twilio](https://www.twilio.com/).

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/sabya2301/meal_suggestion.git
    cd meal_suggestion
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**:
    Create a `.env` file in the root directory:
    ```ini
    TWILIO_ACCOUNT_SID=your_sid_here
    TWILIO_AUTH_TOKEN=your_token_here
    TWILIO_FROM_NUMBER=whatsapp:+1234567890
    MY_PHONE_NUMBER=whatsapp:+9876543210
    ```

### ▶️ Usage

Run the agent script:

```bash
python deepseek.py
```

The agent will:
1.  Check your meal history from `meal_history.db`.
2.  Prompt DeepSeek to generate a new plan (excluding recent meals).
3.  Save the new plan to the database.
4.  Send you a WhatsApp message with the menu!

## 📂 Project Structure

```
.
├── deepseek.py       # Main agent logic (Brain)
├── db_handler.py     # Database interactions (Memory)
├── notification.py   # WhatsApp service (Tools)
├── logger.py         # Logging configuration
├── requirements.txt  # Dependencies
└── logs/             # Execution logs
```

---
*Built as an exploration into Agentic Workflows.*
