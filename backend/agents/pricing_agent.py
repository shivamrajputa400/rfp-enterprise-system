import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class PricingAgent:
    def __init__(self):
        self.tax_rate = 0.18
        self.transport_rate = 0.15
        self.testing_charge = 0.02
    
    async def generate_quotation(self, company_info: Dict, matched_items: List[Dict]) -> Dict[str, Any]:
        try:
            line_items = []
            subtotal = 0
            
            for item in matched_items:
                if item.get('matched_product'):
                    product = item['matched_product']
                    quantity = item.get('quantity', 1)
                    
                    base_cost = product['unit_price'] * quantity
                    testing_charges = base_cost * self.testing_charge
                    transport_cost = self.transport_rate * 100 * quantity
                    
                    line_total = base_cost + testing_charges + transport_cost
                    subtotal += line_total
                    
                    line_items.append({
                        "product_id": product['product_id'],
                        "product_name": product['name'],
                        "quantity": quantity,
                        "unit": product['unit'],
                        "unit_price": product['unit_price'],
                        "base_cost": round(base_cost, 2),
                        "testing_charges": round(testing_charges, 2),
                        "transport_cost": round(transport_cost, 2),
                        "line_total": round(line_total, 2),
                        "match_score": item.get('match_score', 0)
                    })
            
            discount = self._calculate_discount(subtotal, len(line_items))
            taxable_amount = subtotal - discount
            tax_amount = taxable_amount * self.tax_rate
            final_amount = taxable_amount + tax_amount
            
            quotation = {
                "quotation_id": f"QT{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "company_info": company_info,
                "line_items": line_items,
                "pricing_summary": {
                    "subtotal": round(subtotal, 2),
                    "discount_amount": round(discount, 2),
                    "taxable_amount": round(taxable_amount, 2),
                    "tax_rate": self.tax_rate * 100,
                    "tax_amount": round(tax_amount, 2),
                    "final_amount": round(final_amount, 2)
                },
                "validity": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                "terms_conditions": [
                    "Prices valid for 30 days",
                    "Delivery: 4-6 weeks from order confirmation",
                    "Payment: 50% advance, 50% before delivery",
                    "Warranty: 1 year from commissioning date",
                    "Taxes extra as applicable"
                ]
            }
            
            return quotation
            
        except Exception as e:
            logger.error(f"Pricing error: {e}")
            raise
    
    def _calculate_discount(self, subtotal: float, item_count: int) -> float:
        if subtotal > 100000: return subtotal * 0.10
        if subtotal > 50000: return subtotal * 0.07
        if item_count > 5: return subtotal * 0.05
        return 0.0
