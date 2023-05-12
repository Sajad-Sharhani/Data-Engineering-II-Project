import requests

# Your PAT goes here
token = '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'

headers = {
    'Authorization': f'token {token}',
}

# The GitHub API url for searching repositories
url = 'https://api.github.com/search/repositories?q=created:>2023-01-01&sort=updated&order=desc&per_page=100'

response = requests.get(url, headers=headers)

# The response will be a JSON object containing the search results
data = response.json()

# Check if 'items' key exists in the response data
if 'items' in data:
    # Loop over each repository in the results
    for item in data['items']:
        # Get the repository's name and owner
        repo_name = item['full_name']
        default_branch = item['default_branch']

        # Get the number of commits for this repository's default branch
        page = 1
        num_commits = 0
        while True:
            commits_url = f'https://api.github.com/repos/{repo_name}/commits?sha={default_branch}&page={page}&per_page=100'
            commits_response = requests.get(commits_url, headers=headers)
            commits_data = commits_response.json()

            # If the response is empty, we've reached the end of the commit list
            if not commits_data:
                break

            num_commits += len(commits_data)
            page += 1

        print(f'Repository: {repo_name}, Number of Commits: {num_commits}')
