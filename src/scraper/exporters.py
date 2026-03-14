import csv
from collections import defaultdict
from pathlib import Path


def export_products(products, filepath):
    """Write the product list to a CSV file."""
    if not products:
        print("No products to export.")
        return

    Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "category",
        "subcategory",
        "title",
        "price",
        "url",
        "image_url",
        "description",
        "review_count",
        "rating",
        "spec",
        "page",
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(products)

    print(f"Exported {len(products)} products to {filepath}")


def export_category_summary(products, duplicates_removed, filepath):
    """
    Write a per-subcategory summary CSV with pricing stats and data quality counts.
    Columns: category, subcategory, total_products, avg_price, min_price,
             max_price, missing_descriptions, duplicates_removed
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    # Group products by (category, subcategory)
    groups = defaultdict(list)
    for p in products:
        key = (p.get("category", ""), p.get("subcategory", ""))
        groups[key].append(p)

    rows = []
    for (category, subcategory), items in sorted(groups.items()):
        prices = [p["price"] for p in items if p.get("price") is not None]
        missing_desc = sum(1 for p in items if not p.get("description"))
        rows.append(
            {
                "category": category,
                "subcategory": subcategory,
                "total_products": len(items),
                "avg_price": round(sum(prices) / len(prices), 2) if prices else "",
                "min_price": min(prices) if prices else "",
                "max_price": max(prices) if prices else "",
                "missing_descriptions": missing_desc,
                "duplicates_removed": duplicates_removed,
            }
        )

    fieldnames = [
        "category",
        "subcategory",
        "total_products",
        "avg_price",
        "min_price",
        "max_price",
        "missing_descriptions",
        "duplicates_removed",
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Exported category summary ({len(rows)} rows) to {filepath}")