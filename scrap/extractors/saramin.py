from bs4 import BeautifulSoup
import requests


def extract_saramin_jobs(keyword):
    url = f"https://www.saramin.co.kr/zf_user/search?search_area=main&search_done=y&search_optional_item=n&searchType=search&searchword={keyword}"
    request = requests.get(url, headers={"User-Agent": "Kimchi"})
    if request.status_code != 200:
        print("Can't request website")
    else:
        results = []
        soup = BeautifulSoup(request.text, "html.parser")
        jobs = soup.find_all("section", class_="section_search")
        for job_section in jobs:
            job_posts = job_section.find_all("div", class_="item_recruit")
            for post in job_posts:
                anchors = post.find_all("a")
                anchor = anchors[0]
                title = anchor["title"]
                link = anchor["href"]
                company = post.select_one("strong a")
                location = post.select_one("div span a")
                notes = post.find_all("span")
                note = notes[-5]
                job_data = {
                    'title': title.replace(",", " "),
                    'company': (company.string).strip().replace(",", " "),
                    'location': (location.string).strip().replace(",", " "),
                    'link': f"https://www.saramin.co.kr{link}".replace(",", " "),
                    'note': note.string.replace(",", " "),
                }
                results.append(job_data)
        return results
