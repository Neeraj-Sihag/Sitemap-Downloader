import os
import time
import signal
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
from bs4 import BeautifulSoup

# Paths to GeckoDriver and Firefox binary
geckodriver_path = "C:/WebDrivers/geckodriver.exe"
firefox_binary_path = "C:/Program Files/Mozilla Firefox/firefox.exe"

# Set up Firefox options
firefox_options = Options()
firefox_options.binary_location = firefox_binary_path
firefox_options.add_argument("--headless")

# Global control flag for graceful shutdown
running = True

def signal_handler(sig, frame):
    """Handle keyboard interrupt and exit gracefully."""
    global running
    running = False
    print("\n\n[INFO] Interrupted! Exiting and closing browser session...")
    driver.quit()
    print("[INFO] Browser session closed. All tasks completed.")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Display GitHub Repository Information
print("\n==========================================")
print("Sitemap Downloader by Neeraj Sihag")
print("Repository: https://github.com/Neeraj-Sihag/Sitemap-Downloader")
print("==========================================\n")

# Initialize the Firefox WebDriver
print("[INFO] Starting browser session...")
service = Service(geckodriver_path)
driver = webdriver.Firefox(service=service, options=firefox_options)
driver.set_page_load_timeout(60)
print("[INFO] Browser session started successfully.\n")

def create_output_folder(base_url):
    """Create a site-specific folder in the output directory based on the domain name."""
    domain = urlparse(base_url).netloc
    site_output_dir = os.path.join("output", domain)
    os.makedirs(site_output_dir, exist_ok=True)
    return site_output_dir

def save_page_source(url, page_source, output_dir, extension):
    """Save the page source to a file with the correct extension based on content type."""
    slug = urlparse(url).path.split("/")[-1] or "index"
    filepath = os.path.join(output_dir, f"{slug}.{extension}")
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(page_source)
    print(f"    [SAVED] {slug}.{extension} to {output_dir}")

def fetch_sitemap(url, max_retries=3, load_timeout=60):
    """Fetch sitemap content with retries and return page source."""
    driver.set_page_load_timeout(load_timeout)
    attempts = 0
    while attempts < max_retries:
        if not running:
            return None, None  # Exit if interrupted
        try:
            print(f"[FETCHING] URL: {url}")
            driver.get(url)
            time.sleep(1)
            page_source = driver.page_source

            # Detect HTML or XML content
            if "<html" in page_source.lower():
                print("    [DETECTED] HTML content. Parsing as HTML sitemap.")
                return "html", page_source
            
            print("    [DETECTED] XML content. Parsing as XML sitemap.")
            return "xml", page_source
        except (WebDriverException, TimeoutException) as e:
            attempts += 1
            print(f"    [RETRY] Attempt {attempts} failed for {url}. Error: {e}")
            time.sleep(5)
    print(f"[ERROR] Failed to load {url} after {max_retries} attempts.")
    return None, None

def parse_sitemap_links(content_type, page_source):
    """Parse and return sitemap links from the page source, handling XML and HTML."""
    links = []
    if content_type == "xml":
        try:
            root = ET.fromstring(page_source)
            namespace = ""
            if root.tag.startswith("{"):
                namespace = root.tag.split("}")[0] + "}"
            
            if root.tag == f"{namespace}sitemapindex" or root.tag == f"{namespace}urlset":
                for element in root.findall(f".//{namespace}loc"):
                    link = element.text.strip()
                    if link.endswith(".xml") or link.endswith(".html"):
                        links.append(link)
                print(f"    [INFO] {len(links)} links found in XML sitemap.")
            else:
                print("    [WARNING] Not a valid XML sitemap format. Skipping.")
        except ET.ParseError as e:
            print("    [ERROR] XML ParseError:", e)
    elif content_type == "html":
        soup = BeautifulSoup(page_source, "html.parser")
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.endswith(".xml") or href.endswith(".html"):
                links.append(href)
        print(f"    [INFO] {len(links)} links found in HTML sitemap.")
    return links

def download_single_sitemap():
    url = input("Enter the full URL of the single sitemap: ")
    output_dir = create_output_folder(url)
    content_type, page_source = fetch_sitemap(url)
    if page_source:
        extension = "xml" if content_type == "xml" else "html"
        save_page_source(url, page_source, output_dir, extension)
        print("\n[SUCCESS] Single sitemap download completed.\n")

def download_index_sitemap():
    url = input("Enter the full URL of the index sitemap: ")
    output_dir = create_output_folder(url)
    content_type, page_source = fetch_sitemap(url)
    if not page_source:
        print("[ERROR] Failed to load index sitemap.\n")
        return
    
    # Save the index sitemap itself
    extension = "xml" if content_type == "xml" else "html"
    save_page_source(url, page_source, output_dir, extension)
    print("[INFO] Index sitemap saved successfully.\n")

    # Parse and download nested sitemaps
    nested_sitemaps = parse_sitemap_links(content_type, page_source)
    if not nested_sitemaps:
        print("[INFO] No nested sitemaps found.\n")
        return

    for i, sitemap_url in enumerate(nested_sitemaps, start=1):
        if not running:
            break  # Exit if interrupted
        print(f"\n[FETCHING] Nested sitemap {i}: {sitemap_url}")
        nested_content_type, nested_page_source = fetch_sitemap(sitemap_url)
        if nested_page_source:
            extension = "xml" if nested_content_type == "xml" else "html"
            save_page_source(sitemap_url, nested_page_source, output_dir, extension)
    print("\n[SUCCESS] Index sitemap and all nested sitemaps downloaded successfully.\n")

def download_range_of_sitemaps():
    base_url = input("Enter the base URL structure (use '{}' as a placeholder for the number): ")
    start = int(input("Enter the starting number: "))
    end = int(input("Enter the ending number: "))
    output_dir = create_output_folder(base_url)
    
    for i in range(start, end + 1):
        if not running:
            break  # Exit if interrupted
        url = base_url.format(i)
        print(f"\n[FETCHING] Sitemap {i}: {url}")
        content_type, page_source = fetch_sitemap(url)
        if page_source:
            extension = "xml" if content_type == "xml" else "html"
            save_page_source(url, page_source, output_dir, extension)
    print("\n[SUCCESS] Range of sitemaps downloaded successfully.\n")

# Main script logic
def main():
    print("Choose an option:")
    print("1. Download a single sitemap")
    print("2. Download an index sitemap and all its nested sitemaps")
    print("3. Download a range of sitemaps")
    
    choice = input("Enter your choice (1, 2, or 3): ")
    
    if choice == "1":
        print("\n[START] Starting single sitemap download...\n")
        download_single_sitemap()
    elif choice == "2":
        print("\n[START] Starting index sitemap download with nested sitemaps...\n")
        download_index_sitemap()
    elif choice == "3":
        print("\n[START] Starting download of a range of sitemaps...\n")
        download_range_of_sitemaps()
    else:
        print("[ERROR] Invalid choice. Exiting.\n")

try:
    main()
finally:
    driver.quit()
    print("\n[INFO] Browser session closed.")
    print("[INFO] All tasks completed successfully.")
