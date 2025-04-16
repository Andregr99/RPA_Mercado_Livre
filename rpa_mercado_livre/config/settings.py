import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "scraper.log")
ML_URL = "https://www.mercadolivre.com.br"
TIMEOUT = 5000  

