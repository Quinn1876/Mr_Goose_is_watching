from flask import Flask
app = Flask(__name__)

from dotenv import load_dotenv
load_dotenv()

@app.route('/')
def hello_world():
  return 'Hello, World!'

if __name__ == "__main__":
  app.run(debug=True)
