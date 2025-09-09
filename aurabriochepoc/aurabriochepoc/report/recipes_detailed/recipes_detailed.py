import frappe
from frappe.utils import flt

def execute(filters=None):
    columns = get_columns()
    data = []

    # Get BOMs
    boms = frappe.get_all("BOM",
        filters={"is_active": 1},
        fields=["name", "item", "item_name", "total_cost"])

    for bom in boms:
        standard_rate = frappe.db.get_value("Item", bom.item, "standard_rate") or 0

        # ===== Header: Main Item (bold row) =====
        data.append({
            "ingredient": f"{bom.item_name} ({bom.item})",
            "pos": None,
            "act_qty": None,
            "base_unit": None,
            "ave": None,
            "cos": None,
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
                "pos": pos,
                "ingredient": f"{bi.item_name} ({bi.item_code})",
                "act_qty": bi.qty,
                "base_unit": bi.stock_uom,
                "ave": bi.rate,
                "cos": cos,
                "cos_percent": (cos / bom.total_cost * 100) if bom.total_cost else None,
                "indent": 1.0,
                "parent": bom.item
            })
            pos += 1

        # ===== Footer: Standard Rate (same level as header) =====
        data.append({
            "ingredient": f"Net Sales Price: {standard_rate}",
            "pos": None,
            "act_qty": None,
            "base_unit": None,
            "ave": None,
            "cos": None,
            "cos_percent": None,
            "indent": 1.0   # Same as Main Item
        })

        # Spacer row
        data.append({
            "ingredient": None,
            "pos": None,
            "act_qty": None,
            "base_unit": None,
            "ave": None,
            "cos": None,
            "cos_percent": None,
		})

    return columns, data


def get_columns():
    return [
        {"label": "Pos", "fieldname": "pos", "fieldtype": "Int", "width": 40},
        {"label": "Ingredient", "fieldname": "ingredient", "fieldtype": "Data", "width": 670},
        {"label": "ACT QTY", "fieldname": "act_qty", "fieldtype": "Float", "width": 160},
        {"label": "Base Unit", "fieldname": "base_unit", "fieldtype": "Data", "width": 160},
        {"label": "AVE", "fieldname": "ave", "fieldtype": "Currency", "width": 170},
        {"label": "COS", "fieldname": "cos", "fieldtype": "Currency", "width": 170},
        {"label": "COS %", "fieldname": "cos_percent", "fieldtype": "Percent", "width": 170},
    ]