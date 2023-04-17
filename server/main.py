from __init__ import create_app
from flask import send_from_directory
app = create_app()

@app.route('/')
def index():
    return 'Backend'

# @app.route('/')
# def serve():
#     return send_from_directory(app.static_folder, 'index.html')

# @app.route('/<path:path>')
# def static_files(path):
#     return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run()
