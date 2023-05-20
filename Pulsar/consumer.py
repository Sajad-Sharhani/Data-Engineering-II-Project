import requests
from pymongo import MongoClient
import pulsar
from pulsar.schema import AvroSchema

# Define the schema for the repository data


class RepoData(AvroSchema):
    name: str
    language: str
    default_branch: str


def consumer():
    # Connect to the Pulsar server
    client = pulsar.Client('pulsar://localhost:6650')
    consumer = client.subscribe(
        topic='persistent://sample/standalone/github_repositories',
        subscription_name='repo_analyzer',
        schema=RepoData)

    # Connect to MongoDB
    mongo_client = MongoClient(port=27017)
    db = mongo_client.github

    headers = {
        'Authorization': f'token {token}',
    }

    repository_data = []

    while True:
        msg = consumer.receive()
        repo_data = msg.value()
        consumer.acknowledge(msg)

        # Count the commits for the repo
        page = 1
        num_commits = 0
        while True:
            commits_url = f'https://api.github.com/repos/%7Brepo_data.name%7D/commits?sha={repo_data.default_branch}&page={page}&per_page=100'
            commits_response = requests.get(commits_url, headers=headers)
            commits_data = commits_response.json()

            if not commits_data:
                break

            num_commits += len(commits_data)
            page += 1

            # Check if the repository has a 'tests' or 'test' directory
        contents_url = f'https://api.github.com/repos/%7Brepo_data.name%7D/contents'
        contents_response = requests.get(contents_url, headers=headers)
        contents_data = contents_response.json()
        has_tests = 0
        if isinstance(contents_data, list) and any(content['name'].lower() in {'tests', 'test'} for content in contents_data):
            has_tests = 1

        # Check if the repository has a CI/CD workflow
        workflows_url = f'https://api.github.com/repos/%7Brepo_data.name%7D/actions/workflows'
        workflows_response = requests.get(workflows_url, headers=headers)
        workflows_data = workflows_response.json()
        has_ci_cd = 0
        if any('ci' in workflow['name'].lower() or 'cd' in workflow['name'].lower() for workflow in workflows_data.get('workflows', [])):
            has_ci_cd = 1

        # Append to the repository_data list
        repository_data.append({
            'name': repo_data.name,
            'language': repo_data.language,
            'commits': num_commits,
            'has_tests': has_tests,
            'has_ci_cd': has_ci_cd
        })

        # If repository_data has 30 items, insert them into MongoDB and clear the list
        if len(repository_data) == 30:
            db.repository.insert_many(repository_data)
            repository_data.clear()

    client.close()


if __name__ == "main":
    # Access the token from the environment variable
    token = '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'
    consumer()
