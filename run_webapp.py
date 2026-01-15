"""
Run Flask webapp for Telegram Mini App
"""
from webapp.app import app
from config import HOST, PORT, DEBUG

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)

