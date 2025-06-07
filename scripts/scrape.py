# CLI entry point
import argparse
from bit_scrapper.config.loader import load_config
from bit_scrapper.core.scraper import BitScrapper
from bit_scrapper.utils.writer import write_csv, write_json

def main():
    parser = argparse.ArgumentParser(description="BitScrapper CLI - Core Engine")
    parser.add_argument("--url", type=str, help="The URL to scrape", required=True)
    parser.add_argument("--config", type=str, help="Path to the JSON configuration file", required=True)
    parser.add_argument("--output", type=str, default="output.json", help="Output file path")
    parser.add_argument("--format", type=str, choices=["json", "csv"], default="json", help="Output format")

    args = parser.parse_args()

    # Load the configuration
    config = load_config(args.config)

    # Init the scraper
    bitscrapper = BitScrapper(config)

    # Execute the operation
    results = bitscrapper.run(args.url)

    if args.format == "json": write_json(results, args.output)
    else: write_csv(results, args.output)

    print(f"Scraping completed. Output written to {args.output}")

if __name__ == "__main__":
    main()