import requests
import json
import csv
import pytz
from datetime import datetime

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), "../.env")
load_dotenv(dotenv_path)

TOKEN = os.environ.get("TOKEN")
ENDPOINT = os.environ.get("ENDPOINT")

# token
token = TOKEN

# endpoint
endpoint = ENDPOINT


# If you want to search repo's in organization `org:hoge` instead of user:hoge

get_master_pr = {
    "query": """
  query {
  search(query: "user:tubone24", type: REPOSITORY, first: 100) {
      pageInfo {
      endCursor
      startCursor
    }
    edges {
      node {
        ... on Repository {
          name
          url
          pullRequests (first: 100){
            edges {
            node {
              baseRefName
              createdAt
              closedAt
              merged
              mergedAt
              mergedBy {
                login
              }
              commits (first: 45){
                nodes {
                  commit {
                    message
                  }
                }
              }
              title
              url
              headRefName
              }
            }
            }
          }
        }
    }
  }
  }
  """
}


def post(query):
    headers = {"Authorization": "bearer " + token}
    res = requests.post(endpoint, json=query, headers=headers)
    if res.status_code != 200:
        raise Exception("failed : {}".format(res.status_code))
    return res.json()


def iso_to_jst(iso_str):
    dt = None
    try:
        dt = datetime.strptime(iso_str, "%Y-%m-%dT%H:%M:%SZ")
        dt = pytz.utc.localize(dt).astimezone(pytz.timezone("Asia/Tokyo"))
    except ValueError:
        try:
            dt = datetime.strptime(iso_str, "%Y-%m-%dT%H:%M:%Sz")
            dt = dt.astimezone(pytz.timezone("Asia/Tokyo"))
        except ValueError:
            pass
    if dt is None:
        return ""
    return dt.strftime("%Y/%m/%d %H:%M:%S")


def create_csv_header():
    with open("master_pr.csv", "w", encoding="utf_8_sig") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Repository",
                "Repository URL",
                "PR#",
                "PR Title",
                "Target Branch",
                "Merged By",
                "Merged at",
                "Created at",
                "PR URL",
                "Commit Msgs",
            ]
        )


def main():
    create_csv_header()
    res = post(get_master_pr)
    print("{}".format(json.dumps(res)))
    for node in res["data"]["search"]["edges"]:
        repo_name = node["node"]["name"]
        repo_url = node["node"]["url"]
        pr_count = 0
        for pr in node["node"]["pullRequests"]["edges"]:
            base_ref_name = pr["node"]["baseRefName"]
            if base_ref_name != "master":
                continue
            head_ref_name = pr["node"]["headRefName"]
            created_at = iso_to_jst(pr["node"]["createdAt"])
            if pr["node"]["merged"]:
                pr_count += 1
                merged_at = iso_to_jst(pr["node"]["mergedAt"])
                merged_by = pr["node"]["mergedBy"]["login"]
                pr_title = pr["node"]["title"]
                pr_url = pr["node"]["url"]
                commit_list = [
                    x["commit"]["message"] for x in pr["node"]["commits"]["nodes"]
                ]
                if pr_count == 1:
                    print("\n")
                    print(
                        "{repo_name}:  {repo_url}".format(
                            repo_name=repo_name, repo_url=repo_url
                        )
                    )
                print(
                    "  #{pr_count} {pr_title} for {head_ref_name} by {merged_by} at {merged_at}".format(
                        pr_count=pr_count,
                        pr_title=pr_title,
                        head_ref_name=head_ref_name,
                        merged_by=merged_by,
                        merged_at=merged_at,
                    )
                )
                print("        {pr_url}".format(pr_url=pr_url))
                with open("master_pr.csv", "a", encoding="utf_8_sig") as f:
                    writer = csv.writer(f)
                    writer.writerow(
                        [
                            repo_name,
                            repo_url,
                            pr_count,
                            pr_title,
                            head_ref_name,
                            merged_by,
                            merged_at,
                            created_at,
                            pr_url,
                            "\n".join(commit_list),
                        ]
                    )


if __name__ == "__main__":
    main()
