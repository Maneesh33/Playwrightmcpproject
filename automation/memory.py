import json
import os

MEMORY_FILE = "memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return set()

    with open(MEMORY_FILE, "r") as f:
        data = json.load(f)
        return set(data)


def save_memory(links_set):
    with open(MEMORY_FILE, "w") as f:
        json.dump(list(links_set), f, indent=2)


def filter_new_jobs(jobs):
    seen_links = load_memory()

    new_jobs = []
    updated_links = set(seen_links)

    for job in jobs:
        link = job.get("link")

        if link and link not in seen_links:
            new_jobs.append(job)
            updated_links.add(link)

    save_memory(updated_links)

    print(f"\n🧠 Memory: {len(new_jobs)} new jobs, {len(jobs) - len(new_jobs)} duplicates removed")

    return new_jobs
