import frappe

def before_uninstall():
    """
    Deletes custom fields created by custom_pricing_app on uninstallation.
    """
    print("🔧 Running custom field deletion script")
     #{"dt": "Item", "fieldname": "custom_default_unit_of_rate"},
    fields_to_delete = [
        {"dt": "Purchase Order Item", "fieldname": "custom_rate_default"},
        {"dt": "Sales Order Item", "fieldname": "custom_rate_default"},
        {"dt": "Purchase Receipt Item", "fieldname": "custom_rate_default"},
    ]

    for field_info in fields_to_delete:
        dt = field_info["dt"]
        fieldname = field_info["fieldname"]

        # The actual name is just: Doctype-fieldname
        cf_name = f"{dt}-{fieldname}"

        if frappe.db.exists("Custom Field", cf_name):
            try:
                frappe.delete_doc("Custom Field", cf_name, ignore_permissions=True)
                print(f"✅ Custom Field '{fieldname}' removed from '{dt}'.")
            except Exception as e:
                frappe.log_error(f"❌ Failed to delete Custom Field '{cf_name}': {e}")
                print(f"❌ Error deleting Custom Field '{fieldname}' from '{dt}': {e}")
        else:
            print(f"⚠️ Custom Field '{fieldname}' on '{dt}' does not exist, skipping.")
