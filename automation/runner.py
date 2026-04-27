import os
from datetime import datetime
from memory import filter_new_jobs
from scraper import scrape_all
from saver import save_to_excel

def write_log(role, location, total, new_jobs, duplicates, filename):
    os.makedirs("logs", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"logs/run_{timestamp}.log"

    with open(log_file, "w") as f:
        f.write(f"🔍 Role: {role}\n")
        f.write(f"📍 Location: {location}\n\n")

        f.write(f"📊 Total Scraped: {total}\n")
        f.write(f"🧠 New Jobs: {new_jobs}\n")
        f.write(f"♻️ Duplicates Removed: {duplicates}\n\n")

        f.write(f"📁 Saved File: {filename}\n")

    print(f"📝 Log saved: {log_file}")

if __name__ == "__main__":
    role = "data analyst"
    location = "Hyderabad"

    print(f"\n🔍 Searching: {role} in {location}")

    raw_jobs = scrape_all(role, location, max_jobs=200)

    total_scraped = len(raw_jobs)

    # 🧠 Apply memory filter
    data = filter_new_jobs(raw_jobs)

    new_jobs = len(data)
    duplicates = total_scraped - new_jobs

    # 💾 Save file
    filename = save_to_excel(data, role, location)

    # 📝 Write log
    write_log(role, location, total_scraped, new_jobs, duplicates, filename)