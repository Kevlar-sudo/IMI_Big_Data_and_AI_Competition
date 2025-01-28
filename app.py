from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.ensemble import IsolationForest
import sqlite3
import logging

app = Flask(__name__)

DB_NAME = 'mydatabase.db'

# --- Data Loading and Preprocessing (from database) ---

def load_atm_data():
    """Loads and preprocesses ATM transaction data from the database."""
    conn = sqlite3.connect(DB_NAME)
    try:
        query = "SELECT * FROM abm"  # Assuming 'abm' table for ATM data
        df = pd.read_sql_query(query, conn)

        # Basic preprocessing
        df['amount_cad'] = pd.to_numeric(df['amount_cad'], errors='coerce')
        df.dropna(subset=['amount_cad'], inplace=True)
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        df['day_of_week'] = df['transaction_date'].dt.dayofweek
        try:
            df['hour_of_day'] = pd.to_datetime(df['transaction_time'], format='%H:%M:%S').dt.hour
        except ValueError:
            # If the above format fails, try an alternative format
            df['hour_of_day'] = pd.to_datetime(df['transaction_time'], format='%I:%M %p').dt.hour

        return df
    except Exception as e:
        print(f"Error loading ATM data: {e}")
        return None
    finally:
        conn.close()


def load_kyc_data():
    """Loads KYC data from the database."""
    conn = sqlite3.connect(DB_NAME)
    try:
        query = "SELECT customer_id, industry_code, employee_count, sales FROM kyc"
        kyc_data = pd.read_sql_query(query, conn)

        return kyc_data

    except Exception as e:
        print(f"Error loading KYC data: {e}")
        return None
    finally:
        conn.close()


# --- Feature Engineering ---
def create_features(df):
    """Creates features from ATM transaction data."""
    features = df.groupby('customer_id').agg(
        total_transactions=('customer_id', 'count'),
        avg_amount=('amount_cad', 'mean'),
        max_amount=('amount_cad', 'max'),
        std_amount=('amount_cad', 'std'),
        unique_locations=('city', 'nunique')  # Assuming 'city' represents location
    )

    features['amount_ratio'] = features['max_amount'] / features['avg_amount']

    # Fill NaN values with 0, you can adjust this strategy as needed
    features.fillna(0, inplace=True)

    return features


# --- Anomaly Detection Model ---

def train_anomaly_detection_model(features):
    """Trains a simple Isolation Forest model."""
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(features)
    return model


def detect_anomalies(model, features):
    """Predicts anomalies using the trained model."""
    predictions = model.predict(features)
    scores = model.decision_function(features)
    features['anomaly'] = predictions
    features['anomaly_score'] = scores
    return features


# --- Load data ---
atm_data = load_atm_data()
kyc_data = load_kyc_data()

if atm_data is not None and kyc_data is not None:
    # --- Join KYC data with ATM data ---
    atm_data = atm_data.merge(kyc_data, on='customer_id', how='left')

    # --- Create features ---
    features = create_features(atm_data)

    # --- Train the model ---
    model = train_anomaly_detection_model(features)

    # --- Detect anomalies ---
    anomalies = detect_anomalies(model, features)

    # --- Merge anomaly scores and flags back into the main ATM data ---
    atm_data = atm_data.merge(anomalies[['anomaly', 'anomaly_score']], left_on='customer_id', right_index=True,
                              how='left')


    # --- Rule-Based System ---
    def apply_rules(df):
        """Applies simple rule-based logic."""
        df['rule_based_flag'] = 0  # Initialize the column with 0

        # Rule 1: Large cash withdrawals (example threshold: $5000)
        df.loc[df['amount_cad'] > 5000, 'rule_based_flag'] = 1

        # Rule 2: Multiple transactions in a short period (example: within 1 hour)
        # Sort the DataFrame by customer_id and transaction_date
        df.sort_values(['customer_id', 'transaction_date'], inplace=True)

        # Calculate the time difference between consecutive transactions for each customer
        df['time_diff'] = df.groupby('customer_id')['transaction_date'].diff()

        # Flag transactions where the time difference is less than 1 hour (3600 seconds)
        df.loc[df['time_diff'].dt.total_seconds() < 3600, 'rule_based_flag'] = 1

        # Remove the 'time_diff' column as it's no longer needed
        df.drop('time_diff', axis=1, inplace=True)

        return df


    atm_data = apply_rules(atm_data)

    # --- Prepare data for the frontend ---
    alerts_data = atm_data[(atm_data['anomaly'] == -1) | (atm_data['rule_based_flag'] == 1)]

    # Clean the data for JSON serialization
    alerts_data = alerts_data.fillna('N/A')
    alerts_data = alerts_data.replace([True, False], [1, 0])
    alerts_data['transaction_date'] = alerts_data['transaction_date'].dt.strftime('%Y-%m-%d %H:%M:%S')

    alerts_data = alerts_data.to_dict(orient='records')

else:
    logging.error("Error: Data loading or preprocessing failed.")
    alerts_data = []
print(len(alerts_data))


@app.route('/')
def index():
    """Homepage with a link to the lookup feature."""
    return render_template('index_mvp.html')

@app.route('/get_alerts', methods=['GET'])
def get_alerts():
    logging.info(f"Alerts data: {alerts_data}")  # Log the data being sent
    return jsonify(alerts_data)
@app.route('/lookup', methods=['GET', 'POST'])
def lookup_item():
    """Lookup and display a record based on the given eft_id."""
    record = None
    if request.method == 'POST':
        eft_id = request.form.get('eftId')
        if eft_id:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            # Query the database for the specified eft_id
            c.execute("SELECT * FROM eft WHERE eft_id=?", (eft_id,))
            record = c.fetchone()
            conn.close()
    return render_template('lookup_item.html', record=record)

if __name__ == '__main__':
    app.run(debug=True)





