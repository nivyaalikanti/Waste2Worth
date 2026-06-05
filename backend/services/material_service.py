import pandas as pd
import re
import logging
from config import Config
from utils.helpers import extract_numeric_from_range

logger = logging.getLogger(__name__)

class MaterialService:
    """Handles material recovery and recycling calculations"""
    
    def __init__(self, excel_loader):
        self.excel_loader = excel_loader
        self.dataframes = excel_loader.get_all_dataframes()
    
    def get_multiplier_from_table(self, value, table_key, default=1.0):
        """
        Get multiplier from lookup table
        
        Args:
            value: The value to look up
            table_key: Key for the dataframe in excel_loader
            default: Default multiplier if no match found
        
        Returns:
            float: The multiplier value
        """
        try:
            df = self.dataframes.get(table_key)
            if df is None or df.empty:
                logger.warning(f"Table {table_key} is empty, using default {default}")
                return default
            
            value_col = df.columns[0]
            multiplier_col = df.columns[1]
            
            # Convert value to float if possible
            if isinstance(value, str):
                try:
                    value = float(value)
                except:
                    pass
            
            # Clean dataframe
            df_clean = df.copy()
            df_clean[multiplier_col] = pd.to_numeric(df_clean[multiplier_col], errors='coerce')
            df_clean = df_clean.dropna(subset=[multiplier_col])
            
            if df_clean.empty:
                return default
            
            # Find matching row
            for idx, row in df_clean.iterrows():
                range_value = str(row[value_col]).lower().strip()
                multiplier = float(row[multiplier_col])
                numeric_value = extract_numeric_from_range(range_value)
                
                if numeric_value is None:
                    continue
                
                if isinstance(value, (int, float)):
                    # Handle different range types
                    if '–' in range_value or '-' in range_value:
                        numbers = re.findall(r'(\d+(?:\.\d+)?)', range_value)
                        if len(numbers) >= 2:
                            lower = float(numbers[0])
                            upper = float(numbers[1])
                            if lower <= value <= upper:
                                logger.info(f"Range match: {value} in {range_value} -> {multiplier}")
                                return multiplier
                    elif '<' in range_value and value <= numeric_value:
                        logger.info(f"Less than match: {value} <= {numeric_value} -> {multiplier}")
                        return multiplier
                    elif '>' in range_value and value >= numeric_value:
                        logger.info(f"Greater than match: {value} >= {numeric_value} -> {multiplier}")
                        return multiplier
                    elif abs(value - numeric_value) < 0.1:
                        logger.info(f"Exact match: {value} = {numeric_value} -> {multiplier}")
                        return multiplier
            
            # Fallback: find closest match
            numeric_values = []
            multipliers = []
            for idx, row in df_clean.iterrows():
                range_value = str(row[value_col]).lower().strip()
                numeric_val = extract_numeric_from_range(range_value)
                if numeric_val is not None:
                    numeric_values.append(numeric_val)
                    multipliers.append(float(row[multiplier_col]))
            
            if numeric_values and isinstance(value, (int, float)):
                closest_idx = min(range(len(numeric_values)), 
                                key=lambda i: abs(numeric_values[i] - value))
                logger.warning(f"No exact match for {value}, using closest: {multipliers[closest_idx]}")
                return multipliers[closest_idx]
            
            return default
            
        except Exception as e:
            logger.error(f"Error getting multiplier: {str(e)}")
            return default
    
    def get_metal_prices(self):
        """Extract metal prices from price sheet"""
        try:
            price_df = self.dataframes.get('price')
            if price_df is None or price_df.empty:
                return Config.DEFAULT_METAL_PRICES
            
            prices = {}
            for idx, row in price_df.iterrows():
                metal_name = str(row[price_df.columns[0]]).lower().strip()
                if pd.isna(metal_name) or metal_name == 'nan' or len(metal_name) < 2:
                    continue
                
                price_col = price_df.columns[1]
                if pd.isna(row[price_col]):
                    continue
                
                price_str = str(row[price_col]).replace(',', '').strip()
                price_match = re.search(r'(\d+(?:\.\d+)?)', price_str)
                if price_match:
                    price = float(price_match.group(1))
                    prices[metal_name] = price
            
            logger.info(f"Loaded metal prices: {prices}")
            return prices if prices else Config.DEFAULT_METAL_PRICES
            
        except Exception as e:
            logger.error(f"Error extracting metal prices: {str(e)}")
            return Config.DEFAULT_METAL_PRICES
    
    def get_brand_material_content(self, brand):
        """Get base material content for a brand"""
        try:
            brand_df = self.dataframes.get('brand')
            if brand_df is None or brand_df.empty:
                return Config.DEFAULT_MATERIAL_CONTENT
            
            brand_match = brand_df[
                brand_df[brand_df.columns[0]].astype(str).str.lower() == brand.lower()
            ]
            
            if brand_match.empty:
                logger.warning(f"Brand '{brand}' not found, using defaults")
                return Config.DEFAULT_MATERIAL_CONTENT
            
            row = brand_match.iloc[0]
            return {
                "gold": float(row[brand_df.columns[1]]),
                "silver": float(row[brand_df.columns[2]]),
                "copper": float(row[brand_df.columns[3]]),
                "lithium": float(row[brand_df.columns[4]])
            }
            
        except Exception as e:
            logger.error(f"Error getting brand material: {str(e)}")
            return Config.DEFAULT_MATERIAL_CONTENT
    
    def calculate_material_recovery(self, brand, storage, ram, battery, weight, age, condition):
        """Calculate material recovery quantities"""
        try:
            # Get base materials
            base_materials = self.get_brand_material_content(brand)
            
            # Get multipliers
            multipliers = {
                'storage': self.get_multiplier_from_table(storage, 'storage', 1.0),
                'ram': self.get_multiplier_from_table(ram, 'ram', 1.0),
                'battery': self.get_multiplier_from_table(battery, 'battery', 1.0),
                'weight': self.get_multiplier_from_table(weight, 'weight', 1.0),
                'age': self.get_multiplier_from_table(age, 'age', 0.5),
                'condition': self.get_condition_multiplier(condition)
            }
            
            logger.info(f"Multipliers: {multipliers}")
            
            # Calculate material quantities
            gold = base_materials["gold"] * multipliers['storage'] * multipliers['ram'] * multipliers['age'] * multipliers['condition']
            silver = base_materials["silver"] * multipliers['storage'] * multipliers['ram'] * multipliers['age'] * multipliers['condition']
            copper = base_materials["copper"] * multipliers['weight'] * multipliers['age'] * multipliers['condition']
            lithium = base_materials["lithium"] * multipliers['battery'] * multipliers['age'] * multipliers['condition']
            
            # Calculate value
            metal_prices = self.get_metal_prices()
            recycling_value = (
                (gold * metal_prices.get("gold", 5000)) +
                (silver * metal_prices.get("silver", 70)) +
                (copper * metal_prices.get("copper", 0.7)) +
                (lithium * metal_prices.get("lithium", 35))
            )
            
            recycling_value = round(recycling_value, 2)
            
            # Log calculation details
            logger.info(f"=== RECYCLING CALCULATION ===")
            logger.info(f"Base: Au={base_materials['gold']}g, Ag={base_materials['silver']}g, Cu={base_materials['copper']}g, Li={base_materials['lithium']}g")
            logger.info(f"Adjusted: Au={gold:.6f}g, Ag={silver:.6f}g, Cu={copper:.6f}g, Li={lithium:.6f}g")
            logger.info(f"Recycling Value: ₹{recycling_value}")
            
            # Environmental impact
            co2_saved = round(weight * Config.CO2_PER_KG, 4)
            landfill_waste_prevented = round(weight / 1000, 2)
            total_material_recovered = round(gold + silver + copper + lithium, 6)
            
            return {
                "gold": round(gold, 6),
                "silver": round(silver, 6),
                "copper": round(copper, 6),
                "lithium": round(lithium, 6),
                "recycling_value": recycling_value,
                "co2_saved": co2_saved,
                "landfill_waste_prevented": landfill_waste_prevented,
                "total_material_recovered": total_material_recovered,
                "multipliers": {k: round(v, 4) for k, v in multipliers.items()}
            }
            
        except Exception as e:
            logger.error(f"Error calculating material recovery: {str(e)}")
            raise
    
    def get_condition_multiplier(self, condition):
        """Get condition multiplier"""
        condition_df = self.dataframes.get('condition')
        if condition_df is None or condition_df.empty:
            return 1.0
        
        for idx, row in condition_df.iterrows():
            condition_value = str(row[condition_df.columns[0]]).lower().strip()
            if condition_value == condition.lower().strip():
                return float(row[condition_df.columns[1]])
        
        return 1.0