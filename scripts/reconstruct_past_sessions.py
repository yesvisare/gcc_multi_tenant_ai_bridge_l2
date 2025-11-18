#!/usr/bin/env python3
"""
Reconstruct past sessions from git commit history.

This script analyzes git commits and helps you backfill SESSION_LOG.md
with information from past development sessions.

Usage:
    python scripts/reconstruct_past_sessions.py --start-date 2025-01-01
    python scripts/reconstruct_past_sessions.py --commits 10
    python scripts/reconstruct_past_sessions.py --branch main
"""

import argparse
import subprocess
import sys
from datetime import datetime
from collections import defaultdict


def run_git_command(command):
    """Run a git command and return output."""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}", file=sys.stderr)
        return ""


def get_commit_history(start_date=None, num_commits=None, branch=None):
    """Get git commit history."""
    cmd = "git log --pretty=format:'%H|%h|%an|%ae|%ad|%s' --date=short"

    if branch:
        cmd += f" {branch}"

    if start_date:
        cmd += f" --since='{start_date}'"

    if num_commits:
        cmd += f" -n {num_commits}"

    output = run_git_command(cmd)

    commits = []
    for line in output.split('\n'):
        if line:
            parts = line.split('|')
            if len(parts) == 6:
                commits.append({
                    'hash': parts[0],
                    'short_hash': parts[1],
                    'author': parts[2],
                    'email': parts[3],
                    'date': parts[4],
                    'message': parts[5]
                })

    return commits


def get_files_in_commit(commit_hash):
    """Get files changed in a specific commit."""
    cmd = f"git diff-tree --no-commit-id --name-status -r {commit_hash}"
    output = run_git_command(cmd)

    files = []
    for line in output.split('\n'):
        if line:
            parts = line.split('\t')
            if len(parts) >= 2:
                status_map = {'A': 'NEW', 'M': 'MODIFIED', 'D': 'DELETED'}
                files.append({
                    'status': status_map.get(parts[0], parts[0]),
                    'path': parts[1]
                })

    return files


def get_commit_stats(commit_hash):
    """Get insertion/deletion stats for a commit."""
    cmd = f"git show --shortstat --pretty='' {commit_hash}"
    stats = run_git_command(cmd)
    return stats.strip() if stats else "No stats"


def group_commits_by_session(commits):
    """
    Group commits into likely sessions based on date and commit messages.

    Heuristic: Commits on the same day with related messages are likely
    from the same session.
    """
    sessions = defaultdict(list)

    for commit in commits:
        # Group by date
        date = commit['date']
        sessions[date].append(commit)

    return sessions


def generate_session_entry(session_num, date, commits):
    """Generate a session entry from commit history."""

    # Combine all commit messages
    messages = [c['message'] for c in commits]

    # Get all files changed across commits
    all_files = []
    for commit in commits:
        files = get_files_in_commit(commit['hash'])
        all_files.extend(files)

    # Remove duplicates (keep latest status)
    files_dict = {}
    for f in all_files:
        files_dict[f['path']] = f['status']

    files_changed = '\n'.join([f"- `{path}` ({status})" for path, status in files_dict.items()])

    # Get stats for first commit (most significant)
    main_commit = commits[0]
    stats = get_commit_stats(main_commit['hash'])

    # Generate combined task description from commit messages
    task_desc = "\n".join([f"- {msg}" for msg in messages])

    template = f"""
## Session {session_num} - {date}

### Task Description
[RECONSTRUCTED FROM GIT HISTORY]

Commits from this session:
{task_desc}

### Deliverables

**Files created/modified in this session:**
{files_changed}

**[MANUAL REVIEW NEEDED]**
Please review the files above and provide a description of what was built.

### Files Changed
{files_changed}

### Git Details
- **Main Commit:** `{main_commit['short_hash']}` - "{main_commit['message']}"
- **Total Commits:** {len(commits)}
- **Author:** {main_commit['author']}
- **Stats:** {stats}

### Key Outcomes

**[MANUAL REVIEW NEEDED]**
Please fill in:
- What standards were met
- What was accomplished
- Any important highlights

### Metrics

**Commits:** {len(commits)}
**Files Changed:** {len(files_dict)}

**[MANUAL REVIEW NEEDED]**
Add specific metrics based on what was built.

### Notes

**RECONSTRUCTED FROM GIT HISTORY**
This session entry was automatically generated from git commits.
Please review and update with actual context from the session.

Commit details:
"""

    for commit in commits:
        template += f"\n- {commit['short_hash']}: {commit['message']}"

    template += "\n\n---\n"

    return template


def main():
    parser = argparse.ArgumentParser(
        description="Reconstruct past sessions from git history"
    )
    parser.add_argument(
        "--start-date",
        type=str,
        help="Start date for commit history (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--commits",
        type=int,
        help="Number of recent commits to analyze"
    )
    parser.add_argument(
        "--branch",
        type=str,
        help="Git branch to analyze"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="RECONSTRUCTED_SESSIONS.md",
        help="Output file for reconstructed sessions"
    )
    parser.add_argument(
        "--start-session-num",
        type=int,
        default=2,
        help="Starting session number (default: 2)"
    )

    args = parser.parse_args()

    print("🔍 Analyzing git history...")

    # Get commit history
    commits = get_commit_history(args.start_date, args.commits, args.branch)

    if not commits:
        print("❌ No commits found with the given criteria")
        return 1

    print(f"✅ Found {len(commits)} commits")

    # Group commits by likely sessions (by date)
    sessions = group_commits_by_session(commits)

    print(f"📅 Grouped into {len(sessions)} potential sessions")
    print()

    # Generate session entries
    output_content = "# Reconstructed Sessions from Git History\n\n"
    output_content += "**NOTE:** These sessions were reconstructed from git commits.\n"
    output_content += "Please review and update with actual context from each session.\n\n"
    output_content += "---\n\n"

    session_num = args.start_session_num
    for date in sorted(sessions.keys(), reverse=True):
        session_commits = sessions[date]
        print(f"📝 Session {session_num} - {date} ({len(session_commits)} commits)")

        entry = generate_session_entry(session_num, date, session_commits)
        output_content += entry

        session_num += 1

    # Write to output file
    with open(args.output, 'w') as f:
        f.write(output_content)

    print()
    print(f"✅ Reconstructed sessions written to: {args.output}")
    print()
    print("📋 Next steps:")
    print("1. Review the generated file")
    print("2. Fill in the [MANUAL REVIEW NEEDED] sections")
    print("3. Copy relevant entries to SESSION_LOG.md")
    print("4. Commit the updated SESSION_LOG.md")

    return 0


if __name__ == "__main__":
    sys.exit(main())
