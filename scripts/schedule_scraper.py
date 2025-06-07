import schedule
import time
import subprocess

def run_scraper():
    subprocess.run([
        "python", "-m", "bit_scrapper.cli.main",
        "--config", "examples/sample_config.json",
        "--url", "https://target_domain.com",
        "--format", "json",
        "--output", "output"
    ])

# Scheduling once a day, at 9 AM
schedule.every().day.at("09:00").do(run_scraper)

print("Bitscrapper scheduler started. Running at 9 AM daily.")
while True:
    schedule.run_pending()
    time.sleep(60)