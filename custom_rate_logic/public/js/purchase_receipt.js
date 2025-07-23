frappe.ui.form.on('Purchase Receipt Item', {
    item_code: function(frm, cdt, cdn) {
        // Wait for system to set the rate after item selection
        setTimeout(() => handleRateChange(frm, cdt, cdn), 500);
    },
    rate: function(frm, cdt, cdn) {
        handleRateChange(frm, cdt, cdn);
    },
    custom_rate_default: function(frm, cdt, cdn) {
        handleCustomRateDefault(frm, cdt, cdn);
    },
    conversion_factor: function(frm, cdt, cdn) {
        handleConversionFactor(frm, cdt, cdn);
    }
});

async function handleRateChange(frm, cdt, cdn) {
    console.log("rate changed");
    const row = locals[cdt][cdn];
    
    try {
        const { message: item } = await frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Item",
                name: row.item_code
            }
        });

        const default_uom = item.custom_default_unit_of_rate;
        const default_uom_cf = item.uoms.find(({ uom }) => uom === default_uom)?.conversion_factor || 1;
        
        // Calculate what the custom_rate_default should be based on current rate
        const calculated = ((row.rate * default_uom_cf) / row.conversion_factor).toFixed(3);

        // Only update if different from current custom_rate_default
        if (calculated !==  parseFloat(row.custom_rate_default).toFixed(3)) {
            console.log("Updating custom_rate_default to match rate:", calculated);
            frappe.model.set_value(cdt, cdn, 'custom_rate_default', calculated);
        }
    } catch (err) {
        console.error("Rate change handling failed:", err);
    }
}

async function handleCustomRateDefault(frm, cdt, cdn) {
    console.log("custom rate default changed");
    const row = locals[cdt][cdn];
    
    try {
        const { message: item } = await frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Item",
                name: row.item_code
            }
        });

        const default_uom = item.custom_default_unit_of_rate;
        const default_uom_cf = item.uoms.find(({ uom }) => uom === default_uom)?.conversion_factor || 1;
        
        const new_rate = (row.custom_rate_default / default_uom_cf) * row.conversion_factor;
        frappe.model.set_value(cdt, cdn, 'rate', new_rate);
    } catch (err) {
        console.error("Custom rate default handling failed:", err);
    }
}

async function handleConversionFactor(frm, cdt, cdn) {
    console.log("conversion factor changed");
    const row = locals[cdt][cdn];
    
    try {
        const { message: item } = await frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Item",
                name: row.item_code
            }
        });

        const default_uom = item.custom_default_unit_of_rate;
        const default_uom_cf = item.uoms.find(({ uom }) => uom === default_uom)?.conversion_factor || 1;
        
        if (row.custom_rate_default) {
            const new_rate = (row.custom_rate_default / default_uom_cf) * row.conversion_factor;
            frappe.model.set_value(cdt, cdn, 'rate', new_rate);
        }
    } catch (err) {
        console.error("Conversion factor handling failed:", err);
    }
}
