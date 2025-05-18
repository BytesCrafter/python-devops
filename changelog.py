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
import requests
import openai
from openai import OpenAI

assistant = os.getenv("ASSISTANT_NAME", "PEASANT")
print(f"{assistant}: CHANGELOG generation is initializing...")

project_name = os.getenv("RELEASE_NAME")
project_path = os.getenv("PROJECT_PATH")
changelog_openai_title = os.getenv("CHANGELOG_ITEM_OPENAI_TITLE", False).lower() == 'true'
changelog_openai_special_note = os.getenv("CHANGELOG_NOTE_OPENAI_GENERATE", False).lower() == 'true'
changelog_openai_note_instructions = os.getenv("OPENAI_NOTE_INSTRUCTIONS")

changelog_with_time = os.getenv("CHANGELOG_ITEM_WITH_TIME", False).lower() == 'true'
changelog_with_pr_num = os.getenv("CHANGELOG_ITEM_WITH_PR_NUM", False).lower() == 'true'
changelog_special_note = os.getenv("CHANGELOG_SPECIAL_NOTE")

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

# To store all pull requests and contributors
all_repo_items = {
    "Added": [],
    "Changed": [],
    "Fixed": [],
    "Removed": [],
    "Other": []  # For PRs that don't match any of the categories
}
contributors = set()  # Track unique contributors

# GitHub API endpoint to get pull requests
pull_request_url = f'https://api.github.com/repos/{owner}/{repo}/pulls?state=all&base=release&head=develop'
issues_url = f'https://api.github.com/repos/{owner}/{repo}/issues?state=closed'

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
        max_tokens = 120,  # Limit the response length
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
    return "Added"

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

            print(f"{assistant}: Fetching the pull requests from github server...")

            # Append the data to all_repo_items
            for pr in pr_data:
                pr['title'] = re.sub(sanitization_pattern, '', pr['title'])
                if pr['title'].startswith(':'):
                    pr['title'] = pr['title'][1:]
                if pr['title'].startswith('-'):
                    pr['title'] = pr['title'][1:]
                if pr['title'].startswith(' '):
                    pr['title'] = pr['title'][1:]

                if changelog_openai_title:
                    print(f"{assistant}: Revising and correcting the ticket title...")
                    pr['title'] = send_chat(os.getenv("OPENAI_PRETEXT") + pr['title'], os.getenv("OPENAI_INSTRUCTIONS"))
                    print(f"{assistant}: OPENAI REVISION - " + pr['title'])
                else:
                    pr['title'] = pr['title']
                    print(f"{assistant}: Writing - " + pr['title'])

                category = categorize_items(pr['title'])
                all_repo_items[category].append(pr)
                contributors.add(pr['user']['login'])

            # Move to the next page
            page += 1
        else:
            print(f"Failed to fetch PRs: {response.status_code}")
            break

# Function to fetch closed issues for a specific branch
def fetch_issues(branch):
    # Set up initial pagination variables
    page = 1
    per_page = 100  # You can increase this number to retrieve more PRs per page
    issues = []

    while True:
        # Fetch pull requests with pagination
        response = requests.get(f"{issues_url}&page={page}&per_page={per_page}&labels={branch}", headers=headers)

        if response.status_code == 200:
            issue_data = response.json()

            # If there are no more Issues, break the loop
            if not issue_data:
                break

            print(f"{assistant}: Fetching the issues from github server...")

            # Append the data to all_repo_items
            for issue in issue_data:
                issue['title'] = re.sub(sanitization_pattern, '', issue['title'])
                if issue['title'].startswith(':'):
                    issue['title'] = issue['title'][1:]
                if issue['title'].startswith('-'):
                    issue['title'] = issue['title'][1:]
                if issue['title'].startswith(' '):
                    issue['title'] = issue['title'][1:]

                if changelog_openai_title:
                    print(f"{assistant}: Revising and correcting the ticket title...")
                    issue_title = send_chat(os.getenv("OPENAI_PRETEXT") + issue['title'], os.getenv("OPENAI_INSTRUCTIONS"))
                    print(f"{assistant}: OPENAI REVISION - " + issue_title)
                else:
                    issue_title = pr['title']
                    print(f"{assistant}: Writing - " + issue_title)

            # Move to the next page
            page += 1
        else:
            print(f"Failed to fetch PRs: {response.status_code}")
            break

if github_target == "pulls":
    fetch_pulls()
else:
    # Fetch closed issues for develop and release branches
    develop_issues = fetch_issues('develop') or []
    release_issues = fetch_issues('release') or []

    # Finding differences between the issues closed in both branches
    issues_in_develop_not_in_release = [issue for issue in develop_issues if issue not in release_issues]

    # Compile the issues diff to all issues.
    for issue in issues_in_develop_not_in_release:
        category = categorize_items(issue["title"])
        all_repo_items[category].append(issue)
        contributors.add(issue['user']['login'])

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
    for category in ["Added", "Changed", "Fixed", "Removed"]:
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

            if github_target == "pulls" and changelog_with_pr_num:
                pre_text = f" [PR #{item_number}]({item_url}):"
            else:
                pre_text = ""

            # Adding the PR number as a markdown link and formatted date
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
    changelog_content += "\n\n"
    changelog_content += "Special thanks to all contributors: "
    changelog_content += ", ".join([f"[@{login}](https://github.com/{login})" for login in sorted(contributors)])
    changelog_content += "! 💯🥳\n"

    # Write to CHANGELOG file with UTF-8 encoding
    with open(log_path, "w", encoding="utf-8") as file:
        file.write(changelog_content)
    
    print(f"{assistant}: Changelog written to {log_path}")
else:
    print(f"{assistant}: No {github_target} found or failed to fetch them.")