import requests
from datetime import datetime, timedelta
import pulsar
from pulsar.schema import *

# Define the schema for the repository data


class RepoData(Record):
    name= String()
    language= String()
    default_branch= String()


def producer():
    # Connect to the Pulsar server
    client = pulsar.Client('pulsar://localhost:6650')
    producer = client.create_producer(
        topic='persistent://sample/standalone/github_repositories',
        schema=JsonSchema(RepoData))

    headers = {
        'Authorization': f'token {token}',
    }

    one_year_ago = datetime.now() - timedelta(days=365)

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
                print(
                    f"Request failed with status code {response.status_code}")
                break

            data = response.json()

            if 'items' in data:
                for item in data['items']:
                    repo_data = RepoData(
                        name=item['full_name'], language=item['language'], default_branch=item['default_branch'])
                    producer.send(repo_data)

            if 'Link' in response.headers:
                links = response.headers['Link'].split(', ')
                url = None
                for link in links:
                    if 'rel="next"' in link:
                        url = link[link.index('<') + 1:link.index('>')]
            else:
                url = None

    client.close()


if __name__ == "__main__":
    # Access the token from the environment variable
    token = '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'
    producer()
