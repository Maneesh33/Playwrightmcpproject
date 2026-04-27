from playwright.sync_api import sync_playwright
import time


# ------------------ BROWSER SETUP ------------------ #
def launch_browser(p):
    browser = p.chromium.launch(
        headless=False,
        args=["--start-maximized"]
    )

    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
        viewport={"width": 1280, "height": 800}
    )

    page = context.new_page()
    page.set_default_timeout(15000)

    return browser, page


# ------------------ INDEED (BEST EFFORT) ------------------ #
def scrape_indeed(role, location, max_jobs=50):
    jobs = []

    with sync_playwright() as p:
        browser, page = launch_browser(p)

        url = f"https://in.indeed.com/jobs?q={role.replace(' ', '+')}&l={location.replace(' ', '+')}"
        print(f"\nOpening Indeed: {url}")

        page.goto(url)
        page.wait_for_timeout(6000)

        cards = page.locator("div.job_seen_beacon")
        count = cards.count()

        print("Indeed jobs found:", count)

        for i in range(min(count, max_jobs)):
            job = cards.nth(i)

            try:
                title = job.locator("h2").inner_text()
            except:
                title = "N/A"

            try:
                company = job.locator("[data-testid='company-name']").inner_text()
            except:
                company = "N/A"

            try:
                location_text = job.locator("[data-testid='text-location']").inner_text()
            except:
                location_text = location

            try:
                link = job.locator("a").first.get_attribute("href")
                if link:
                    link = "https://in.indeed.com" + link
                else:
                    link = "N/A"
            except:
                link = "N/A"

            jobs.append({
                "title": title,
                "company": company,
                "location": location_text,
                "link": link,
                "source": "Indeed"
            })

        browser.close()

    return jobs


# ------------------ NAUKRI (FIXED) ------------------ #
def scrape_naukri(role, location, max_jobs=100):
    jobs = []
    page_no = 1

    with sync_playwright() as p:
        browser, page = launch_browser(p)

        while len(jobs) < max_jobs:
            url = f"https://www.naukri.com/{role.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}-{page_no}"
            print(f"\nOpening Naukri Page {page_no}: {url}")

            page.goto(url)
            page.wait_for_timeout(5000)

            # scroll
            for _ in range(5):
                page.mouse.wheel(0, 2000)
                page.wait_for_timeout(1000)

            cards = page.locator("div.srp-jobtuple-wrapper")
            count = cards.count()

            print("Jobs found:", count)

            if count == 0:
                break

            for i in range(count):
                if len(jobs) >= max_jobs:
                    break

                job = cards.nth(i)

                try:
                    title = job.locator("a.title").inner_text()
                except:
                    title = "N/A"

                # 🔥 FIXED COMPANY SELECTOR
                try:
                    company = job.locator("a.comp-name").inner_text()
                except:
                    try:
                        company = job.locator("span.comp-name").inner_text()
                    except:
                        company = "N/A"

                try:
                    location_text = job.locator(".locWdth").inner_text()
                except:
                    location_text = location

                try:
                    link = job.locator("a.title").get_attribute("href")
                except:
                    link = "N/A"

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location_text,
                    "link": link,
                    "source": "Naukri"
                })

            page_no += 1
            time.sleep(2)

        browser.close()

    return jobs


# ------------------ FUTURE PORTALS (STRUCTURE READY) ------------------ #
# ------------------ REMOTEOK ------------------ #
def scrape_remoteok(role, max_jobs=50):
    jobs = []

    with sync_playwright() as p:
        browser, page = launch_browser(p)

        url = f"https://remoteok.com/remote-{role.replace(' ', '-')}-jobs"
        print(f"\nOpening RemoteOK: {url}")

        page.goto(url)
        page.wait_for_timeout(5000)

        cards = page.locator("tr.job")
        count = cards.count()

        print("RemoteOK jobs:", count)

        for i in range(min(count, max_jobs)):
            job = cards.nth(i)

            try:
                title = job.locator("h2").inner_text()
            except:
                title = "N/A"

            try:
                company = job.locator("h3").inner_text()
            except:
                company = "N/A"

            try:
                link = job.locator("a").first.get_attribute("href")
                link = "https://remoteok.com" + link if link else "N/A"
            except:
                link = "N/A"

            jobs.append({
                "title": title,
                "company": company,
                "location": "Remote",
                "link": link,
                "source": "RemoteOK"
            })

        browser.close()

    return jobs


