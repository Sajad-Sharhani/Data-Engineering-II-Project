import requests
from datetime import datetime, timedelta
import time

# Your PAT goes here
token = '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'

headers = {
    'Authorization': f'token {token}',
}

# Calculate the date one year ago
one_year_ago = datetime.now() - timedelta(days=365)

# Loop over each day in the last year
for day in range(1):
    # Calculate the start and end dates for this day
    start_date = one_year_ago + timedelta(days=day)
    end_date = start_date + timedelta(days=1)

    # Format the dates as strings in the format expected by the GitHub API
    start_date_str = start_date.isoformat()
    end_date_str = end_date.isoformat()

    # The GitHub API url for searching repositories
    url = f'https://api.github.com/search/repositories?q=created:{start_date_str}..{end_date_str}'

    response = requests.get(url, headers=headers)

    # Check the status code of the response
    if response.status_code != 200:
        print(f"Request failed with status code {response.status_code}")
    else:
        # Check rate limit info
        rate_limit_info = response.headers
        print('Limit: ', rate_limit_info['X-RateLimit-Limit'])
        print('Remaining: ', rate_limit_info['X-RateLimit-Remaining'])
        print('Reset: ', rate_limit_info['X-RateLimit-Reset'])
        
        # The response will be a JSON object containing the search results
        data = response.json()

        # Check if 'items' key exists in the response data
        if 'items' in data:
            # You can now access the data in the response. For example, to print the names of all the repositories:
            for item in data['items']:
                print(item['name'])
        else:
            print("No 'items' key in the response. Response data: ", data)

    # Sleep for a short time to avoid hitting the rate limit
    time.sleep(2)
