from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory database (for demonstration)
items = []

@app.route('/')
def index():
    return render_template('index.html', items=items)

# CREATE
@app.route('/create', methods=['GET', 'POST'])
def create_item():
    if request.method == 'POST':
        new_item = request.form.get('itemName')
        if new_item:
            items.append(new_item)
        return redirect(url_for('index'))
    return render_template('create_item.html')

# READ (handled by index route, which shows items)

# UPDATE
@app.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    if item_id < 0 or item_id >= len(items):
        return redirect(url_for('index'))
    if request.method == 'POST':
        updated_item = request.form.get('itemName')
        if updated_item:
            items[item_id] = updated_item
        return redirect(url_for('index'))
    return render_template('update_item.html', item_id=item_id, item_value=items[item_id])

# DELETE
@app.route('/delete/<int:item_id>', methods=['GET'])
def delete_item(item_id):
    if item_id >= 0 and item_id < len(items):
        items.pop(item_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
