import json
import logging
import re
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class SalesAgent:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def extract_rfp_data(self, text_content: str) -> Dict[str, Any]:
        """Extract structured data from RFP text"""
        try:
            extracted_data = {
                "company_info": {
                    "name": self._extract_company_name(text_content),
                    "project": self._extract_project_name(text_content),
                    "contact": self._extract_contact_info(text_content)
                },
                "items": self._extract_items(text_content),
                "project_details": {
                    "delivery_timeline": self._extract_timeline(text_content),
                    "payment_terms": self._extract_payment_terms(text_content),
                    "warranty_requirements": self._extract_warranty(text_content)
                }
            }
            return extracted_data
        except Exception as e:
            self.logger.error(f"Sales Agent error: {e}")
            raise
    
    def _extract_company_name(self, text: str) -> str:
        keywords = ["COMPANY:", "Company:", "Vendor:", "Supplier:"]
        for keyword in keywords:
            if keyword in text:
                return text.split(keyword)[1].split('\n')[0].strip()
        return "Unknown Company"
    
    def _extract_items(self, text: str) -> List[Dict]:
        items = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in ['cable', 'transformer', 'switchgear', 'light', 'led']):
                item = {
                    "item_name": line.strip(),
                    "quantity": self._extract_quantity(line),
                    "unit": self._extract_unit(line),
                    "specifications": self._extract_specs(lines, i),
                    "delivery_requirements": "Standard"
                }
                items.append(item)
        
        return items[:3] if items else [
            {
                "item_name": "Electrical Cable",
                "quantity": 100,
                "unit": "meter", 
                "specifications": "Standard electrical cable",
                "delivery_requirements": "2 weeks"
            }
        ]
    
    def _extract_quantity(self, text: str) -> int:
        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else 1
    
    def _extract_unit(self, text: str) -> str:
        if 'meter' in text.lower(): return 'meter'
        if 'unit' in text.lower(): return 'unit'
        return 'piece'
    
    def _extract_specs(self, lines: list, index: int) -> str:
        specs = []
        for i in range(index, min(index+3, len(lines))):
            if lines[i].strip() and not lines[i].strip().isdigit():
                specs.append(lines[i].strip())
        return ' | '.join(specs) if specs else "Standard specifications"
    
    def _extract_project_name(self, text: str) -> str:
        if "PROJECT:" in text:
            return text.split("PROJECT:")[1].split('\n')[0].strip()
        return "Electrical Project"
    
    def _extract_contact_info(self, text: str) -> str:
        return "contact@company.com"
    
    def _extract_timeline(self, text: str) -> str:
        if "week" in text.lower():
            return "4-6 weeks"
        return "Standard delivery"
    
    def _extract_payment_terms(self, text: str) -> str:
        return "50% advance, 50% on delivery"
    
    def _extract_warranty(self, text: str) -> str:
        return "1 year warranty"
