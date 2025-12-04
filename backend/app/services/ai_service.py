import google.generativeai as genai
import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.calorieninjas_api_key = os.getenv("CALORIENINJAS_API_KEY")
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    async def predict_nutrition(self, query: str):
        if not self.calorieninjas_api_key:
            raise Exception("CALORIENINJAS_API_KEY not found in .env file")

        api_url = 'https://api.calorieninjas.com/v1/nutrition?query=' + query
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers={'X-Api-Key': self.calorieninjas_api_key})
        
        if response.status_code != 200:
            raise Exception(f"Error from CalorieNinjas API: {response.status_code} - {response.text}")

        data = response.json()
        items = data.get('items', [])
        
        if not items:
            raise Exception("No food items found for this query")

        # Aggregate values if multiple items are returned
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fats = 0
        serving_size_parts = []
        food_names = []

        for item in items:
            total_calories += item.get('calories', 0)
            total_protein += item.get('protein_g', 0)
            total_carbs += item.get('carbohydrates_total_g', 0)
            total_fats += item.get('fat_total_g', 0)
            serving_size_parts.append(f"{item.get('serving_size_g', 0)}g")
            food_names.append(item.get('name', ''))

        return {
            "food_name": ", ".join(food_names),
            "calories": round(total_calories, 1),
            "protein": round(total_protein, 1),
            "carbs": round(total_carbs, 1),
            "fats": round(total_fats, 1),
            "serving_size": ", ".join(serving_size_parts)
        }

    async def predict_workout(self, activity: str, duration: int):
        # Local MET calculation
        # Formula: Calories = MET * Weight(kg) * Duration(hours)
        # Default weight: 70kg
        
        met_values = {
            "running": 9.8,
            "jogging": 7.0,
            "cycling": 7.5,
            "biking": 7.5,
            "swimming": 8.0,
            "walking": 3.8,
            "strength": 5.0,
            "lifting": 5.0,
            "gym": 5.0,
            "yoga": 2.5,
            "pilates": 3.0,
            "hiit": 8.0,
            "cardio": 7.0,
            "basketball": 6.5,
            "soccer": 7.0,
            "tennis": 7.0,
            "hiking": 6.0,
            "dancing": 5.0
        }
        
        activity_lower = activity.lower()
        met = 5.0 # Default to moderate activity if not found
        
        # Simple keyword matching
        for key, value in met_values.items():
            if key in activity_lower:
                met = value
                break
                
        weight_kg = 70
        duration_hours = duration / 60.0
        calories = met * weight_kg * duration_hours
        
        return {"calories_burned": round(calories)}

ai_service = AIService()
