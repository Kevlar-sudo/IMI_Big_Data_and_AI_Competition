from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DB_NAME = 'mydatabase.db'

def init_db():
    """Initialize the SQLite database if it doesn't already exist."""
    db_exists = os.path.exists(DB_NAME)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    if not db_exists:
        c.execute('''
            CREATE TABLE items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        conn.commit()
    conn.close()

# Call init_db() once at startup
init_db()

@app.route('/')
def index():
    # Retrieve items from the SQLite database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name FROM items")
    all_items = c.fetchall()
    conn.close()

    # all_items is a list of tuples: [(1, 'Item1'), (2, 'Item2'), ...]
    # Pass this to the template
    return render_template('index.html', items=all_items)

@app.route('/create', methods=['GET', 'POST'])
def create_item():
    if request.method == 'POST':
        new_item = request.form.get('itemName')
        if new_item:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("INSERT INTO items (name) VALUES (?)", (new_item,))
            conn.commit()
            conn.close()
        return redirect(url_for('index'))
    return render_template('create_item.html')

@app.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    if request.method == 'POST':
        updated_item = request.form.get('itemName')
        if updated_item:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("UPDATE items SET name=? WHERE id=?", (updated_item, item_id))
            conn.commit()
            conn.close()
        return redirect(url_for('index'))
    else:
        # Fetch the current item name
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT name FROM items WHERE id=?", (item_id,))
        row = c.fetchone()
        conn.close()

        if not row:
            # If no item found, redirect or handle error
            return redirect(url_for('index'))
        
        current_name = row[0]
        return render_template('update_item.html', item_id=item_id, item_value=current_name)

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM items WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
