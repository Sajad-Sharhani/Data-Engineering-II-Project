import requests
import time
import re

# Your PAT goes here
token = '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'

headers = {
    'Authorization': f'token {token}',
}

# Initial GitHub API url for searching repositories
url = 'https://api.github.com/search/repositories?q=created:>2023-01-01&sort=updated&order=desc&per_page=100'

def check_rate_limit(response):
    remaining = int(response.headers['X-RateLimit-Remaining'])
    reset_time = int(response.headers['X-RateLimit-Reset'])

    if remaining <= 10:
        sleep_duration = reset_time - int(time.time()) + 10  # Add a buffer of 10 seconds
        print(f'Sleeping for {sleep_duration} seconds to avoid hitting the rate limit...')
        time.sleep(sleep_duration)

# Create a dictionary to count the occurrences of each language
language_counts = {}

while url:
    response = requests.get(url, headers=headers)

    # Extract the next page URL from the Link header, if it exists
    link_header = response.headers.get('Link')
    if link_header:
        match = re.search(r'<(https://api.github.com/.*?)>; rel="next"', link_header)
        url = match.group(1) if match else None
    else:
        url = None

    # Check the rate limit after each search request
    check_rate_limit(response)

    # The response will be a JSON object containing the search results
    data = response.json()

    # Check if 'items' key exists in the response data
    if 'items' in data:
        # Loop over each repository in the results
        for item in data['items']:
            # Get the repository's name and owner
            repo_name = item['full_name']

            # Get the contents of the root directory for this repository
            contents_url = f'https://api.github.com/repos/{repo_name}/contents'
            contents_response = requests.get(contents_url, headers=headers)
            contents_data = contents_response.json()

            # Check the rate limit after each request for contents
            check_rate_limit(contents_response)

            # If the response is a list, check if there's a 'tests' or 'test' directory
            if isinstance(contents_data, list) and any(content['name'].lower() in {'tests', 'test'} for content in contents_data):
                # Get the repository's primary language
                language = item['language']

                # If the language is not None, increment its count in the dictionary
                if language is not None:
                    if language in language_counts:
                        language_counts[language] += 1
                    else:
                        language_counts[language] = 1

                # If we have found 100 repositories with a 'tests' or 'test' directory, exit the loop
                if sum(language_counts.values()) >= 10:
                    url = None
                    break
                    
    # Sleep for a short time to avoid hitting the rate limit
    time.sleep(2)

# After all requests are done, print the top 10 languages
top_languages = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)[:10]
for language, count in top_languages:
    print(f'{language}: {count} repositories')
