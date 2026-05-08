
# helpers.py
from database import get_all_items, get_item_by_id, add_item, update_item, delete_item

def get_items():
    """جلب جميع items"""
    return get_all_items()

def get_item(item_id):
    """جلب item محدد"""
    return get_item_by_id(item_id)

def add_item(name: str, description: str = ""):
    """إضافة item جديد"""
    return add_item(name=name, description=description)

def update_item(item_id: int, **kwargs):
    """تحديث item"""
    return update_item(item_id, **kwargs)

def delete_item(item_id):
    """حذف item"""
    return delete_item(item_id)
