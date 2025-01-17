from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DB_NAME = 'mydatabase.db'

@app.route('/')
def index():
    """Homepage with a link to the lookup feature."""
    return render_template('index.html')

@app.route('/lookup', methods=['GET', 'POST'])
def lookup_item():
    """Lookup and display a record based on the given eft_id."""
    record = None
    if request.method == 'POST':
        eft_id = request.form.get('eftId')
        if eft_id:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            # Query the database for the specified eft_id
            c.execute("SELECT * FROM items WHERE eft_id=?", (eft_id,))
            record = c.fetchone()
            conn.close()
    return render_template('lookup_item.html', record=record)

if __name__ == '__main__':
    app.run(debug=True)
