import os

class Config:
    """Application configuration"""
    
    # Base directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # File paths
    EXCEL_FILE_PATH = os.path.join(BASE_DIR, "ewaste_metal_lookup_tables.xlsx")
    MODEL_PATH = os.path.join(BASE_DIR, "extratrees_resale_model.pkl")
    MODEL_COLUMNS_PATH = os.path.join(BASE_DIR, "model_columns.pkl")
    
    # Excel sheet names
    SHEET_BRAND = "Brand_Metal_Content"
    SHEET_STORAGE = "Storage_Multiplier"
    SHEET_BATTERY = "Battery_Multiplier"
    SHEET_WEIGHT = "Weight_Multiplier"
    SHEET_AGE = "Age_Depreciation"
    SHEET_CONDITION = "Condition_Multiplier"
    SHEET_RAM = "RAM_Multiplier"
    SHEET_PRICE = "Recovery_Value_Formula"
    
    # Excel loading parameters
    MULTIPLIER_SKIP_ROWS = 2
    PRICE_SKIP_ROWS = 3
    
    # Default values
    DEFAULT_METAL_PRICES = {
        "gold": 5000,
        "silver": 70,
        "copper": 0.7,
        "lithium": 35
    }
    
    DEFAULT_MATERIAL_CONTENT = {
        "gold": 0.034,
        "silver": 0.35,
        "copper": 15,
        "lithium": 3
    }
    
    DEFAULT_MULTIPLIERS = {
        "storage": 1.0,
        "ram": 1.0,
        "battery": 1.0,
        "weight": 1.0,
        "age": 0.5,
        "condition": 1.0
    }
    
    # Environmental factors
    CO2_PER_KG = 0.012  # 12g CO2 saved per kg
    
    # Current year for age calculation
    CURRENT_YEAR = 2026
    
    # Resale price multiplier
    RESALE_MULTIPLIER = 86
    
    # Flask settings
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}