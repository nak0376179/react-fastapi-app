# protected_handler.py
from mangum import Mangum

from app.main import app  # FastAPI アプリの import

handler = Mangum(app)
