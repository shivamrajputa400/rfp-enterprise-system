import logging
from backend.agents.sales_agent import SalesAgent
from backend.agents.technical_agent import TechnicalAgent  
from backend.agents.pricing_agent import PricingAgent
from backend.services.file_processor import FileProcessor

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self):
        self.sales_agent = SalesAgent()
        self.technical_agent = TechnicalAgent()
        self.pricing_agent = PricingAgent()
        self.file_processor = FileProcessor()
    
    async def process_rfp(self, file_path: str) -> dict:
        try:
            text_content = await self.file_processor.extract_text(file_path)
            
            extracted_data = await self.sales_agent.extract_rfp_data(text_content)
            
            matched_items = []
            for item in extracted_data['items']:
                matches = await self.technical_agent.find_product_matches(
                    item['item_name'], item['specifications']
                )
                if matches:
                    best_match = matches[0]
                    matched_items.append({
                        **item,
                        "matched_product": best_match['product'],
                        "match_score": best_match['match_score'],
                        "reasoning": best_match['reasoning']
                    })
            
            quotation = await self.pricing_agent.generate_quotation(
                extracted_data['company_info'], matched_items
            )
            
            return {
                "status": "success",
                "extracted_data": extracted_data,
                "quotation": quotation
            }
            
        except Exception as e:
            logger.error(f"Processing failed: {e}")
            return {"status": "error", "message": str(e)}
