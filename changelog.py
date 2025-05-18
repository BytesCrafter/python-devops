# ===============================================================================
# Script Name : changelog.py
# Author      : BytesCrafter
# Created On  : 2025-05-18
# Version     : 1.0.0
# Purpose     : Compare closed GitHub issues / pulls between 'develop' and 'release' branches
#               to identify changes not yet released then generate a changelog.md.
# ===============================================================================

import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
import re
import json
import requests
import openai
from openai import OpenAI

assistant = os.getenv("ASSISTANT_NAME", "PEASANT")
print(f"{assistant}: CHANGELOG generation is initializing...")

project_name = os.getenv("RELEASE_NAME")
project_path = os.getenv("PROJECT_PATH")

compare_base = os.getenv("GITHUB_COMPARED_BASE", "release")
compare_head = os.getenv("GITHUB_COMPARED_HEAD", "develop")
date_since = os.getenv("GITHUB_SCAN_DATE_SINCE", "2025-01-01")

changelog_openai_summarize = os.getenv("CHANGELOG_OPENAI_SUMMARIZE", False).lower() == 'true'
openai_summarize_pretext = os.getenv("OPENAI_SUMMARIZE")

changelog_openai_title = os.getenv("CHANGELOG_ITEM_OPENAI_TITLE", False).lower() == 'true'
changelog_openai_special_note = os.getenv("CHANGELOG_NOTE_OPENAI_GENERATE", False).lower() == 'true'
changelog_openai_note_instructions = os.getenv("OPENAI_NOTE_INSTRUCTIONS")
changelog_special_note = os.getenv("CHANGELOG_SPECIAL_NOTE")
changelog_with_time = os.getenv("CHANGELOG_ITEM_WITH_TIME", False).lower() == 'true'

sanitization_pattern = os.getenv("CHANGELOG_SANITIZATION_PATTERN")
github_target = os.getenv("GITHUB_TARGET")

# Replace with the version and release date.
release_version = os.getenv("RELEASE_VERSION")
release_date = os.getenv("RELEASE_DATE")
milestone_number = os.getenv("MILESTONE_NUMBER")

# Replace these with your actual repository details
owner = os.getenv("GITHUB_OWNER")
repo = os.getenv("GITHUB_REPO")
token = os.getenv("GITHUB_TOKEN")

# Manual possible PR/Commit words to check and set it Category.
check_added = ["add", "added", "new", "introduce", "introduced", "implement", "implemented", "create", "created", "build", "built", "feature", "enhance", "enhanced", "launch", "launched", "extend", "extended", "support", "supported"]
check_changed = ["update", "updated", "modify", "modified", "refactor", "refactored", "improve", "improved", "revise", "revised", "change", "changed", "tweak", "tweaked", "adjustment", "adjusted", "optimize", "optimized", "enhance", "enhanced"]
check_fixed = ["fix", "fixed", "resolve", "resolved", "bug", "bugs", "issue", "issues", "patch", "patched", "correct", "corrected", "repair", "repaired", "hotfix", "hotfixes", "bugfix", "bugfixes", "closes", "closed", "prevent", "prevented", "trivial"]
check_removed = ["remove", "removed", "deprecate", "deprecated", "delete", "deleted", "drop", "dropped", "purge", "purged", "eliminate", "eliminated", "discard", "discarded", "retire", "retired", "outdated", "unused", "unnecessary"]

# To store all pull requests
all_repo_items = {
    "Added": [],
    "Changed": [],
    "Fixed": [],
    "Removed": [],
    "Other": []  # For items that don't match any of the categories
}

# GitHub API endpoint to get pull requests
pull_request_url = f'https://api.github.com/repos/{owner}/{repo}/pulls?state=all&base=release&head=develop'
issues_url = f'https://api.github.com/repos/{owner}/{repo}/issues?state=closed'
commits_url = f'https://api.github.com/repos/{owner}/{repo}/compare/{compare_base}...{compare_head}'

headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json',
}

# Initialize OpenAI client with your API key
client = OpenAI(api_key=os.getenv("OPENAI_TOKEN"))

# Make an API call using the chat completions endpoint
def send_chat(prompt, instructions, response_only = True):
    response = client.chat.completions.create(
        model = "gpt-4",  # Specify the chat model you want to use
        messages = [
            {"role": "system", "content": instructions},
            {"role": "user", "content": prompt}
        ],
        max_tokens = 500,  # Limit the response length
        temperature = 0.7  # Control creativity/randomness of the responses
    )

    if response_only:
        return response.choices[0].message.content
    else:
        return response

