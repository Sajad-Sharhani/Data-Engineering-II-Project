import requests
from datetime import datetime, timedelta
import time
import urllib

# Your PAT goes here
token = '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'

headers = {
    'Authorization': f'token {token}',
}

# Calculate the date one year ago
one_year_ago = datetime.now() - timedelta(days=365)

# Create a dictionary to count the occurrences of each language
language_counts = {}

# Loop over each day in the last year
for day in range(1):  # We're now only looping over one day to reduce the number of requests
    # Calculate the start and end dates for this day
    start_date = one_year_ago + timedelta(days=day)
    end_date = start_date + timedelta(days=1)

    # Format the dates as strings in the format expected by the GitHub API
    start_date_str = start_date.isoformat()
    end_date_str = end_date.isoformat()

    # The GitHub API url for searching repositories
    url = f'https://api.github.com/search/repositories?q=created:{start_date_str}..{end_date_str}&per_page=100'

    while url:
        response = requests.get(url, headers=headers)

        # Check the status code of the response
        if response.status_code != 200:
            print(f"Request failed with status code {response.status_code}")
            break
        else:
            # The response will be a JSON object containing the search results
            data = response.json()

            # Check if 'items' key exists in the response data
            if 'items' in data:
                # Loop over each repository in the results
                for item in data['items']:
                    # Get the repository's primary language
                    language = item['language']

                    # If the language is not None, increment its count in the dictionary
                    if language is not None:
                        if language in language_counts:
                            language_counts[language] += 1
                        else:
                            language_counts[language] = 1
            else:
                print("No 'items' key in the response. Response data: ", data)

        if 'Link' in response.headers:
            links = response.headers['Link'].split(', ')
            url = None
            for link in links:
                if 'rel="next"' in link:
                    url = link[link.index('<') + 1:link.index('>')]
        else:
            url = None

        # Check rate limit headers and sleep if necessary
        if 'X-RateLimit-Remaining' in response.headers and int(response.headers['X-RateLimit-Remaining']) == 0:
            reset_time = datetime.fromtimestamp(int(response.headers['X-RateLimit-Reset']))
            sleep_time = (reset_time - datetime.now()).total_seconds() + 1  # Add a 1 second buffer
            print(f'Rate limit exceeded. Sleeping for {sleep_time} seconds.')
            time.sleep(sleep_time)

# After all requests are done, print the top 10 languages
top_languages = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)[:10]
for language, count in top_languages:
    print(f'{language}: {count} repositories')
