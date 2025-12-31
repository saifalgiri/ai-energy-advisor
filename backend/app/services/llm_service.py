import re
import httpx
import json
from typing import AsyncGenerator
import logging

from app.shared.shared_config import settings
from app.models.home_model import Home
from app.schemas.advice_schema import SSEMessage, MessageType, Recommendation, Priority, Category
from app.interfaces.llm_service_interface import LLMServiceInterface

# Setup logger
logger = logging.getLogger(__name__)

class LLMService(LLMServiceInterface):
    
    def create_energy_prompt(self, home: Home) -> str:
        home_age = 2025 - home.year_built
        
        prompt = f"""
You are a senior residential energy retrofit consultant.

Your task is to recommend HIGH-IMPACT energy efficiency upgrades that deliver the
LARGEST POSSIBLE annual cost savings within the given constraints.

You are explicitly allowed to recommend:
- Insulation upgrades (roof, walls, floors)
- Heating system replacement or optimization
- Window replacement if justified
- Structural or technical interventions with medium renovation effort

DO NOT recommend:
- Behavioral tips
- Low-impact tweaks (LEDs, reminders, habits)
- Measures saving less than 300 €/year

Energy prices:
- Gas: 0.12 €/kWh
- Electricity: 0.35 €/kWh

Constraints:
- Budget: up to 15,000 €
- Ownership: Owned
- Renovation tolerance: Medium
- Primary goal: Reduce heating costs and improve winter comfort

Home details:
- Size: {home.size_sqft} sq ft
- Age: {home_age} years (built {home.year_built})
- Location: {home.location}
- Heating: {home.heating_type.value}
- Insulation: {home.insulation_level.value}
- Windows: {home.windows_type.value}-pane
- Occupants: {home.num_occupants}
- Monthly_Bill: {home.monthly_energy_bill} Euro

Return ONLY valid JSON in the following structure:

{{
  "recommendations": [
    {{
      "id": "R1",
      "priority": "High",
      "details": "Technically specific retrofit action with clear scope",
      "estimate_cost": "Upfront cost range in €",
      "saving_cost": "Estimated annual savings in €/year (must be ≥ 300 €/year)"
    }}
  ]
}}

Rules:
- JSON only, no extra text
- 1-4 recommendations
- Prioritize MAXIMUM annual savings, not lowest cost
- All recommendations must meaningfully reduce heating demand
- Be realistic but bold in savings estimates
"""
        return prompt
    
    def _extract_title_from_details(self, details: str) -> str:
        sentences = details.split('.')
        title = sentences[0].strip() if sentences else details
        
        # Limit to 60 characters
        if len(title) > 60:
            title = title[:57] + "..."
        
        return title
    
    def _parse_recommendations(self, text: str) -> list[dict]:
        try:
            # Remove markdown code blocks if present
            text = re.sub(r'```json\s*', '', text)
            text = re.sub(r'```\s*', '', text)
            text = text.strip()
            
            # Parse JSON
            data = json.loads(text)
            
            if "recommendations" in data:
                return data["recommendations"]
            return []
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {e}")
            print(f"Text received: {text[:200]}")
            return []
    
    def _categorize_recommendation(self, rec: dict) -> str:
        """Auto-categorize recommendation based on content"""
        details = rec.get("details", "").lower()
        title = rec.get("title", "").lower()
        text = f"{title} {details}"
        
        # Category detection keywords
        categories = {
            "insulation": ["insulation", "insulate", "attic", "wall", "ceiling", "floor", "r-value"],
            "windows": ["window", "door", "seal", "draft", "weatherstrip", "caulk", "glazing", "pane"],
            "heating": ["heating", "furnace", "boiler", "thermostat", "heat pump", "hvac", "radiator", "temperature"],
            "appliances": ["appliance", "refrigerator", "washer", "dryer", "led", "light", "bulb", "energy star"],
            "renewable": ["solar", "renewable", "panel", "wind", "geothermal", "photovoltaic"],
            "habits": ["habit", "behavior", "schedule", "adjust", "turn off", "unplug", "routine"]
        }
        
        # Check each category
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        # Default to habits if can't categorize
        return "habits"
    
    async def generate_recommendations_stream(
        self,
        home: Home
    ) -> AsyncGenerator[str, None]:
        """Generate recommendations using Ollama with streaming"""
        prompt = self.create_energy_prompt(home)
        accumulated_text = ""
        
        try:
            async with httpx.AsyncClient(
                timeout=settings.OLLAMA_TIMEOUT
            ) as client:
                # Send connected message
                msg = SSEMessage(
                    type=MessageType.CONNECTED,
                    home_id= str(home.id)
                )
                yield f"data: {msg.model_dump_json()}\n\n"
                
                # Stream from Ollama
                async with client.stream(
                    "POST",
                    f"{settings.OLLAMA_BASE_URL}/api/generate",
                    json={
                        "model": settings.OLLAMA_MODEL,
                        "prompt": prompt,
                        "stream": True,
                        "options": {
                            "temperature": 0.7,
                            "top_p": 0.9,
                        },
                        "format": "json"  # Request JSON format
                    }
                ) as response:
                    if response.status_code != 200:
                        error_text = await response.aread()
                        msg = SSEMessage(
                            type=MessageType.ERROR,
                            error=f"Ollama error: {error_text.decode()}"
                        )
                        yield f"data: {msg.model_dump_json()}\n\n"
                        return
                    
                    # Accumulate the complete response
                    async for line in response.aiter_lines():
                        if line.strip():
                            try:
                                data = json.loads(line)
                                if "response" in data:
                                    accumulated_text += data["response"]
                                
                                if data.get("done", False):
                                    # Parse complete JSON response
                                    recommendations = self._parse_recommendations(accumulated_text)
                                    
                                    # Stream each recommendation separately
                                    for idx, rec in enumerate(recommendations, 1):
                                        # Extract or generate title from details
                                        title = rec.get("title") or self._extract_title_from_details(
                                            rec.get("details", "Energy Recommendation")
                                        )
                                        
                                        # Auto-categorize if not provided
                                        category = rec.get("category")
                                        if not category:
                                            category = self._categorize_recommendation(rec)
                                        
                                        # Map field names (LLM uses 'details', we use 'description')
                                        description = rec.get("details") or rec.get("description", "")
                                        estimated_cost = rec.get("estimate_cost") or rec.get("estimated_cost", "N/A")
                                        estimated_savings = rec.get("saving_cost") or rec.get("estimated_savings", "N/A")
                                        
                                        # Normalize priority
                                        priority = rec.get("priority", "medium").lower()
                                        if priority not in ["high", "medium", "low"]:
                                            priority = "medium"
                                        
                                        # Create recommendation object
                                        recommendation = Recommendation(
                                            id=rec.get("id", f"R{idx}"),
                                            title=title,
                                            description=description,
                                            estimated_cost=estimated_cost,
                                            estimated_savings=estimated_savings,
                                            priority=Priority(priority),
                                            category=Category(category.lower())
                                        )
                                        
                                        msg = SSEMessage(
                                            type=MessageType.RECOMMENDATION,
                                            recommendation=recommendation
                                        )
                                        yield f"data: {msg.model_dump_json()}\n\n"
                                    
                                    # Send complete message
                                    msg = SSEMessage(type=MessageType.COMPLETE)
                                    yield f"data: {msg.model_dump_json()}\n\n"
                                    break
                                    
                            except json.JSONDecodeError:
                                continue
                                
        except httpx.ConnectError:
            error_msg = "Cannot connect to Ollama. Ensure Ollama is running."
            msg = SSEMessage(type=MessageType.ERROR, error=error_msg)
            yield f"data: {msg.model_dump_json()}\n\n"
        except httpx.TimeoutException:
            error_msg = "Request to Ollama timed out. Please try again."
            msg = SSEMessage(type=MessageType.ERROR, error=error_msg)
            yield f"data: {msg.model_dump_json()}\n\n"
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            msg = SSEMessage(type=MessageType.ERROR, error=error_msg)
            yield f"data: {msg.model_dump_json()}\n\n"
