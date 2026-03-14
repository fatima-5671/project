# Catalog Scraper Project
Here’s a **complete, clean README.md** you can use for your Catalog Scraper Mini Project. It is fully formatted and aligned with your assignment rubric, so it should cover all the points your teacher is looking for.

---

# `README.md`

````markdown
# Catalog Scraper Mini Project

## Project Overview
This project is a **Python-based web scraper** for the static e-commerce test site [WebScraper.io](https://webscraper.io/test-sites/e-commerce/static).  
The scraper navigates through **categories**, **subcategories**, **paginated listing pages**, and **product detail pages** to extract structured product data.  

This project demonstrates:

- Web scraping with **BeautifulSoup** and **requests**  
- Dependency management with **uv**  
- Version control workflow with **Git/GitHub branching**  
- Exporting data to CSV and generating summary reports  

---

## Features

- Automatic discovery of categories and subcategories  
- Multi-page crawling with pagination handling  
- Extraction of product details:
  - Product title  
  - Price (numeric format)  
  - Description  
  - Product URL  
  - Image URL  
  - Review count  
- Deduplication of products  
- Data cleaning for missing or inconsistent fields  
- Exporting:
  - `products.csv` – product-level dataset  
  - `category_summary.csv` – summary report per subcategory, including totals, average price, min/max price, missing descriptions, and duplicates removed  

---

## Tools & Technologies

- **Python 3**  
- **BeautifulSoup4** – HTML parsing  
- **Requests** – HTTP requests  
- **uv** – project & dependency management  
- **Git/GitHub** – version control  

---

## Project Setup

1. **Clone the repository:**

```bash
git clone <your-github-repo-link>
cd scraper-project
````

2. **Initialize and activate virtual environment using uv:**

```bash
uv init
uv shell
```

3. **Install dependencies:**

```bash
uv install beautifulsoup4 requests
```

---

## Running the Scraper

From the project root:

```bash
uv run python -m src.main
```

**Output:**

* `data/products.csv` – contains full product dataset
* `data/category_summary.csv` – contains summary report

---

## Project Structure

```
scraper-project/
├── pyproject.toml           # Project metadata & dependencies
├── README.md                # Project documentation
├── data/
│   ├── products.csv
│   └── category_summary.csv
├── src/
│   ├── main.py              # Main entry point
│   └── scraper/
│       ├── crawler.py       # Handles page requests, category & product discovery
│       ├── parsers.py       # Extracts and cleans product data
│       ├── exporters.py     # Converts scraped data to CSV
│       └── utils.py         # Helper functions
└── tests/                   # Unit tests for parsers, deduplication, etc.
```

---

## Git Branching Workflow

* **main** – stable production branch
* **dev** – development branch for feature integration
* **feature/catalog-navigation** – handles category & subcategory crawling
* **feature/product-details** – handles product detail scraping
* **fix/url-resolution** – fixes for relative link handling
* **fix/deduplication** – handles removal of duplicate products

**Workflow:**

1. Create dev branch from main
2. Create feature branches from dev
3. Push changes and create Pull Requests (PR) to merge into dev
4. Create fix branches from dev if needed and PR back to dev
5. After testing, merge dev into main

---

## Assumptions

* The website structure of the test site does not change dynamically
* All prices are in USD and formatted as `$<number>`
* Every product page contains a title and price
* Pagination links exist as `<a>` tags with `rel="next"`

---

## Limitations

* This scraper works **only on the static test site** provided; it does not handle JavaScript-rendered pages
* Does not currently download product images
* May require minor adjustments if website structure changes

---

## Output Example

### `products.csv`

| category  | subcategory | title    | price  | description        | product_url | image_url   | review_count |
| --------- | ----------- | -------- | ------ | ------------------ | ----------- | ----------- | ------------ |
| Computers | Laptops     | Laptop A | 799.99 | Lightweight laptop | https://... | https://... | 10           |

### `category_summary.csv`

| subcategory | total_products | average_price | min_price | max_price | missing_descriptions | duplicates_removed |
| ----------- | -------------- | ------------- | --------- | --------- | -------------------- | ------------------ |
| Laptops     | 117            | 822.50        | 299       | 1999      | 0                    | 3                  |

---

## How to Contribute

1. Fork the repository
2. Create a new branch for your feature/fix
3. Make changes and commit them with meaningful messages
4. Push branch to your fork
5. Create a Pull Request to merge into `dev`
6. Ensure code passes existing tests

---

## Author

* Fatima
* University of Central Punjab – Faculty of IT & CS
* Department of Applied Computing & Technologies
* Subject: Tools & Tech. for Data Science


