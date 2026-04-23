# database.py
# Simple in-memory storage (no SQLAlchemy)
_items = []
_next_id = 1

def get_all():
    return _items

def add(item_data):
    global _next_id
    item_data["id"] = _next_id
    _items.append(item_data)
    _next_id += 1
    return item_data

def delete(item_id):
    global _items
    _items = [i for i in _items if i.get("id") != item_id]
    return True
