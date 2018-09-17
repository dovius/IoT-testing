import sys
from app import create_app

app = create_app()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        app.run(host="bevardis", port=8081, debug=True)
    else:
        app.run(host="0.0.0.0", port=8080, debug=True)