from flask import Flask
app = Flask(__name__) # Create the app

app.secret_key = "loveyou3000"  # Needed for session and flash messages (learn in week 6)