# Function to categorize PR based on title
def categorize_items(item_title):
    item_title = item_title.lower()

    # Check for "Added" keywords
    if any(keyword in item_title for keyword in check_added):
        return "Added"
    
    # Check for "Changed" keywords
    elif any(keyword in item_title for keyword in check_changed):
        return "Changed"
    
    # Check for "Fixed" keywords
    elif any(keyword in item_title for keyword in check_fixed):
        return "Fixed"
    
    # Check for "Removed" keywords
    elif any(keyword in item_title for keyword in check_removed):
        return "Removed"
    
    # Default to "Added" if no match
    return "Other"

# Function to fetch closed Pull requests
def fetch_pulls():
    # Set up initial pagination variables
    page = 1
    per_page = 100  # You can increase this number to retrieve more PRs per page

    while True:
        # Fetch pull requests with pagination
        response = requests.get(f"{pull_request_url}&page={page}&per_page={per_page}", headers=headers)

        if response.status_code == 200:
            pr_data = response.json()

            # If there are no more PRs, break the loop
            if not pr_data:
                break

            print(f"{assistant}: Fetching the pulls from github server...")

            # Append the data to all_repo_items
            for pulls in pr_data:
                pulls['title'] = re.sub(sanitization_pattern, '', pulls['title'])
                if pulls['title'].startswith(':'):
                    pulls['title'] = pulls['title'][1:]
                if pulls['title'].startswith('-'):
                    pulls['title'] = pulls['title'][1:]
                if pulls['title'].startswith(' '):
                    pulls['title'] = pulls['title'][1:]

                if changelog_openai_title:
                    print(f"{assistant}: Revising and correcting the pulls title...")
                    pulls['title'] = send_chat(os.getenv("OPENAI_PRETEXT") + pulls['title'], os.getenv("OPENAI_INSTRUCTIONS"))
                    print(f"{assistant}: OPENAI REVISION - " + pulls['title'])
                else:
                    pulls['title'] = pulls['title']
                    print(f"{assistant}: Writing pulls - " + pulls['title'])

                category = categorize_items(pulls['title'])
                all_repo_items[category].append(pr)

            # Move to the next page
            page += 1
        else:
            print(f"Failed to fetch pulls: {response.status_code}")
            break

# Function to fetch closed issues for a specific branch
def fetch_issues():
    # Set up initial pagination variables
    page = 1
    per_page = 100  # You can increase this number to retrieve more issue per page
    issues = []

    while True:
        # Fetch pull requests with pagination
        response = requests.get(f"{issues_url}&page={page}&per_page={per_page}&since={date_since}T00:00:00Z", headers=headers)

        if response.status_code == 200:
            issue_data = response.json()

            # If there are no more Issues, break the loop
            if not issue_data:
                break

            print(f"{assistant}: Fetching the {len(issue_data)} issues from github server...")

            # Append the data to all_repo_items
            for issue in issue_data:
                issue['title'] = re.sub(sanitization_pattern, '', issue['title'])
                if issue['title'].startswith(':'):
                    issue['title'] = issue['title'][1:]
                if issue['title'].startswith('-'):
                    issue['title'] = issue['title'][1:]
                if issue['title'].startswith(' '):
                    issue['title'] = issue['title'][1:]

                if f"https://github.com/{owner}/{repo}/pull/{issue['number']}" != issue['html_url']:
                    issues.append(issue)

                if changelog_openai_title:
                    print(f"{assistant}: Revising and correcting the issues title...")
                    issue['title'] = send_chat(os.getenv("OPENAI_PRETEXT") + issue['title'], os.getenv("OPENAI_INSTRUCTIONS"))
                    print(f"{assistant}: OPENAI REVISION - " + issue['title'])
                else:
                    issue['title'] = issue['title']
                    print(f"{assistant}: Writing issues - " + issue['title'])

            # Move to the next page
            page += 1
        else:
            print(f"Failed to fetch issues: {response.status_code}")
            break

    return issues

