
import os
import json
from datetime import datetime

def ensure_output_dir():
    """Create output directory if it doesn't exist."""
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def generate_report():
    """Generate a sample JSON report file."""
    report = {
        "status": "success",
        "message": "Python script executed successfully!",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data": [1, 2, 3, 4, 5]
    }
    return report

def save_report(output_dir, report):
    """Save the generated report to the output folder."""
    output_path = os.path.join(output_dir, "report.json")
    with open(output_path, "w") as f:
        json.dump(report, f, indent=4)
    print(f"Report generated: {output_path}")

def main():
    print("Starting main.py script...")

    # Step 1: Prepare output directory
    output_dir = ensure_output_dir()

    # Step 2: Create dummy data (your business logic goes here)
    report = generate_report()

    # Step 3: Save output for Jenkins deployment
    save_report(output_dir, report)

    print("main.py execution finished successfully.")

if __name__ == "__main__":
    main()
