# helpers.py
_items = []
_next_id = 1

def get_contacts():
    return _items

def get_contact(contact_id):
    for item in _items:
        if item.get("id") == contact_id:
            return item
    return None

def add_contact(name: str, description: str = ""):
    global _next_id
    item = {"id": _next_id, "name": name, "description": description}
    _items.append(item)
    _next_id += 1
    return item

def delete_contact(contact_id):
    global _items
    _items = [i for i in _items if i.get("id") != contact_id]
    return True
