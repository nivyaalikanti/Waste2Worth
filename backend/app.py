from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from config import Config
from utils.excel_loader import ExcelLoader
from models.resale_model import ResaleModel
from services.material_service import MaterialService
from services.feature_service import FeatureService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load configuration
app.config.from_object(Config)

# Initialize components
logger.info("Initializing application components...")

# Load Excel data
excel_loader = ExcelLoader()
excel_loader.load_all_sheets()

# Load ML model
resale_model = ResaleModel()
resale_model.load_model()

# Initialize services
material_service = MaterialService(excel_loader)
feature_service = FeatureService()

logger.info("Application initialized successfully")

def get_recommendation(resale_value, recycling_value):
    """Generate recommendation based on values"""
    if recycling_value == 0:
        return "Unable to determine (recycling value is zero)"
    
    ratio = resale_value / recycling_value if recycling_value > 0 else float('inf')
    
    if ratio > 3:
        return "Resell Recommended"
    elif ratio > 1.5:
        return "Consider Reselling"
    elif ratio > 0.8:
        return "Either option viable"
    else:
        return "Recycle Recommended"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        
        # Engineer features
        features, device_age = feature_service.engineer_features(data)
        
        # Get condition from request
        condition = data.get("condition", "Good")
        
        # Predict resale value
        resale_value = resale_model.predict(features)
        
        # Calculate material recovery
        material_results = material_service.calculate_material_recovery(
            brand=data["brand"],
            storage=float(data["internal_memory"]),
            ram=float(data["ram"]),
            battery=float(data["battery"]),
            weight=float(data["weight"]),
            age=device_age,
            condition=condition
        )
        
        # Get recommendation
        recommendation = get_recommendation(resale_value, material_results["recycling_value"])
        
        return jsonify({
            "resale_value": resale_value,
            "recycling_value": material_results["recycling_value"],
            "recommendation": recommendation,
            "gold": material_results["gold"],
            "silver": material_results["silver"],
            "copper": material_results["copper"],
            "lithium": material_results["lithium"],
            "co2_saved": material_results["co2_saved"],
            "landfill_waste_prevented": material_results["landfill_waste_prevented"],
            "total_material_recovered": material_results["total_material_recovered"],
            "multipliers": material_results["multipliers"]
        })
        
    except Exception as e:
        logger.error(f"Error in predict endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "API is running"})

if __name__ == "__main__":
    app.run(
        debug=Config.DEBUG,
        host=Config.HOST,
        port=Config.PORT
    )