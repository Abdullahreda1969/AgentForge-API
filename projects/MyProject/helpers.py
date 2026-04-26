# helpers.py
from database import get_all_items, get_item_by_id, add_item, update_item, delete_item

def get_contacts():
    """جلب جميع contacts"""
    return get_all_items()

def get_contact(contact_id):
    """جلب contact محدد"""
    return get_item_by_id(contact_id)

def add_contact(name: str, description: str = ""):
    """إضافة contact جديد"""
    return add_item(name=name, description=description)

def update_contact(contact_id: int, **kwargs):
    """تحديث contact"""
    return update_item(contact_id, **kwargs)

def delete_contact(contact_id):
    """حذف contact"""
    return delete_item(contact_id)
