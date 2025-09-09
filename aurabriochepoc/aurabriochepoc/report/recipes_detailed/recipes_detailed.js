// Copyright (c) 2025, Tridz Technologies Pvt. Ltd and contributors
// For license information, please see license.txt

frappe.query_reports["RECIPES DETAILED"] = {
	"filters": [
        {
            fieldname: "item",
            label: __("Item"),
            fieldtype: "Link",
            options: "Item",
            reqd: 0,
            get_query: function() {
                return {
                    filters: {
                        is_stock_item: 0   // optional: sirf stock items
                    }
                };
            }
        }
    ]
};