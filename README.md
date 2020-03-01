# github-api-v4-python

Aggregate PR to the master branch and output the release results in CSV format.

## Background

Normally, when you release a system, there should be a release management table that summarizes the release date and release contents, such as release management, but it was troublesome because it was not organized! It was something.

However, our source is managed on GitHub, and we always follow the branch strategy of Git-flow, so if you collect PR and commit history, you can do it! It was.

## How to use

### Precondition

- Python3.6 or more.

Install dependencies.

```
pip install -r requirements.txt
```


Create environments file(dot env). 

```
touch .env
```

Set the GitHub API Tokens to `.env`.

```
TOKEN=YourGitHubToken
ENDPOINT=https://api.github.com/graphql
```

If you use Hosted GitHub Enterprise, Change ENDPOINT to yours.

## How to use

```
python get_master_deploy.py 
```

## More Information?

Read the article below.

[面倒なことはPythonにやらせよう@GitHub API v4を使ったリリース実績取得](https://blog.tubone-project24.xyz/2019/12/16/python-auto)




