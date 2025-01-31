from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials
import datetime

app = Flask(__name__)

# Google Sheets Setup
SPREADSHEET_ID = "1uEBeT_JA1VPDJGYF2Tsf-2CkPeNJy6voO7R5mBUaEvQ"  # Replace with your Spreadsheet ID
SHEET_NAME = "Sheet1"  # Change if needed
CREDS_FILE = r'C:\Users\Admin\Downloads\car-data-logging-fc029dc0f2d4.json'  # Replace with your JSON file path

# Authenticate and connect to Google Sheets
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(CREDS_FILE, scopes=scopes)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

@app.route('/log_obd_data', methods=['POST'])
def log_obd_data():
    try:
        data = request.json  # Receive JSON payload from OBD app

        # Extract Data
        gps_time = data.get("gps_time", datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S GMT"))
        device_time = data.get("device_time", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        longitude = data.get("longitude", "N/A")
        latitude = data.get("latitude", "N/A")
        speed = data.get("speed", "N/A")
        altitude = data.get("altitude", "N/A")
        bearing = data.get("bearing", "N/A")
        fuel_level = data.get("fuel_level", "N/A")
        fuel_used = data.get("fuel_used", "N/A")
        air_fuel_ratio = data.get("air_fuel_ratio", "N/A")

        # Append data to Google Sheets
        row_data = [gps_time, device_time, longitude, latitude, speed, altitude, bearing, fuel_level, fuel_used, air_fuel_ratio]
        sheet.append_row(row_data)

        return jsonify({"message": "Data logged successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
