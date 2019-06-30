import requests
from datetime import datetime, timedelta


def get_last_weak_date():
    now = datetime.now()
    delta = timedelta(days=6)
    last_weak = datetime.strftime(now-delta, "%Y-%m-%d")
    return last_weak


def get_trending_repositories(top_size, last_weak):
    payload = {"q": "created:>={}".format(last_weak), "sort": "stars"}
    query = "https://api.github.com/search/repositories"
    trending_repositories = requests.get(query, params=payload).json()["items"][:top_size]
    return trending_repositories


def get_open_issues_amount(repo_owner, repo_name):
    query = "https://api.github.com/repos/{}/{}/issues"
    issues_amount = len(requests.get(query.format(repo_owner, repo_name)).json())
    return issues_amount


def show(repo_url, issues_amount):
    print(repo_url, "- {} issues".format(issues_amount))


if __name__ == "__main__":
    top_size = 20
    last_weak = get_last_weak_date()
    trending_repositories = get_trending_repositories(top_size, last_weak)
    print("Interesting repositories and their issues amount:")

    for repo in trending_repositories:
        repo_owner, repo_name = repo["full_name"].split("/")
        issues_amount = get_open_issues_amount(repo_owner, repo_name)
        repo_url = repo["html_url"]
        show(repo_url, issues_amount)
