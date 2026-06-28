# Day 7: Pipeline execution entry point
import json
import sys
from pathlib import Path

def load_validation_config(config_path: Path) -> dict:
    """
    Safely reads and parses the JSON validation configuration file.
    """
    # Decision: Use explicit path checking instead of letting json.load crash blindly
    if not config_path.exists():
        print(f"[ERROR] Configuration file missing at: {config_path.resolve()}")
        sys.exit(1)
        
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)
            
        # Validate that our configuration itself isn't structurally malformed
        verify_config_structure(config_data)
        return config_data

    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON syntax in config file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected system error reading config: {e}")
        sys.exit(1)

def verify_config_structure(config: dict):
    """
    Validates that the configuration file itself contains the mandatory structural keys.
    """
    mandatory_keys = ["expected_columns", "required_fields", "data_types", "rules"]
    missing_keys = [key for key in mandatory_keys if key not in config]
    
    if missing_keys:
        # Decision: Raise a clean, narrative error over a generic KeyError
        raise ValueError(f"Malformed configuration file. Missing mandatory sections: {missing_keys}")

def main():
    print("--- Day 1: Starting DataPulse Engine Initialisation ---")
    
    # Decision: Use pathlib.Path objects for robust, cross-platform file paths (Windows vs Mac/Linux)
    config_file_path = Path("datapulse_engine/config/validation_rules.json")
    #when first running, the file path was incorrect, had to change to correct path 6/28/26
    
    print(f"Loading rules engine from {config_file_path}...")
    rules_engine = load_validation_config(config_file_path)
    
    print("[SUCCESS] Validation configuration parsed and verified.")
    print(f"Tracking total expected columns: {len(rules_engine['expected_columns'])}")
    print(f"Enforcing null checks on required fields: {rules_engine['required_fields']}")

if __name__ == "__main__":
    main()
