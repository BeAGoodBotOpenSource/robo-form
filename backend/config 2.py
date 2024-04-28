from dotenv import dotenv_values
import openai

config = dotenv_values(".env")
debug_status = config["DEBUG"] == "TRUE"
openai.api_key = config["OPENAI_API_KEY"]

whitelist_origins = [
    'http://localhost:3000', 
    'http://localhost:8000',
    'https://robo-form.onrender.com',
    'http://35.160.120.126',
    'http://44.233.151.27',
    'https://www.jotform.com/*',
    'http://34.211.200.85'] if debug_status else ['https://robo-form.onrender.com',]