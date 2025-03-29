import os

# Bot configuration
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8091844787:AAF05xMaC9v9xB-s7-Viw1c5xcjWy2KMP6Q")  # Replace with your bot token
API_ID = int(os.environ.get("API_ID", "24061032"))  # Replace with your API ID
API_HASH = os.environ.get("API_HASH", "5ad029547f2eeb5a0b68b05d0db713be")  # Replace with your API hash

# Spoiler Mode configuration (set to True or False)
SPOILER_MODE = os.environ.get("SPOILER_MODE", "True").lower() == "true"

# MongoDB URI (default value if not set in environment)
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://Villainmusic01:deathnote0p@cluster0.nah8e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # MongoDB URI for your database

# List of Sudo users (IDs of users with admin privileges)
SUDO_USERS = [5909658683]  # Add the user ID(s) of the admins
