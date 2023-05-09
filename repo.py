import requests
from datetime import datetime, timedelta

# Your PAT goes here
token = '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'

headers = {
    'Authorization': f'token {token}',
}

# Calculate the date one year ago
one_year_ago = (datetime.now() - timedelta(days=365)).isoformat()

# The GitHub API url for searching repositories
url = f'https://api.github.com/search/repositories?q=created:>{one_year_ago}'

response = requests.get(url, headers=headers)

# Check rate limit info
rate_limit_info = response.headers
print('Limit: ', rate_limit_info['X-RateLimit-Limit'])
print('Remaining: ', rate_limit_info['X-RateLimit-Remaining'])
print('Reset: ', rate_limit_info['X-RateLimit-Reset'])

# The response will be a JSON object containing the search results
data = response.json()

# You can now access the data in the response. For example, to print the names of all the repositories:
for item in data['items']:
    print(item['name'])
