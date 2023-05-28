from pymongo import MongoClient

client = MongoClient('192.168.2.93', 30007)  # Adjust parameters if necessary

db = client['github']  # Replace with your database name

collection = db['repository']  # Replace with your collection name

program_languages = {}
data = collection.find()

for x in data:
    if x['language'] not in program_languages:
        program_languages[f"{x['language']}"] = 1
    else:
        program_languages[f"{x['language']}"] += 1


sorted_list = sorted(program_languages.items(), key = lambda x:x[1], reverse = True)

list_length = 10


print("#Occurances\tLanguage")
print("------------------------")
for (a,b) in sorted_list[:list_length]:
    print(f"{b}\t\t{a}")

project_commits = {}
data = collection.find()

for x in data:
    if x['name'] not in project_commits:
        project_commits[f"{x['name']}"] = x['commits']

sorted_list = sorted(project_commits.items(), key = lambda x:x[1], reverse = True)

print("#Commits\tLanguage")
print("------------------------")
for (a,b) in sorted_list[:list_length]:
    print(f"{b}\t\t{a}")


test_driven = {}
data = collection.find()

for x in data:
    if x['language'] not in test_driven:
        test_driven[f"{x['language']}"] = 0
        test_driven[f"{x['language']}"] += x['has_tests']
    else:
        test_driven[f"{x['language']}"] += x['has_tests']

sorted_list = sorted(test_driven.items(), key = lambda x:x[1], reverse = True)

print("#Test Driven\tLanguage")
print("------------------------")
for (a,b) in sorted_list[:list_length]:
    print(f"{b}\t\t{a}")

test_driven_and_cicd = {}
data = collection.find()

for x in data:
    if x['language'] not in test_driven_and_cicd:
        test_driven_and_cicd[f"{x['language']}"] = 0
        
    if x['has_tests'] == 1 and x['has_ci_cd'] == 1:
        test_driven_and_cicd[f"{x['language']}"] += 1
    
sorted_list = sorted(test_driven_and_cicd.items(), key = lambda x:x[1], reverse = True)

print("#Test Driven and DevOps \tLanguage")
print("----------------------------------------")
for (a,b) in sorted_list[:list_length]:
    print(f"{b}\t\t\t\t{a}")
