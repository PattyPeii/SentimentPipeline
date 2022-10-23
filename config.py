import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "host": os.getenv("RABBIT_HOST", "localhost"),
    "database": {
        "connection": os.getenv("MONGODB_URI", "localhost:27017"),
        "name": os.getenv("DATABASE_NAME", "comment"),
        "collections": {
            "comments": os.getenv("DATABASE_TASKS_COLLECTION", "comments"),
        }
    },
    "NLP_API": {
        "url": os.getenv("NLP_URL", ""),
        "key": os.getenv("API_KEY", ""),
    }
}