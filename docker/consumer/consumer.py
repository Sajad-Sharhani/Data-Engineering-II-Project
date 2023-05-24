import requests
from pymongo import MongoClient
import pulsar
from pulsar.schema import *
from pymongo.errors import DuplicateKeyError

# Define the schema for the repository data
class RepoData(Record):
    name = String()
    language = String()
    default_branch = String()

def consumer():
    # Connect to the Pulsar server
    client = pulsar.Client('pulsar://pulsar:6650')
    consumer = client.subscribe(
        topic='github_repositories',
        subscription_name='repo_2',
        schema=JsonSchema(RepoData))

    # Connect to MongoDB
    mongo_client = MongoClient('mongodb',27017)
    db = mongo_client.github
    db.repository.create_index('name', unique=True)

    headers = {
        'Authorization': f'token {token}',
    }

    repository_data = []

    while True:
        msg = consumer.receive()
        repo_data = msg.value()
        consumer.acknowledge(msg)
        print(repo_data)

        # Count the commits for the repo
        page = 1
        num_commits = 0
        while True:
            commits_url = f'https://api.github.com/repos/{repo_data.name}/commits?sha={repo_data.default_branch}&page={page}&per_page=100'
            commits_response = requests.get(commits_url, headers=headers)
            commits_data = commits_response.json()

            if not commits_data:
                break

            num_commits += len(commits_data)
            page += 1

        # Check if the repository has a 'tests' or 'test' directory
        contents_url = f'https://api.github.com/repos/{repo_data.name}/contents'
        contents_response = requests.get(contents_url, headers=headers)
        contents_data = contents_response.json()

        has_tests = 0
        if isinstance(contents_data, list) and any(content['name'].lower() in {'tests', 'test'} for content in contents_data):
            has_tests = 1

        # Check if the repository has a CI/CD workflow
        workflows_url = f'https://api.github.com/repos/{repo_data.name}/actions/workflows'
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

        if len(repository_data) == 30:
            print('mongo')
            print('repository_data 2', repository_data)
            for single_repo_data in repository_data:
                try:
                    # insert a single repo data
                    db.repository.insert_one(single_repo_data)
                except pymongo.errors.DuplicateKeyError as e:
                    print(f'Duplicate document found for repo {single_repo_data["name"]}. Not inserted into MongoDB.')
                    continue
            repository_data.clear()


    client.close()

if __name__ == "__main__":
    # Access the token from the environment variable.ludvig
    token ='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'
    consumer()
