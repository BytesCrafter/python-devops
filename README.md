# DevOps Automation Script

A Python-based automation tool to streamline development documentation, continuous integration/deployment (CI/CD), dependency checking, testing, and preparing source code for production.

## 🚀 Project Goal

To automate and standardize the DevOps workflow from documentation through deployment by:

- Generating and maintaining changelogs and documentation
- Performing automated dependency checks
- Running tests before deployment
- Ensuring source code is production-ready

## 📂 Features

- ✅ Auto-generate changelogs from merged pull requests
- ✅ Detect and report missing or outdated dependencies
- ✅ Run test suites and report failures
- ✅ Validate code readiness before deployment
- ✅ Output concise release notes for end users

## 🛠️ Requirements

- Python 3.8+
- `openai`
- `requests`
- `python-dotenv`
- OpenAI API token (stored in a `.env` file)
- GitHub API token (stored in a `.env` file)

## ⚙️ Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/BytesCrafter/python-devops.git
   cd python-devops
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file and add your GitHub and OpenAI API keys along with project-specific settings:

   ```env
   GITHUB_TOKEN=your_github_token
   OPENAI_API_KEY=your_openai_key
   PROJECT_REPO=your_org/your_repo
   ```

4. Run the script:

   ```bash
   python changelog.py
   ```

## 📄 Output

- `CHANGELOG.md` – A changelog file generated from pull requests
- Summarized release notes using OpenAI
- Console logs – Summary of test and dependency checks

## 📌 Notes

- This script is intended for use in Python-based CI/CD environments.
- Can be integrated into GitHub Actions, GitLab CI, or other pipelines.
- OpenAI is used to generate natural-language summaries of pull request activity and development changes.

## 📃 License

MIT License

---

**Author**: [BytesCrafter](@BytesCrafter)
**Contributors**: [caezariidecastro](@caezariidecastro)
