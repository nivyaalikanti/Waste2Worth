import numpy as np
import logging
from config import Config

logger = logging.getLogger(__name__)

class FeatureService:
    """Handles feature engineering for the model"""
    
    @staticmethod
    def engineer_features(data):
        """
        Create engineered features from input data
        
        Args:
            data: Dictionary containing input features
        
        Returns:
            tuple: (features_dict, device_age)
        """
        features = {}
        
        # Extract basic features
        screen_size = float(data["screen_size"])
        rear_camera_mp = float(data["rear_camera_mp"])
        front_camera_mp = float(data["front_camera_mp"])
        internal_memory = float(data["internal_memory"])
        ram = float(data["ram"])
        battery = float(data["battery"])
        weight = float(data["weight"])
        release_year = int(data["release_year"])
        days_used = float(data["days_used"])
        new_price = float(data["normalized_new_price"])
        fourg = int(data["fourg"])
        fiveg = int(data["fiveg"])
        
        # Calculate derived values
        normalized_new_price = np.log(new_price)
        current_year = Config.CURRENT_YEAR
        device_age = max(0, current_year - release_year)
        
        # Add basic features
        features["screen_size"] = screen_size
        features["4g"] = fourg
        features["5g"] = fiveg
        features["rear_camera_mp"] = rear_camera_mp
        features["front_camera_mp"] = front_camera_mp
        features["internal_memory"] = internal_memory
        features["ram"] = ram
        features["battery"] = battery
        features["weight"] = weight
        features["release_year"] = release_year
        features["days_used"] = days_used
        features["normalized_new_price"] = normalized_new_price
        
        # Add engineered features
        features["device_age"] = device_age
        features["usage_ratio"] = days_used / (device_age * 365 + 1) if device_age > 0 else 0
        features["camera_total"] = rear_camera_mp + front_camera_mp
        features["battery_per_weight"] = battery / weight if weight > 0 else 0
        features["ram_storage_ratio"] = ram / (internal_memory + 1)
        features["storage_ram_product"] = internal_memory * ram
        features["camera_per_storage"] = (rear_camera_mp + front_camera_mp) / (internal_memory + 1)
        features["battery_age_ratio"] = battery / (device_age + 1)
        features["days_used_per_year"] = days_used / (device_age + 0.1) if device_age > 0 else days_used
        features["price_per_storage"] = normalized_new_price / (internal_memory + 1)
        features["price_per_ram"] = normalized_new_price / (ram + 1)
        features["battery_screen_ratio"] = battery / screen_size if screen_size > 0 else 0
        features["camera_ram_product"] = (rear_camera_mp + front_camera_mp) * ram
        features["storage_per_age"] = internal_memory / (device_age + 1)
        features["battery_ram_product"] = battery * ram
        
        # Add categorical features
        brand = data["brand"]
        brand_col = "device_brand_" + brand
        features[brand_col] = 1
        
        os_name = data["os"]
        if os_name == "iOS":
            features["os_iOS"] = 1
        elif os_name == "Windows":
            features["os_Windows"] = 1
        else:
            features["os_Others"] = 1
        
        return features, device_age