TalOS (Targeted Algorithmic Logic Operating System)

TalOS is a specialized prediction market agent designed to trade exclusively on markets created by Manifold user MikhailTal.

Design Philosophy (Filosofía de Diseño)

Unlike generic bots that use simple heuristics (like betting toward 50%), TalOS is Agentic. It uses an LLM (GPT-4 via OpenAI) to read the specific text of the market, perform a reference class analysis, and generate a calibrated probability.

It utilizes the Fractional Kelly Criterion for money management, ensuring that bet sizes are proportional to the mathematical "edge" the bot perceives, drastically reducing the risk of ruin while maximizing logarithmic wealth growth.

Installation (Instalación)

Clone the repo.

Install dependencies:

pip install -r requirements.txt


Create a .env file with your keys:

MANIFOLD_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here


Run the bot:

python tal_bot.py


Improvements over manifoldbot

This repository improves on the base manifoldbot pattern in several ways:

Modular Intelligence: Separates the trading loop (tal_bot.py) from the decision logic (brain.py) and the financial logic (kelly.py).

Creator Targeting: Implements specific API filtering to target a single creator ID.


Dynamic Sizing: Replaces static bet amounts with Kelly Criterion math.

