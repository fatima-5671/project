from scraper.crawler import crawl_subcategory, get_categories
from scraper.exporters import export_category_summary, export_products
from scraper.parsers import parse_product_detail
from scraper.utils import deduplicate

DATA_DIR = "data"
PRODUCTS_CSV = f"{DATA_DIR}/products.csv"
SUMMARY_CSV = f"{DATA_DIR}/category_summary.csv"


def main():
    print("=== Catalog Scraper ===")
    print("Target: https://webscraper.io/test-sites/e-commerce/static\n")

    # Step 1 — Discover categories and subcategories
    print("Step 1: Discovering categories...")
    categories = get_categories()

    if not categories:
        print("No categories found. Exiting.")
        return

    print(f"Found {len(categories)} subcategories:")
    for c in categories:
        print(f"  {c['category']} > {c['subcategory']}")

    # Step 2 — Collect product links (all pages)
    print("\nStep 2: Collecting product links with pagination...")
    all_product_refs = []
    for cat_info in categories:
        refs = crawl_subcategory(cat_info)
        all_product_refs.extend(refs)

    print(f"\nTotal product links collected: {len(all_product_refs)}")

    # Step 3 — Visit each product detail page
    print("\nStep 3: Scraping product detail pages...")
    products = []
    for i, ref in enumerate(all_product_refs, 1):
        print(f"  [{i}/{len(all_product_refs)}] {ref['url']}")
        product = parse_product_detail(ref)
        if product:
            products.append(product)

    print(f"\nScraped {len(products)} products successfully.")

    # Step 4 — Deduplicate by URL
    print("\nStep 4: Deduplicating...")
    products, duplicates_removed = deduplicate(products)
    print(f"  Duplicates removed : {duplicates_removed}")
    print(f"  Unique products    : {len(products)}")

    # Step 5 — Export data
    print("\nStep 5: Exporting data...")
    export_products(products, PRODUCTS_CSV)
    export_category_summary(products, duplicates_removed, SUMMARY_CSV)

    print("\n=== Done ===")


if __name__ == "__main__":
    main()
