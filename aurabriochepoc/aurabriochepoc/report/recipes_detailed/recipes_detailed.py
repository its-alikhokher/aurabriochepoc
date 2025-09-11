import frappe
from frappe.utils import flt

def execute(filters=None):
    columns = get_columns()
    data = []

    bom_filters = {"is_active": 1}
    if filters and filters.get("item"):
        bom_filters["item"] = filters.get("item")

    # Get BOMs
    boms = frappe.get_all("BOM",
        filters=bom_filters,
        fields=["name", "item", "item_name", "total_cost"])


    for bom in boms:
        standard_rate = frappe.db.get_value("Item", bom.item, "standard_rate") or 0

        # ===== Header: Main Item =====
        data.append({
            "net_sales_price": standard_rate,   # Sirf yahan value hogi
            "ingredient": f"{bom.item_name} ({bom.item})",
            "pos": None,
            "act_qty": None,
            "base_unit": None,
            "ave": None,
            "cos": bom.total_cost,
            "cos_percent": None,
            "indent": 0.0,
            "expanded": 0
        })

        # ===== Child: BOM Items =====
        bom_items = frappe.get_all("BOM Item",
            filters={"parent": bom.name},
            fields=["item_code", "item_name", "qty", "uom", "stock_uom", "rate"])

        pos = 1
        total_cos = 0
        for bi in bom_items:
            cos = flt(bi.qty * bi.rate, 2)
            total_cos += cos

            data.append({
                "net_sales_price": None,   # Niche rows me blank hoga
                "pos": pos,
                "ingredient": f"{bi.item_name}",
                "act_qty": bi.qty,
                "base_unit": bi.stock_uom,
                "ave": bi.rate,
                "cos": cos,
                "cos_percent": (cos / bom.total_cost * 100) if bom.total_cost else None,
                "indent": 1.0,
                "parent": bom.item
            })
            pos += 1


        # Spacer row
        data.append({
            "ingredient": None,
            "pos": None,
            "act_qty": None,
            "base_unit": None,
            "ave": None,
            "cos": None,
            "cos_percent": None,
            "net_sales_price": None,   # Sirf yahan value hogi
		})

    return columns, data


def get_columns():
    return [
        {"label": "Pos", "fieldname": "pos", "fieldtype": "Int", "width": 40},
        {"label": "Ingredient", "fieldname": "ingredient", "fieldtype": "Data", "width": 400},
        {"label": "Net Sales Price", "fieldname": "net_sales_price", "fieldtype": "Currency", "width": 150},
        {"label": "ACT QTY", "fieldname": "act_qty", "fieldtype": "Float", "width": 150},
        {"label": "Base Unit", "fieldname": "base_unit", "fieldtype": "Data", "width": 150},
        {"label": "AVE", "fieldname": "ave", "fieldtype": "Currency", "width": 150},
        {"label": "COS", "fieldname": "cos", "fieldtype": "Currency", "width": 150},
        {"label": "COS %", "fieldname": "cos_percent", "fieldtype": "Percent", "width": 150},
    ]

