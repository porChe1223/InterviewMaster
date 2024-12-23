from flasker import app
from flask import render_template

@app.route('/')
def main():
    text = 'Hello, World!'
    return render_template(
        'main.html', text = text # 引数はいくつでも追加可能
    )

if __name__ == '__main__':
    app.debug = True
    app.run()
