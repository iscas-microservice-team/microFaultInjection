from app import app
from flask import render_template


@app.route('/')
@app.route('/usage')
def usage():
    return render_template('frontPage.html', title='API Usage Guide')


