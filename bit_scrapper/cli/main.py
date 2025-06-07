import argparse
import os
from bit_scrapper.core.scraper import BitScrapper
from bit_scrapper.config.loader import load_config
from bit_scrapper.utils.writer import write_csv, write_json

def main():
    parser = argparse.ArgumentParser(description="BitScrapper CLI - Web Scraping Utility")
    parser.add_argument("--config", type=str, required=True, help="Path to JSON config file")
    parser.add_argument("--url", type=str, required=True, help="Start URL for scraping")
    parser.add_argument("--format", type=str, choices=["json", "csv"], default="json", help="Output format")
    parser.add_argument("--output", type=str, default="output", help="Output filename without extension")
    parser.add_argument("--max-pages", type=int, help="Override max_pages in config")

    args = parser.parse_args()

    if not os.path.exists(args.config):
        print(f"Error: Config file {args.config} not found.")
        return

    config = load_config(args.config)
    if args.max_pages:
        config["pagination"]["max_pages"] = args.max_pages

    scraper = BitScrapper(config)
    results = scraper.run(args.url)

    filename = f"{args.output}.{args.format}"
    if args.format == "json":
        write_json(results, filename)
    else:
        write_csv(results, filename)

    print(f"Scraping completed. Output saved to {filename}")

if __name__ == "__main__":
    main()
