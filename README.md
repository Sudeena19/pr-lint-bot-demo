PR Lint Bot



A GitHub Pull Request Linting Bot that automatically checks Python code for style, formatting, and common issues using Ruff.

It posts inline comments for critical issues and a summary comment on the PR — helping teams maintain clean and professional code.



Features



✅ Fast and efficient Python linting using RuffPR Lint Bot



A GitHub Pull Request Linting Bot that automatically checks Python code for style, formatting, and common issues using Ruff.

It posts inline comments for critical issues and a summary comment on the PR — helping teams maintain clean and professional code.



Features



✅ Fast and efficient Python linting using Ruff



✅ Inline comments for problematic lines (optional)



✅ PR summary comment for all detected issues



✅ Configurable for any Python project



✅ Fully automated with GitHub Actions



Folder Structure

pr-lint-bot/

├─ lint\_bot/

│  ├─ \_\_init\_\_.py

│  ├─ linter.py        # Runs Ruff on repo, returns issues

│  └─ github\_bot.py    # Posts inline and summary comments

├─ app.py              # Main script to run bot

├─ requirements.txt    # Python dependencies

└─ .github/workflows/

&nbsp;  └─ pr\_lint.yml      # GitHub Action workflow



Getting Started

1\. Clone the repository

git clone https://github.com/yourusername/pr-lint-bot.git

cd pr-lint-bot



2\. Set up Python environment

python -m venv venv

source venv/bin/activate      # Linux/Mac

venv\\Scripts\\activate         # Windows



pip install -r requirements.txt



3\. Configure GitHub secrets



Create a Personal Access Token with repo permissions and add it as a secret named PERSONAL\_TOKEN in your GitHub repository.



4\. Run locally (for testing)

export GITHUB\_TOKEN=your\_token           # Linux/Mac

set GITHUB\_TOKEN=your\_token              # Windows



export GITHUB\_REPOSITORY=your/repo       # Linux/Mac

set GITHUB\_REPOSITORY=your/repo          # Windows



export PR\_NUMBER=1                        # Pull Request number

set PR\_NUMBER=1                           # Windows



python app.py





The bot will lint the repository and print inline/summary comments in the PR.



5\. GitHub Actions Automation



The bot runs automatically on pull requests:



name: PR Lint Bot



on:

&nbsp; pull\_request:

&nbsp;   types: \[opened, synchronize, reopened]



jobs:

&nbsp; lint:

&nbsp;   runs-on: ubuntu-latest



&nbsp;   steps:

&nbsp;     - uses: actions/checkout@v3

&nbsp;     - uses: actions/setup-python@v4

&nbsp;       with:

&nbsp;         python-version: '3.x'

&nbsp;     - run: pip install -r requirements.txt

&nbsp;     - run: python app.py

&nbsp;       env:

&nbsp;         GITHUB\_TOKEN: ${{ secrets.PERSONAL\_TOKEN }}

&nbsp;         GITHUB\_REPOSITORY: ${{ github.repository }}

&nbsp;         PR\_NUMBER: ${{ github.event.pull\_request.number }}



Example Output

Inline comment

bad\_code.py:5: F401 - 'os' imported but unused



Summary comment

\### PR Lint Bot Summary

\- bad\_code.py:5 - F401 - 'os' imported but unused

\- test\_file.py:12 - E501 - line too long (120 > 100 characters)



Why it’s professional



Automated linting ensures consistent code quality.



Summary plus optional inline comments make PR review faster and clearer.



Easy to integrate in any Python project or CI/CD workflow.



Clean modular code structure for maintainability.



Future Improvements



Add custom rules for your team or project.



Integrate auto-fix for simple issues (like formatting).



Extend to support other languages or tools (e.g., JavaScript with ESLint).



✅ Inline comments for problematic lines (optional)



✅ PR summary comment for all detected issues



✅ Configurable for any Python project



✅ Fully automated with GitHub Actions



Folder Structure

pr-lint-bot/

├─ lint\_bot/

│  ├─ \_\_init\_\_.py

│  ├─ linter.py        # Runs Ruff on repo, returns issues

│  └─ github\_bot.py    # Posts inline and summary comments

├─ app.py              # Main script to run bot

├─ requirements.txt    # Python dependencies

└─ .github/workflows/

&nbsp;  └─ pr\_lint.yml      # GitHub Action workflow



Getting Started

1\. Clone the repository

git clone https://github.com/yourusername/pr-lint-bot.git

cd pr-lint-bot



2\. Set up Python environment

python -m venv venv

source venv/bin/activate      # Linux/Mac

venv\\Scripts\\activate         # Windows



pip install -r requirements.txt



3\. Configure GitHub secrets



Create a Personal Access Token with repo permissions and add it as a secret named PERSONAL\_TOKEN in your GitHub repository.



4\. Run locally (for testing)

export GITHUB\_TOKEN=your\_token           # Linux/Mac

set GITHUB\_TOKEN=your\_token              # Windows



export GITHUB\_REPOSITORY=your/repo       # Linux/Mac

set GITHUB\_REPOSITORY=your/repo          # Windows



export PR\_NUMBER=1                        # Pull Request number

set PR\_NUMBER=1                           # Windows



python app.py





The bot will lint the repository and print inline/summary comments in the PR.



5\. GitHub Actions Automation



The bot runs automatically on pull requests:



name: PR Lint Bot



on:

&nbsp; pull\_request:

&nbsp;   types: \[opened, synchronize, reopened]



jobs:

&nbsp; lint:

&nbsp;   runs-on: ubuntu-latest



&nbsp;   steps:

&nbsp;     - uses: actions/checkout@v3

&nbsp;     - uses: actions/setup-python@v4

&nbsp;       with:

&nbsp;         python-version: '3.x'

&nbsp;     - run: pip install -r requirements.txt

&nbsp;     - run: python app.py

&nbsp;       env:

&nbsp;         GITHUB\_TOKEN: ${{ secrets.PERSONAL\_TOKEN }}

&nbsp;         GITHUB\_REPOSITORY: ${{ github.repository }}

&nbsp;         PR\_NUMBER: ${{ github.event.pull\_request.number }}



Example Output

Inline comment

bad\_code.py:5: F401 - 'os' imported but unused



Summary comment

\### PR Lint Bot Summary

\- bad\_code.py:5 - F401 - 'os' imported but unused

\- test\_file.py:12 - E501 - line too long (120 > 100 characters)



Why it’s professional



Automated linting ensures consistent code quality.



Summary plus optional inline comments make PR review faster and clearer.



Easy to integrate in any Python project or CI/CD workflow.



Clean modular code structure for maintainability.



Future Improvements



Add custom rules for your team or project.



Integrate auto-fix for simple issues (like formatting).



Extend to support other languages or tools (e.g., JavaScript with ESLint).

