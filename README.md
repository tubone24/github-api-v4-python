# github-api-v4-python

Aggregate PR to the master branch and output the release results in CSV format.

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





