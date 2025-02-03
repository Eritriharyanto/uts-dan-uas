from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data storage (like a database)
items = [
    {"id": 1, "name": "Item1", "price": 10.99},
    {"id": 2, "name": "Item2", "price": 19.99},
]

# Tampilkan semua data dari data Items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

# Tampilkan data berdasarkan ID dari data Items
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

# Menambahkan data ke dalam data Items
@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "Invalid data"}), 400
    new_item = {
        "id": items[-1]["id"] + 1 if items else 1,
        "name": data["name"],
        "price": data["price"]
    }
    items.append(new_item)
    return jsonify(new_item), 201

# Edit data dalam Items berdasarkan ID
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    item = next((item for item in items if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    if "name" in data:
        item["name"] = data["name"]
    if "price" in data:
        item["price"] = data["price"]
    return jsonify(item)

# Menghapus data dalam Items
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item["id"] != item_id]
    return jsonify({"message": "Item deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
