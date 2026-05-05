from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")