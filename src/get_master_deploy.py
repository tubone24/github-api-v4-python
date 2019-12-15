import requests
import json

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), "../.env")
load_dotenv(dotenv_path)

TOKEN = os.environ.get("TOKEN")  # 環境変数の値をAPに代入

# token
token = TOKEN

# endpoint
endpoint = 'https://api.github.com/graphql'

get_master_pr = {"query": """
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


def main():
    res = post(get_master_pr)
    # print('{}'.format(json.dumps(res)))
    for node in res["data"]["search"]["edges"]:
        repo_name = node["node"]["name"]
        repo_url = node["node"]["url"]
        pr_count = 0
        for pr in node["node"]["pullRequests"]["edges"]:
            base_ref_name = pr["node"]["baseRefName"]
            if base_ref_name != "master":
                continue
            head_ref_name = pr["node"]["headRefName"]
            created_at = pr["node"]["createdAt"]
            if pr["node"]["merged"]:
                pr_count += 1
                merged_at = pr["node"]["mergedAt"]
                merged_by = pr["node"]["mergedBy"]["login"]
                pr_title = pr["node"]["title"]
                pr_url = pr["node"]["url"]
                if pr_count == 1:
                    print("\n")
                    print("{repo_name}:  {repo_url}".format(repo_name=repo_name, repo_url=repo_url))
                print("  #{pr_count} {pr_title} for {head_ref_name} by {merged_by} at {merged_at}".format(pr_count=pr_count, pr_title=pr_title, head_ref_name=head_ref_name, merged_by=merged_by, merged_at=merged_at))
                print("        {pr_url}".format(pr_url=pr_url))


if __name__ == '__main__':
    main()
