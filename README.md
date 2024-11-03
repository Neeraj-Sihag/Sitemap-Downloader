# Sitemap Downloader

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)  
A powerful Python tool for downloading XML and HTML sitemaps, supporting nested and range-based sitemap structures. Works on both Windows and Linux.

**Author**: Neeraj Sihag  
**Repository**: [GitHub - Sitemap Downloader](https://github.com/Neeraj-Sihag/Sitemap-Downloader)

---

## ✨ Features

- **Single Sitemap Download**: Retrieve and save a single XML or HTML sitemap.
- **Index Sitemap with Nested Links**: Automatically download all sitemaps linked from an index sitemap.
- **Range of Sitemaps**: Download a series of numbered sitemaps (e.g., `sitemap-1.xml` to `sitemap-50.xml`).

---

## ⚙️ Prerequisites

1. **Python 3.7+**  
2. **Firefox Browser** - [Download here](https://www.mozilla.org/en-US/firefox/new/).
3. **GeckoDriver** - [Install instructions](https://github.com/mozilla/geckodriver/releases).  
   - Place `geckodriver` in your system’s PATH or specify its location in the script.

---

## 🚀 Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/Neeraj-Sihag/Sitemap-Downloader.git
   cd Sitemap-Downloader
   ```

2. **Install Dependencies**  
   - Using `requirements.txt`:  
     ```bash
     pip install -r requirements.txt
     ```
   - Or install directly:  
     ```bash
     pip install selenium beautifulsoup4 urllib3
     ```

---

## 🧩 Usage

Run the script:

```bash
python sitemap-downloader.py
```

### Options

1. **Download a single sitemap**: Download a single XML or HTML sitemap.
2. **Download an index sitemap**: Download an index sitemap and all nested sitemaps.
3. **Download a range of sitemaps**: Specify a base URL and range to download multiple numbered sitemaps.

---

## 🔍 Examples

- **Single Sitemap**: `https://example.com/sitemap.xml`
- **Index Sitemap**: `https://example.com/sitemap_index.xml`
- **Range**: `https://example.com/sitemap-{}.xml` from 1 to 50

---

## 📌 Additional Information

- **Interrupting**: Press `Ctrl+C` to stop the script gracefully.
- **Output Directory**: Sitemaps are saved in `output/<domain>`.
- **Headless Mode**: The script runs Firefox in headless mode. To disable, remove `firefox_options.add_argument("--headless")` in the script.

---

## 🛠 Troubleshooting

- **Browser Not Starting**: Ensure `geckodriver` is installed and the path is correct.
- **Permission Issues**: Verify write permissions for the output directory.
- **File Not Found Error**: Ensure paths to Firefox and GeckoDriver are correct.

For **Windows**:
   - Place `geckodriver.exe` in `C:/WebDrivers` or update the path in the script.
   - Run `python sitemap-downloader.py` from the command prompt.

For **Linux**:
   - Place `geckodriver` in `/usr/local/bin/` or update the path in the script.
   - Run `python3 sitemap-downloader.py` from the terminal.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
