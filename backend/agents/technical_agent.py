import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class TechnicalAgent:
    def __init__(self):
        self.product_database = self._load_product_database()
    
    def _load_product_database(self) -> Dict[str, Any]:
        return {
            "cables": [
                {
                    "product_id": "CABLE-XLPE-1.5",
                    "name": "XLPE Insulated Copper Cable 1.5 sqmm",
                    "category": "Cables",
                    "specifications": {"voltage": "1100V", "current": "20A", "material": "Copper"},
                    "unit_price": 45.50,
                    "unit": "meter"
                },
                {
                    "product_id": "CABLE-PVC-2.5", 
                    "name": "PVC Insulated Copper Cable 2.5 sqmm",
                    "category": "Cables",
                    "specifications": {"voltage": "1100V", "current": "27A", "material": "Copper"},
                    "unit_price": 68.75,
                    "unit": "meter"
                }
            ],
            "transformers": [
                {
                    "product_id": "TRANSFORMER-11KV-500",
                    "name": "11KV/433V Distribution Transformer 500KVA",
                    "category": "Transformers", 
                    "specifications": {"primary": "11KV", "secondary": "433V", "capacity": "500KVA"},
                    "unit_price": 450000.00,
                    "unit": "unit"
                }
            ],
            "lighting": [
                {
                    "product_id": "LED-STREET-50W",
                    "name": "LED Street Light 50W",
                    "category": "Lighting",
                    "specifications": {"power": "50W", "lumen": "6000lm", "ip_rating": "IP65"},
                    "unit_price": 3200.00,
                    "unit": "unit"
                }
            ]
        }
    
    async def find_product_matches(self, item_description: str, specifications: str) -> List[Dict[str, Any]]:
        matches = []
        
        for category, products in self.product_database.items():
            for product in products:
                score = self._calculate_match_score(item_description, specifications, product)
                if score > 60:
                    matches.append({
                        "product": product,
                        "match_score": score,
                        "reasoning": self._generate_reasoning(score),
                        "compatibility_notes": self._check_compatibility(specifications, product)
                    })
        
        return sorted(matches, key=lambda x: x['match_score'], reverse=True)[:3]
    
    def _calculate_match_score(self, description: str, specs: str, product: Dict) -> float:
        score = 0
        description_lower = description.lower()
        product_name_lower = product['name'].lower()
        
        if any(word in product_name_lower for word in description_lower.split()):
            score += 40
        
        spec_matches = sum(1 for spec in product['specifications'].values() 
                          if str(spec).lower() in specs.lower())
        score += spec_matches * 20
        
        return min(score, 100)
    
    def _generate_reasoning(self, score: float) -> str:
        if score >= 80: return "Excellent technical match"
        if score >= 60: return "Good technical compatibility" 
        return "Partial match - manual review recommended"
    
    def _check_compatibility(self, requirements: str, product: Dict) -> List[str]:
        notes = []
        req_lower = requirements.lower()
        
        if "voltage" in req_lower and "voltage" in product['specifications']:
            notes.append(f"Voltage: {product['specifications']['voltage']}")
        
        if "current" in req_lower and "current" in product['specifications']:
            notes.append(f"Current: {product['specifications']['current']}")
            
        return notes