# ------------------ WEWORKREMOTELY ------------------ #
def scrape_weworkremotely(role, max_jobs=50):
    jobs = []

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser, page = launch_browser(p)

        try:
            url = f"https://weworkremotely.com/remote-jobs/search?term={role}"
            print(f"\nOpening WWR: {url}")

            page.goto(url, timeout=60000)  # ⬅️ increase timeout
            page.wait_for_timeout(5000)

            cards = page.locator("section.jobs article")
            count = cards.count()

            print("WWR jobs found:", count)

            for i in range(min(count, max_jobs)):
                job = cards.nth(i)

                try:
                    title = job.locator("span.title").inner_text()
                except:
                    title = "N/A"

                try:
                    company = job.locator("span.company").inner_text()
                except:
                    company = "N/A"

                try:
                    link = job.locator("a").get_attribute("href")
                    if link:
                        link = "https://weworkremotely.com" + link
                    else:
                        link = "N/A"
                except:
                    link = "N/A"

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": "Remote",
                    "link": link,
                    "source": "WWR"
                })

        except Exception as e:
            print("⚠️ WWR failed:", str(e))

        finally:
            browser.close()

    return jobs


# ------------------ WELLFOUND (ANGELLIST) ------------------ #
def scrape_wellfound(role, max_jobs=50):
    jobs = []

    with sync_playwright() as p:
        browser, page = launch_browser(p)

        url = f"https://wellfound.com/jobs"
        print(f"\nOpening Wellfound: {url}")

        page.goto(url)
        page.wait_for_timeout(6000)

        cards = page.locator("div[data-testid='job-list-item']")
        count = cards.count()

        print("Wellfound jobs:", count)

        for i in range(min(count, max_jobs)):
            job = cards.nth(i)

            try:
                title = job.locator("h3").inner_text()
            except:
                title = "N/A"

            try:
                company = job.locator("h4").inner_text()
            except:
                company = "N/A"

            jobs.append({
                "title": title,
                "company": company,
                "location": "Startup",
                "link": "https://wellfound.com",
                "source": "Wellfound"
            })

        browser.close()

    return jobs


# ------------------ INTERNSHALA ------------------ #
def scrape_internshala(role, max_jobs=50):
    jobs = []

    with sync_playwright() as p:
        browser, page = launch_browser(p)

        url = f"https://internshala.com/jobs/{role.replace(' ', '-')}-jobs"
        print(f"\nOpening Internshala: {url}")

        page.goto(url)
        page.wait_for_timeout(5000)

        cards = page.locator(".individual_internship")
        count = cards.count()

        print("Internshala jobs:", count)

        for i in range(min(count, max_jobs)):
            job = cards.nth(i)

            try:
                title = job.locator(".job-internship-name").inner_text()
            except:
                title = "N/A"

            try:
                company = job.locator(".company-name").inner_text()
            except:
                company = "N/A"

            try:
                location_text = job.locator(".locations").inner_text()
            except:
                location_text = "India"

            jobs.append({
                "title": title,
                "company": company,
                "location": location_text,
                "link": "https://internshala.com",
                "source": "Internshala"
            })

        browser.close()

    return jobs


# ------------------ CUTSHORT ------------------ #
def scrape_cutshort(role, location, max_jobs=50):
    jobs = []

    with sync_playwright() as p:
        browser, page = launch_browser(p)

        url = f"https://cutshort.io/jobs/{role.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"
        print(f"\nOpening Cutshort: {url}")

        page.goto(url)
        page.wait_for_timeout(6000)

        cards = page.locator(".job-card")
        count = cards.count()

        print("Cutshort jobs:", count)

        for i in range(min(count, max_jobs)):
            job = cards.nth(i)

            try:
                title = job.locator("h3").inner_text()
            except:
                title = "N/A"

            try:
                company = job.locator(".company-name").inner_text()
            except:
                company = "N/A"

            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "link": "https://cutshort.io",
                "source": "Cutshort"
            })

        browser.close()

    return jobs


# ------------------ MAIN ------------------ #
def scrape_all(role, location, max_jobs=100):
    print("\n🚀 Multi-Platform Scraper Starting...\n")

    all_jobs = []

    all_jobs += scrape_naukri(role, location, max_jobs)
    all_jobs += scrape_remoteok(role)
    all_jobs += scrape_weworkremotely(role)
    all_jobs += scrape_wellfound(role)
    all_jobs += scrape_internshala(role)
    all_jobs += scrape_cutshort(role, location)

    print(f"\n✅ Total Jobs Collected: {len(all_jobs)}")

    return all_jobs