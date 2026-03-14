from bs4 import BeautifulSoup

from .utils import BASE_URL, clean_text, resolve_url, safe_get


def get_categories(base_url=BASE_URL):
    """
    Scrape the site to discover all categories and subcategories.
    Strategy:
      1. Fetch the home page and collect category links (class="category-link").
      2. Visit each category page and collect subcategory links
         (class="subcategory-link") from the expanded sidebar.
    Returns a list of dicts: {category, subcategory, url}.
    """
    response = safe_get(base_url)
    if not response:
        print("Could not load main page.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    categories = []

    # Sidebar menu: <ul id="side-menu"> or <ul class="nav flex-column">
    nav = soup.find("ul", id="side-menu")
    if not nav:
        nav = soup.find("ul", class_="flex-column")
    if not nav:
        print("Sidebar navigation not found.")
        return []

    # Each top-level category has class="category-link"
    category_links = nav.find_all("a", class_="category-link")
    for cat_link in category_links:
        cat_name = clean_text(cat_link.find("span").get_text() if cat_link.find("span") else cat_link.get_text())
        cat_url = resolve_url(base_url, cat_link.get("href", ""))

        # Visit the category page to discover subcategories
        cat_response = safe_get(cat_url)
        if not cat_response:
            continue

        cat_soup = BeautifulSoup(cat_response.text, "html.parser")
        sub_links = cat_soup.find_all("a", class_="subcategory-link")

        if sub_links:
            for sub_link in sub_links:
                sub_name = clean_text(
                    sub_link.find("span").get_text() if sub_link.find("span") else sub_link.get_text()
                )
                sub_url = resolve_url(base_url, sub_link.get("href", ""))
                categories.append(
                    {
                        "category": cat_name,
                        "subcategory": sub_name,
                        "url": sub_url,
                    }
                )
        else:
            # No subcategories — use the category page itself
            categories.append(
                {
                    "category": cat_name,
                    "subcategory": cat_name,
                    "url": cat_url,
                }
            )

    return categories


def get_product_links(soup, page_url):
    """Extract all product page links from a listing page."""
    links = []
    for a_tag in soup.find_all("a", class_="title"):
        href = a_tag.get("href", "")
        if href:
            links.append(resolve_url(page_url, href))
    return links


def get_next_page_url(soup, current_url):
    """Return the URL of the next pagination page, or None if there isn't one."""
    # The next-page link has rel="next" attribute
    next_a = soup.find("a", rel="next")
    if next_a and next_a.get("href"):
        return resolve_url(current_url, next_a.get("href"))
    return None


def crawl_subcategory(cat_info):
    """
    Crawl all paginated listing pages for a subcategory.
    Returns a list of dicts: {url, category, subcategory, page}.
    """
    url = cat_info["url"]
    page_num = 1
    all_product_refs = []

    print(f"  Crawling: {cat_info['category']} > {cat_info['subcategory']}")

    while url:
        response = safe_get(url)
        if not response:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        links = get_product_links(soup, url)
        print(f"    Page {page_num}: found {len(links)} products")

        for link in links:
            all_product_refs.append(
                {
                    "url": link,
                    "category": cat_info["category"],
                    "subcategory": cat_info["subcategory"],
                    "page": page_num,
                }
            )

        next_url = get_next_page_url(soup, url)
        url = next_url
        page_num += 1

    return all_product_refs
