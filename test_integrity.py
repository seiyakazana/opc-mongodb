import pandas as pd
from integrity import check_integrity, REQUIRED_COLS

def test_integrity_ok():
    df = pd.DataFrame({col: ["x"] for col in REQUIRED_COLS})
    assert check_integrity(df)

def test_missing_values():
    df = pd.DataFrame({col: ["x"] for col in REQUIRED_COLS})
    df.loc[0, "Age"] = None
    try:
        check_integrity(df)
        assert False
    except AssertionError:
        assert True
