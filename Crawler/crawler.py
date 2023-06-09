import requests
from datetime import datetime, timedelta
import time
import urllib
import json
import os
from pymongo import MongoClient

# Connect to the MongoDB, change the connection string per your MongoDB environment
client = MongoClient(port=27017)
# Set the db object to point to the business database
db = client.github

# Access the token from the environment variable
# token = os.environ.get('GITHUB_TOKEN')
token = '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'
headers = {
    'Authorization': f'token {token}',
}

# Calculate the date one year ago
one_year_ago = datetime.now() - timedelta(days=365)

# Create a list to store the repository data
repository_data = []
file_counter = 1

# Loop over each day in the last year
for day in range(365):
    start_date = one_year_ago + timedelta(days=day)
    end_date = start_date + timedelta(days=1)
    start_date_str = start_date.isoformat()
    end_date_str = end_date.isoformat()
    url = f'https://api.github.com/search/repositories?q=created:{start_date_str}..{end_date_str}&per_page=100'

    while url:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Request failed with status code {response.status_code}")
            break

        data = response.json()
        print('data', data)

        if 'items' in data:
            for item in data['items']:
                repo_name = item['full_name']
                default_branch = item['default_branch']

                page = 1
                num_commits = 0
                while True:
                    commits_url = f'https://api.github.com/repos/{repo_name}/commits?sha={default_branch}&page={page}&per_page=100'
                    commits_response = requests.get(
                        commits_url, headers=headers)
                    commits_data = commits_response.json()

                    if not commits_data:
                        break

                    num_commits += len(commits_data)
                    page += 1

                # Check if the repository has a 'tests' or 'test' directory
                contents_url = f'https://api.github.com/repos/{repo_name}/contents'
                contents_response = requests.get(contents_url, headers=headers)
                contents_data = contents_response.json()
                has_tests = 0
                if isinstance(contents_data, list) and any(content['name'].lower() in {'tests', 'test'} for content in contents_data):
                    has_tests = 1

                # Check if the repository has a CI/CD workflow
                workflows_url = f'https://api.github.com/repos/{repo_name}/actions/workflows'
                workflows_response = requests.get(
                    workflows_url, headers=headers)
                workflows_data = workflows_response.json()
                has_ci_cd = 0
                if any('ci' in workflow['name'].lower() or 'cd' in workflow['name'].lower() for workflow in workflows_data.get('workflows', [])):
                    has_ci_cd = 1

                language = item['language']
                repository_data.append({
                    'name': repo_name,
                    'language': language,
                    'commits': num_commits,
                    'has_tests': has_tests,
                    'has_ci_cd': has_ci_cd
                })

                if len(repository_data) == 30:
                    for i in range(len(repository_data)):
                        for key in repository_data[i]:
                            if repository_data[i][key] == 'null':
                                repository_data[i][key] = None

                    # insert the data into the repository collection
                    db.repository.insert_many(repository_data)

                    # clear the repository_data list
                    repository_data.clear()

        if 'Link' in response.headers:
            links = response.headers['Link'].split(', ')
            url = None
            for link in links:
                if 'rel="next"' in link:
                    url = link[link.index('<') + 1:link.index('>')]
        else:
            url = None

        if 'X-RateLimit-Remaining' in response.headers and int(response.headers['X-RateLimit-Remaining']) == 0:
            reset_time = datetime.fromtimestamp(
                int(response.headers['X-RateLimit-Reset']))
            # Add a 1 second buffer
            sleep_time = (reset_time - datetime.now()).total_seconds() + 1
            print(f'Rate limit exceeded. Sleeping for {sleep_time} seconds.')
            time.sleep(sleep_time)

# If there are fewer than 100 repositories in the last batch, write them to a file
if repository_data:
    with open(f'repository_data_{file_counter}.json', 'w') as f:
        json.dump(repository_data, f)