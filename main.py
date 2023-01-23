from flask import Flask, render_template
app = Flask("My Project", template_folder='templates/startbootstrap-sb-admin-2-gh-pages', static_folder='templates/startbootstrap-sb-admin-2-gh-pages')


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()