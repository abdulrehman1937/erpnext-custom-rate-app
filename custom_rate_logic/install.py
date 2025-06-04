import frappe

def after_install():
    """
    Called after the app is installed. Creates custom fields.
    """
    print("✅ Custom Pricing App installed successfully!")
    create_item_custom_fields()
    create_purchase_order_item_custom_fields()
    create_sales_order_item_custom_fields()
    create_purchase_receipt_item_custom_fields()
    move_custom_rate_field()
    hide_standard_rate()

def create_item_custom_fields():
    """
    Adds 'custom_default_unit_of_rate' to Item.
    """
    if not frappe.db.exists("Custom Field", {"dt": "Item", "fieldname": "custom_default_unit_of_rate"}):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Item",
            "label": "Default Unit Of Rate",
            "fieldname": "custom_default_unit_of_rate",
            "fieldtype": "Link",
            "options": "UOM",
            "insert_after": "default_uom", # Renders below Default Unit Of Measure
            "description": "Default UOM to be used for rate calculations.",
            "reqd": 1,
            "read_only": 0
        }).insert(ignore_permissions=True)
        print("Custom Field 'Default Unit Of Rate' added to Item.")
    else:
        print("Custom Field 'Default Unit Of Rate' already exists on Item.")

def create_purchase_receipt_item_custom_fields():
    """
    Adds 'custom_rate_default' to Purchase Order Item.
    """
    if not frappe.db.exists("Custom Field", {"dt": "Purchase Receipt Item", "fieldname": "custom_rate_default"}):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Purchase Receipt Item",
            "label": "Rate (Default UOM)",
            "fieldname": "custom_rate_default",
            "fieldtype": "Currency",
            "precision": 2, # Adjust precision as needed
            "insert_after": "rate", # Or any other field you prefer
            "description": "Rate in the Item's Default Unit Of Rate.",
            "reqd": 1,
            "read_only": 0
        }).insert(ignore_permissions=True)
        print("Custom Field 'Rate (Default UOM)' added to Purchase Order Item.")
    else:
        print("Custom Field 'Rate (Default UOM)' already exists on Purchase Order Item.")

def create_purchase_order_item_custom_fields():
    """
    Adds 'custom_rate_default' to Purchase Order Item.
    """
    if not frappe.db.exists("Custom Field", {"dt": "Purchase Order Item", "fieldname": "custom_rate_default"}):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Purchase Order Item",
            "label": "Rate (Default UOM)",
            "fieldname": "custom_rate_default",
            "fieldtype": "Currency",
            "precision": 2, # Adjust precision as needed
            "insert_after": "qty", # Or any other field you prefer
            "description": "Rate in the Item's Default Unit Of Rate.",
            "reqd": 1,
            "read_only": 0
        }).insert(ignore_permissions=True)
        print("Custom Field 'Rate (Default UOM)' added to Purchase Order Item.")
    else:
        print("Custom Field 'Rate (Default UOM)' already exists on Purchase Order Item.")


def create_sales_order_item_custom_fields():
    """
    Adds 'custom_rate_default' to Sales Order Item.
    """
    if not frappe.db.exists("Custom Field", {"dt": "Sales Order Item", "fieldname": "custom_rate_default"}):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Sales Order Item",
            "label": "Rate (Default UOM)",
            "fieldname": "custom_rate_default",
            "fieldtype": "Currency",
            "precision": 2, # Adjust precision as needed
            "insert_after": "qty", # Or any other field you prefer
            "description": "Rate in the Item's Default Unit Of Rate.",
            "reqd": 1,
            "read_only": 0
        }).insert(ignore_permissions=True)
        print("Custom Field 'Rate (Default UOM)' added to Sales Order Item.")
    else:
        print("Custom Field 'Rate (Default UOM)' already exists on Sales Order Item.")
def move_custom_rate_field():
    """
    Move custom_rate_default field up using Property Setter for idx
    """
    target_idx = 6  # Adjust as needed
    for doctype in ["Purchase Order Item", "Sales Order Item", "Purchase Receipt Item"]:
        fieldname = "custom_rate_default"
        property_name = f"{doctype}-{fieldname}-idx"

        if not frappe.db.exists("Property Setter", {"name": property_name}):
            frappe.get_doc({
                "doctype": "Property Setter",
                "doc_type": doctype,
                "doctype_or_field": "DocField",  # <-- This is required
                "field_name": fieldname,
                "property": "idx",
                "value": target_idx,
                "property_type": "Int",
                "name": property_name
            }).insert()
            print(f"✅ Moved '{fieldname}' in '{doctype}' to idx {target_idx}")
        else:
            print(f"⚠️ Property Setter for '{fieldname}' in '{doctype}' already exists.")

def hide_standard_rate():
    """
    Hides the default 'rate' field in child tables using Property Setters
    """
    for doctype in ["Purchase Order Item", "Sales Order Item", "Purchase Receipt Item"]:
        fieldname = "rate"
        property_name = f"{doctype}-{fieldname}-hidden"

        if not frappe.db.exists("Property Setter", {"name": property_name}):
            frappe.get_doc({
                "doctype": "Property Setter",
                "doc_type": doctype,
                "doctype_or_field": "DocField",  # <-- This is required
                "field_name": fieldname,
                "property": "hidden",
                "value": 1,
                "property_type": "Check",
                "name": property_name
            }).insert()
            print(f"✅ Hid 'rate' field in '{doctype}'")
        else:
            print(f"⚠️ Rate field in '{doctype}' already hidden or Property Setter exists.")
