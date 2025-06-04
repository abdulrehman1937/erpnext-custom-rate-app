frappe.ui.form.on('Purchase Receipt Item', {
    item_code: updateDefaultRate,
    custom_rate_default: updateDefaultRate,
    conversion_factor: updateDefaultRate,
});

async function updateDefaultRate(frm, cdt, cdn) {
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
         else if(row.custom_rate_default===0 || !row.custom_rate_default && row.rate){
           const calculated = (row.rate * default_uom_cf) / row.conversion_factor;
            console.log("Calculated custom rate default:", calculated);
            frappe.model.set_value(cdt, cdn, 'custom_rate_default', calculated);
         }
         

    } catch (err) {
        console.error("Custom rate update failed:", err);
    }
}
