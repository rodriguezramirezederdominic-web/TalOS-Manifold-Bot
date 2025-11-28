import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Manifold API Key
MANIFOLD_API_KEY = os.getenv("MANIFOLD_API_KEY")

# OpenAI API Key for the 'Brain'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Bot settings
BOT_USERNAME = "TalOS_Bot"  # Designated username for this task
TARGET_CREATOR_USERNAME = "MikhailTal" 

# Risk Management
KELLY_FRACTION = 0.25  # Quarter Kelly to be conservative
MAX_BET_MANA = 50      # Cap max bet to prevent ruin on one error
MIN_EDGE = 0.05        # Minimum edge (5%) required to place a bet