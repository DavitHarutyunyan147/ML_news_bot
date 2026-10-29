import csv
import re
import time
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse


SECTIONS = {
    "Քաղաքական": "https://www.aravot.am/category/news/politics/",
    "Մշակույթ": "https://www.aravot.am/category/news/culture/",
    "Սպորտ": "https://www.aravot.am/category/news/sport/",
}

TOTAL_COUNT = 1000
EXTRA_LINKS = 1.2
LINES_COUNT = 10
MAX_LISTING_PAGES = 100
REQUEST_DELAY = 0.5
OUTPUT_FILE = "news.csv"

ARTICLE_PATTERN = re.compile(r"/\d{4}/\d{2}/\d+/?")

session = requests.Session()
session.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
})


def get_soup(url):
    try:
        response = session.get(
            url,
            timeout=(5, 15)
        )
        response.raise_for_status()
        response.encoding = response.apparent_encoding

        return BeautifulSoup(response.text, "html.parser")

    except requests.RequestException as error:
        print(f"Ներբեռնման սխալ՝ {url}")
        print(f"Պատճառ՝ {error}")
        return None


def normalize_url(url):
    parsed = urlparse(url)

    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        "",
        "",
        ""
    )).rstrip("/") + "/"


def is_article_url(url):
    parsed = urlparse(url)

    return (
        parsed.netloc.lower().endswith("aravot.am")
        and ARTICLE_PATTERN.search(parsed.path) is not None
    )


def get_listing_links(soup, page_url, section):
    heading = None

    for tag in soup.find_all(["h1", "h2", "h3", "h4"]):
        if tag.get_text(" ", strip=True).strip() == section:
            heading = tag
            break

    if heading is None:
        print(f"Չգտնվեց «{section}» բաժնի վերնագիրը։")
        return []

    links = []

    for link in heading.find_all_next("a", href=True):
        classes = link.get("class", [])
        text = link.get_text(" ", strip=True).casefold()

        if "page-numbers" in classes:
            break

        if text in ("լրահոս", "հաջորդ", "next", "»", "›"):
            break

        url = normalize_url(urljoin(page_url, link["href"]))

        if is_article_url(url):
            links.append(url)

    return links


def get_next_page(soup, current_url):
    current_path = urlparse(current_url).path
    match = re.search(r"/page/(\d+)/?$", current_path)
    current_number = int(match.group(1)) if match else 1

    for link in soup.select("a.page-numbers[href]"):
        text = link.get_text(" ", strip=True).casefold()

        if text in ("»", "›", "հաջորդ", "next"):
            candidate = normalize_url(
                urljoin(current_url, link["href"])
            )

            if candidate != normalize_url(current_url):
                return candidate

    for link in soup.select("a.page-numbers[href]"):
        text = link.get_text(" ", strip=True)

        if text.isdigit() and int(text) == current_number + 1:
            return normalize_url(urljoin(current_url, link["href"]))

    if match:
        next_path = re.sub(
            r"/page/\d+/?$",
            f"/page/{current_number + 1}/",
            current_path
        )
    else:
        next_path = current_path.rstrip("/") + "/page/2/"

    parsed = urlparse(current_url)

    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        next_path,
        "",
        "",
        ""
    ))


def collect_article_links(section, section_url, limit):
    collected = []
    seen = set()
    visited_pages = set()
    current_url = section_url

    print(f"\nԲԱԺԻՆ՝ {section}")

    for page_number in range(1, MAX_LISTING_PAGES + 1):
        if len(collected) >= limit:
            break

        current_url = normalize_url(current_url)

        if current_url in visited_pages:
            break

        visited_pages.add(current_url)

        soup = get_soup(current_url)

        if soup is None:
            break

        for url in get_listing_links(soup, current_url, section):
            if url not in seen:
                seen.add(url)
                collected.append(url)

                if len(collected) >= limit:
                    break

        print(f"Էջ {page_number}՝ հղումներ {len(collected)}")

        current_url = get_next_page(soup, current_url)
        time.sleep(REQUEST_DELAY)

    return collected


def extract_article(url):
    soup = get_soup(url)

    if soup is None:
        return None

    title_element = None

    for selector in [
        "h1.entry-title",
        "h1.post-title",
        "main h1",
        "article h1",
        "h1",
    ]:
        element = soup.select_one(selector)

        if element and element.get_text(" ", strip=True):
            title_element = element
            break

    if title_element is None:
        print(f"Վերնագիրը չգտնվեց՝ {url}")
        return None

    title = title_element.get_text(" ", strip=True)

    paragraphs = []
    seen_paragraphs = set()

    stop_headings = {
        "կարդացեք նաև",
        "նման նյութեր",
        "մեկնաբանություններ",
        "պատասխանել",
        "ամենաընթերցված",
    }

    for element in title_element.find_all_next(
        ["p", "h1", "h2", "h3", "h4", "h5", "h6"]
    ):
        if element.name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            heading_text = " ".join(
                element.get_text(" ", strip=True).split()
            ).casefold()

            if heading_text in stop_headings:
                break

            continue

        text = " ".join(element.get_text(" ", strip=True).split())

        if len(text) < 30:
            continue

        if text in seen_paragraphs:
            continue

        seen_paragraphs.add(text)
        paragraphs.append(text)

        if len(paragraphs) >= LINES_COUNT:
            break

    article_text = "\n".join(paragraphs).strip()

    if len(article_text) < 100:
        print(
            f"Տեքստը բավարար չէ՝ {url} "
            f"({len(article_text)} նիշ)"
        )
        return None

    return {
        "title": title,
        "text": article_text,
        "url": url,
    }


def main():
    all_articles = []

    per_section = TOTAL_COUNT // len(SECTIONS)
    remainder = TOTAL_COUNT % len(SECTIONS)

    section_number = 0

    for section, section_url in SECTIONS.items():
        target = per_section
        if section_number < remainder:
            target = target + 1
        section_number = section_number + 1

        links = collect_article_links(section, section_url, int(target * EXTRA_LINKS))

        successful = 0

        for index, url in enumerate(links, start=1):
            if successful >= target:
                break

            print(f"[{section}] {index}/{len(links)} (հաջող՝ {successful}/{target}) {url}")

            try:
                article = extract_article(url)
            except Exception as error:
                print(f"Հոդվածի մշակման սխալ՝ {error}")
                continue

            if article is None:
                continue

            article["section"] = section
            all_articles.append(article)
            successful += 1

            time.sleep(REQUEST_DELAY)

        print(f"«{section}» բաժնից ստացվեց՝ {successful}")

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "text", "url", "section"])
        writer.writeheader()
        writer.writerows(all_articles)

    print(f"\nԸնդհանուր հոդվածներ՝ {len(all_articles)} (նպատակը՝ {TOTAL_COUNT})")
    print(f"Պահվեց՝ {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
