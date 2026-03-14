from bs4 import BeautifulSoup

from .utils import clean_text, parse_price, resolve_url, safe_get


def parse_product_detail(product_ref):
    """
    Fetch a product detail page and extract all required fields.
    Returns a dict with product data, or None if the page fails to load.

    Actual HTML structure on this site:
      Title      : <h4 class="title card-title">
      Price      : <span itemprop="price"> inside <h4 class="price ...">
      Description: <p class="description card-text">
      Reviews    : <span itemprop="reviewCount"> inside <p class="review-count">
      Stars      : <span class="ws-icon ws-icon-star">
      Spec label : <label class="memory"> + active <button class="btn swatch ...active">
      Image      : <img class="image img-fluid img-responsive">
    """
    url = product_ref["url"]
    response = safe_get(url)
    if not response:
        print(f"    Skipping (failed to load): {url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # --- Title ---
    title = ""
    title_tag = soup.find("h4", class_="card-title")
    if not title_tag:
        title_tag = soup.find("a", class_="title")
    if title_tag:
        title = clean_text(title_tag.get_text())

    # --- Price (from <span itemprop="price">) ---
    price = None
    price_span = soup.find("span", itemprop="price")
    if price_span:
        price = parse_price(clean_text(price_span.get_text()))

    # --- Description ---
    description = ""
    desc_tag = soup.find("p", class_="description")
    if not desc_tag:
        desc_tag = soup.find("p", class_="card-text")
    if desc_tag:
        description = clean_text(desc_tag.get_text())

    # --- Review count and star rating ---
    review_count = ""
    rating = ""
    review_span = soup.find("span", itemprop="reviewCount")
    if review_span:
        review_count = clean_text(review_span.get_text())
    stars = soup.find_all("span", class_="ws-icon-star")
    if stars:
        rating = str(len(stars))

    # --- Image URL ---
    image_url = ""
    img_tag = soup.find("img", class_="img-responsive")
    if not img_tag:
        img_tag = soup.find("img", class_="img-fluid")
    if img_tag:
        image_url = resolve_url(url, img_tag.get("src", ""))

    # --- Spec: label (e.g. "HDD:") + the active swatch value ---
    spec = ""
    spec_label = soup.find("label", class_="memory")
    active_swatch = soup.find("button", class_="active")
    if spec_label and active_swatch:
        spec = clean_text(spec_label.get_text()) + " " + clean_text(active_swatch.get_text())
    elif spec_label:
        spec = clean_text(spec_label.get_text())

    return {
        "category": product_ref["category"],
        "subcategory": product_ref["subcategory"],
        "title": title,
        "price": price,
        "url": url,
        "image_url": image_url,
        "description": description,
        "review_count": review_count,
        "rating": rating,
        "spec": spec,
        "page": product_ref["page"],
    }