# Function to fetch commits for a specific branch
def fetch_issues_from_commits():
    # Set up initial pagination variables
    page = 1
    per_page = 100  # You can increase this number to retrieve more commits per page
    issue_numbers = []

    while True:
        # Fetch pull requests with pagination (ensure `commits_url` is defined)
        response = requests.get(f"{commits_url}?page={page}&per_page={per_page}", headers=headers)

        if response.status_code == 200:
            commit_data = response.json()

            # Extract commit titles (modify this part if needed based on actual commit data structure)
            commit_titles = [commit['commit']['message'] for commit in commit_data['commits']]

            # List to hold issue IDs for this page
            page_issues = []

            # Loop through commit titles and extract issue IDs using regex
            for c_title in commit_titles:
                issue_ids = re.findall(r'#(\d+)', c_title)  # Extract issue IDs with regex
                for issue_id in issue_ids:  # Check each issue_id extracted
                    if issue_id not in page_issues:  # Avoid adding duplicates for this page
                        page_issues.append(issue_id)

            # If no more issues, exit the loop
            if not page_issues:
                break

            # Ensure unique issue IDs in the overall list
            for page_issue_id in page_issues:
                if page_issue_id not in issue_numbers:
                    issue_numbers.append(page_issue_id)

            # Move to the next page
            page += 1
        else:
            print(f"Failed to fetch commits: {response.status_code}")
            break
    return issue_numbers

if github_target == "issues":
    # Fetch closed issues for with start date.
    issue_lists = fetch_issues() or []
    print(f"{assistant}: Fetched issue total numbers: ", len(issue_lists))    

    # Get the list of issue number from commits.
    issue_numbers = fetch_issues_from_commits()
    print(f"{assistant}: Fetched issue from commits: ", len(issue_numbers))

    # Now filter out the relevant issues
    final_issues = []
    for issue in issue_lists:
        if str(issue["number"]) in issue_numbers:
            final_issues.append(issue)

    # Compile the issues diff to all issues.
    for issue in final_issues:
        category = categorize_items(issue["title"])
        all_repo_items[category].append(issue)
else:
    fetch_pulls()

print(f"{assistant}: Completed processing items from server.")

# Calculate the path two directories back
log_path = os.path.join(project_path, "CHANGELOG.md")

# Proceed with writing the changelog if pull requests were fetched
if any(all_repo_items.values()):
    changelog_content = f"# {project_name}\n\n"
    changelog_content += "All notable changes to this project will be documented in this file.\n\n"
    changelog_content += "The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).\n\n"
    changelog_content += f"### {release_version} - {release_date} Release \n\n"

    print(f"{assistant}: Categorizing the CHANGELOG items to Added, Changed, Fixed, and Removed.")

    # Group PRs into categories and add to the changelog
    for category in ["Added", "Changed", "Fixed", "Removed", "Other"]:
        changelog_content += f"### {category} \n\n"
        for repo_item in all_repo_items[category]:
            item_title = repo_item['title']
            item_number = repo_item['number']
            item_user = repo_item['user']['login']
            item_date = repo_item['closed_at']
            item_url = repo_item['html_url']
            user_url = f"https://github.com/{item_user}"
    
            # Convert the closed_at date to datetime and format it
            closed_date = datetime.strptime(item_date, "%Y-%m-%dT%H:%M:%SZ")

            if changelog_with_time:
                formatted_date = closed_date.strftime("%Y-%m-%d %I:%M %p")
            else:
                formatted_date = closed_date.strftime("%Y-%m-%d")

            pre_text = f" [#{item_number}]({item_url}) - "

            # Adding the item number as a markdown link and formatted date
            changelog_content += f"-{pre_text} {item_title} by [{item_user}]({user_url}) (Closed on {formatted_date})\n"

    print(f"{assistant}: Finalizing the CHANGELOG footer for special notes and contributors.")

    # Add the footer of the file.
    changelog_content += "## Special Notes\n\n"
    if changelog_openai_special_note:
        special_note_generated = send_chat(changelog_openai_note_instructions + changelog_content, os.getenv("OPENAI_INSTRUCTIONS"))
        changelog_content += special_note_generated
        print(f"{assistant}: SPECIAL NOTE GENERATED - " + special_note_generated)
    else:
        changelog_content += "{changelog_special_note}"

    if changelog_openai_summarize:
        changelog_content = send_chat(openai_summarize_pretext + changelog_content, os.getenv("OPENAI_INSTRUCTIONS"))
    
    # Collect unique contributors from issues
    contributors = set()
    for category in all_repo_items.values():
        for item in category:
            if 'user' in item:
                contributors.add((item['user']['login'], item['user']['html_url']))
    
    changelog_content += "\n\nSpecial thanks to the development team"
    if contributors:
        changelog_content += ": "
        changelog_content += ", ".join(
            f"[@{login}]({url})"
            for login, url in sorted(contributors)
        )
    changelog_content += "! 💯🥳\n"

    # Write to CHANGELOG file with UTF-8 encoding
    with open(log_path, "w", encoding="utf-8") as file:
        file.write(changelog_content)
    
    print(f"{assistant}: Changelog written to {log_path}")
else:
    print(f"{assistant}: No {github_target} found or failed to fetch them.")