import json
import re
from openai import OpenAI
import db_handler
from notification import WhatsAppSender
from logger import setup_logger

# Initialize Logger
logger = setup_logger("deepseek_agent")

OLLAMA_BASE_URL = "http://localhost:11434/v1"

# Initialize Client
ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key='ollama')

# 1. Get History
logger.info("Fetching recent meal interactions...")
recent_meals = db_handler.get_recent_meals(days=3)
history_text = ""
if recent_meals:
    history_text = "Here is what the user ate in the last 3 days (Avoid repeating these):\n"
    for meal in recent_meals:
        history_text += f"- {meal['date']} ({meal['meal_type']}): {meal['content']}\n"
else:
    history_text = "No recent meal history."

# 2. Define Prompts
system_prompt = f"""You are a helpful assistant who helps the user plan their meals. 
{history_text}
Provide a meal plan for today including Breakfast, Lunch, Dinner, and strictly optional Snacks.
You MUST output the response in valid JSON format with the below structure. Make sure that this is the only thing you output, there should not be any other text in your response other than the JSON structure below.:
{{
    "meals": [
        {{
            "meal_type": "Breakfast",
            "content": "Description of the meal",
            "macros": "Calories: Xkcal, Carbs: Xg, Protein: Yg, Fats: Zg"
        }},
        ...
    ]
}}
Do not add any markdown formatting or text outside the JSON."""

user_prompt = "Give me a meal suggestion for today."

# 3. Call LLM
logger.info("Querying DeepSeek model...")
try:
    response = ollama.chat.completions.create(
        model="deepseek-r1:7b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )

    content = response.choices[0].message.content
    logger.info("Received response from DeepSeek.")
    logger.debug(f"Raw Response: {content}")

    # 4. Parse and Save
    # Remove <think> blocks (DeepSeek R1 specific)
    clean_content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
    
    # Remove markdown code blocks
    clean_content = clean_content.replace("```json", "").replace("```", "").strip()
    
    logger.debug(f"Cleaned JSON content: {clean_content}")

    data = json.loads(clean_content)
    
    logger.info("Parsing successful. Saving to database...")
    
    # Initialize message for WhatsApp
    whatsapp_message = "🍽️ *Today's Meal Plan* 🍽️\n\n"
    
    for meal in data.get("meals", []):
        logger.info(f"Processing meal: {meal['meal_type']}")
        
        # Get data with defaults to avoid errors
        meal_type = meal.get('meal_type', 'Unknown Type')
        content = meal.get('content', 'No description provided')
        macros = meal.get('macros', 'NA')
        
        # Add to DB
        db_handler.add_meal(
            meal_type=meal_type,
            content=content,
            macros=macros
        )
        logger.info(f"Saved: {meal_type}")
        
        # Append to WhatsApp message
        whatsapp_message += f"*Meal Type:* {meal_type}\n"
        whatsapp_message += f"*Meal:* {content}\n"
        whatsapp_message += f"*Macros:* {macros}\n\n"
    
    # Send WhatsApp Notification
    logger.info("Sending WhatsApp notification...")
    sender = WhatsAppSender()
    sender.send_message(whatsapp_message)
    
except json.JSONDecodeError as e:
    logger.exception("Failed to parse JSON response.")
    logger.error(f"Content that failed: {content}")
except Exception as e:
    logger.exception("An unexpected error occurred")