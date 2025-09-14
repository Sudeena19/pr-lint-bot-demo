import os
import re
from github import Github, Auth
from github.GithubException import GithubException

token = os.getenv("GITHUB_TOKEN")
repo_name = os.getenv("GITHUB_REPOSITORY")
pr_number = int(os.getenv("PR_NUMBER", "0"))

def lint_file_local(path):
    issues = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, start=1):
                if len(line) > 100:
                    issues.append((path.replace("\\", "/"), i, f"Line too long ({len(line)} chars)"))
                if "\t" in line:
                    issues.append((path.replace("\\", "/"), i, "Contains tab instead of spaces"))
                if re.search(r"[ \t]+$", line.rstrip("\n\r")):
                    issues.append((path.replace("\\", "/"), i, "Trailing whitespace"))
    except FileNotFoundError:
        pass
    return issues

def build_position_map(patch):
    mapping = {}
    if not patch:
        return mapping
    pos = 0
    cur_new = None
    for raw in patch.splitlines():
        if raw.startswith('@@'):
            m = re.search(r'\+(\d+)(?:,(\d+))?', raw)
            if m:
                cur_new = int(m.group(1))
            continue
        if cur_new is None:
            continue
        pos += 1
        first = raw[:1]
        if first == ' ':
            mapping[cur_new] = pos
            cur_new += 1
        elif first == '+':
            mapping[cur_new] = pos
            cur_new += 1
        elif first == '-':
            # removed line in old file: no change to cur_new
            pass
    return mapping

def main():
    if not token or not repo_name or pr_number == 0:
        print("Missing env vars: GITHUB_TOKEN, GITHUB_REPOSITORY or PR_NUMBER")
        return

    gh = Github(auth=Auth.Token(token))
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    pr_files = list(pr.get_files())
    all_issues = []
    file_position_maps = {}

    for f in pr_files:
        filename = f.filename
        if not filename.endswith(".py"):
            continue
        patch = getattr(f, "patch", None)
        file_position_maps[filename] = build_position_map(patch)
        all_issues.extend(lint_file_local(filename))

    if not all_issues:
        # post single friendly comment saying "no issues"
        try:
            repo.get_issue(pr_number).create_comment("No linting issues found.")
            print("Posted 'no issues' comment.")
        except Exception as e:
            print("Could not post 'no issues' comment:", e)
        return

    comments = []
    fallback = []
    for file, line, msg in all_issues:
        rel_path = file.lstrip("./")
        pos_map = file_position_maps.get(rel_path, {})
        position = pos_map.get(line)
        if position:
            comments.append({"path": rel_path, "position": position, "body": msg})
        else:
            fallback.append(f"{rel_path}:{line} {msg}")

    if comments:
        try:
            # event="COMMENT" -> will not set PR to changes requested
            pr.create_review(body="PR Lint Bot — inline feedback", event="COMMENT", comments=comments)
            print(f"Posted {len(comments)} inline comment(s).")
            # optionally also post a tiny summary in conversation if you want
        except GithubException as e:
            # 403 likely means token lacks permission (e.g., PR from fork)
            print("Failed to post inline review:", e, getattr(e, "status", None), e.data if hasattr(e, "data") else e)
            # fallback to posting first-n issues as a summary on the PR
            if all_issues:
                body = "PR Lint Bot found issues (fallback):\n\n" + "\n".join(f"{f}:{l} {m}" for f, l, m in all_issues[:10])
                try:
                    repo.get_issue(pr_number).create_comment(body)
                    print("Posted fallback summary comment.")
                except Exception as e2:
                    print("Failed to post fallback summary:", e2)
    else:
        # no inline positions found — post short summary (first few)
        body = "PR Lint Bot found issues (no inline positions):\n\n" + "\n".join(f"{f}:{l} {m}" for f, l, m in all_issues[:10])
        try:
            repo.get_issue(pr_number).create_comment(body)
            print("Posted summary comment (no positions).")
        except Exception as e:
            print("Failed to post summary comment:", e)

if __name__ == "__main__":
    main()
