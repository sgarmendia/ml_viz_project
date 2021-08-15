import os
from dotenv import load_dotenv

load_dotenv()

DEV=os.getenv('DEV', True)
PORT=os.getenv('PORT', 8000)
MONGO_URL=os.getenv('MONGO_URL')