import pandas as pd
import logging
from config import Config

logger = logging.getLogger(__name__)

class ExcelLoader:
    """Handles loading of Excel data"""
    
    def __init__(self, file_path=Config.EXCEL_FILE_PATH):
        self.file_path = file_path
        self.dataframes = {}
    
    def load_all_sheets(self):
        """Load all required Excel sheets"""
        try:
            # Load brand sheet
            self.dataframes['brand'] = pd.read_excel(
                self.file_path,
                sheet_name=Config.SHEET_BRAND,
                header=0
            )
            
            # Load multiplier sheets
            multiplier_sheets = {
                'storage': Config.SHEET_STORAGE,
                'battery': Config.SHEET_BATTERY,
                'weight': Config.SHEET_WEIGHT,
                'age': Config.SHEET_AGE,
                'condition': Config.SHEET_CONDITION,
                'ram': Config.SHEET_RAM
            }
            
            for key, sheet_name in multiplier_sheets.items():
                self.dataframes[key] = pd.read_excel(
                    self.file_path,
                    sheet_name=sheet_name,
                    skiprows=Config.MULTIPLIER_SKIP_ROWS,
                    header=0
                )
            
            # Load price sheet
            self.dataframes['price'] = pd.read_excel(
                self.file_path,
                sheet_name=Config.SHEET_PRICE,
                skiprows=Config.PRICE_SKIP_ROWS,
                header=0
            )
            
            # Clean dataframes
            self._clean_dataframes()
            
            logger.info("✓ All Excel sheets loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading Excel files: {str(e)}")
            raise
    
    def _clean_dataframes(self):
        """Clean dataframes by removing NaN rows"""
        multiplier_keys = ['storage', 'battery', 'weight', 'age', 'condition', 'ram']
        
        for key in multiplier_keys:
            if key in self.dataframes:
                df = self.dataframes[key]
                # Keep only rows where both columns have values
                df = df.dropna(subset=[df.columns[0], df.columns[1]], how='any')
                self.dataframes[key] = df
    
    def get_dataframe(self, key):
        """Get a specific dataframe by key"""
        return self.dataframes.get(key)
    
    def get_all_dataframes(self):
        """Get all loaded dataframes"""
        return self.dataframes