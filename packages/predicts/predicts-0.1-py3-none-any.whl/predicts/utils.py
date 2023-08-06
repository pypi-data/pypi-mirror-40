from pathlib import Path
import joblib

class Loader:
    @staticmethod
    def load_model(path:str):
        p = Path(path)
        joblib.load(p)