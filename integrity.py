import pandas as pd

REQUIRED_COLS = [
    'Name', 'Age', 'Gender', 'Blood Type', 'Medical Condition',
    'Date of Admission', 'Doctor', 'Hospital', 'Insurance Provider',
    'Billing Amount', 'Room Number', 'Admission Type', 'Discharge Date',
    'Medication', 'Test Results'
]

def check_integrity(df: pd.DataFrame):
    assert all(col in df.columns for col in REQUIRED_COLS)
    assert df.duplicated().sum() == 0
    assert df.isnull().sum().sum() == 0
    return True
