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
                        is_stock_item: 0
                    }
                };
            }
        }
    ]
};
