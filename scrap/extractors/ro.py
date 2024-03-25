import requests
from bs4 import BeautifulSoup

def extract_ro_jobs(keyword):
    url = f"https://remoteok.com/remote-{keyword}-jobs"
    request = requests.get(url, headers={"User-Agent": "Kimchi"})
    if request.status_code != 200:
        print("Can't request website")
    else:
        results = []
        soup = BeautifulSoup(request.text, "html.parser")
        jobs = soup.find_all("tr", class_="job")
        for job_section in jobs:
            job_posts = job_section.find_all("td", class_="company_and_position")
            for post in job_posts:
                anchor = post.select_one("a")
                link = anchor['href']
                title = post.find("h2")
                company = post.find("h3")
                locations = post.find_all("div", class_="location")
                location = locations[0]
                salary = locations[-1]
                job_data = {
                    "link": f"https://remoteok.com{link}",
                    "title": (title.string).strip().replace(",", " "),
                    "company": (company.string).strip().replace(",", " "),
                    "location": (location.string).strip().replace(",", " "),
                    "note": (salary.string).strip().replace(",", " "),
                }
                results.append(job_data)
        return results