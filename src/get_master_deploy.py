import requests
import json

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), "../.env")
load_dotenv(dotenv_path)

TOKEN = os.environ.get("TOKEN") # 環境変数の値をAPに代入

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
    tests = [
        get_master_pr
    ]
    for i, test in enumerate(tests):
        res = post(test)
        print('{}'.format(json.dumps(res)))


if __name__ == '__main__':
    main()
