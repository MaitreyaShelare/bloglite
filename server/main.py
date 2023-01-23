from __init__ import create_app

app = create_app()

@app.route('/')
def index():
    return 'Backend'

if __name__ == '__main__':
    app.run(debug=True)
