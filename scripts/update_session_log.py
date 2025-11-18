#!/usr/bin/env python3
"""
Helper script to update SESSION_LOG.md with new session information.

Usage:
    python scripts/update_session_log.py --session N --task "Description" --branch branch-name

This script will:
1. Extract git information (commits, files changed)
2. Generate a formatted session entry
3. Insert it into SESSION_LOG.md at the correct position
"""

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path


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


def get_latest_commit_info():
    """Get information about the latest commit."""
    commit_hash = run_git_command("git rev-parse --short HEAD")
    commit_message = run_git_command("git log -1 --pretty=%B")
    return commit_hash, commit_message


def get_files_changed(base_commit="HEAD~1"):
    """Get list of files changed in recent commits."""
    files = run_git_command(f"git diff --name-status {base_commit} HEAD")

    file_list = []
    for line in files.split('\n'):
        if line:
            status, filepath = line.split('\t', 1)
            status_map = {'A': 'NEW', 'M': 'MODIFIED', 'D': 'DELETED'}
            file_list.append(f"- `{filepath}` ({status_map.get(status, status)})")

    return '\n'.join(file_list) if file_list else "- No files changed"


def get_branch_name():
    """Get current git branch name."""
    return run_git_command("git rev-parse --abbrev-ref HEAD")


def get_stats():
    """Get insertion/deletion stats for recent commits."""
    stats = run_git_command("git diff --shortstat HEAD~1 HEAD")
    return stats if stats else "No stats available"


def create_session_entry(session_num, task_desc, branch=None):
    """Create a formatted session entry."""
    today = datetime.now().strftime("%Y-%m-%d")
    branch = branch or get_branch_name()
    commit_hash, commit_msg = get_latest_commit_info()
    files_changed = get_files_changed()
    stats = get_stats()

    template = f"""
## Session {session_num} - {today}

### Task Description
{task_desc}

### Deliverables

**[TO BE FILLED]**

### Files Changed
{files_changed}

### Git Details
- **Branch:** `{branch}`
- **Commit:** `{commit_hash}` - "{commit_msg}"
- **Status:** ✅ Committed and Pushed
- **Stats:** {stats}

### Key Outcomes

**[TO BE FILLED]**

### Metrics

**[TO BE FILLED]**

### Notes
[Add any important notes or follow-ups]

---
"""
    return template


def insert_session_into_log(session_entry, log_path="SESSION_LOG.md"):
    """Insert the session entry into SESSION_LOG.md at the correct position."""
    log_file = Path(log_path)

    if not log_file.exists():
        print(f"Error: {log_path} not found!", file=sys.stderr)
        return False

    content = log_file.read_text()

    # Find the insertion point (after "## Future Sessions" marker)
    marker = "## Future Sessions"
    marker_pos = content.find(marker)

    if marker_pos == -1:
        print(f"Error: Could not find '{marker}' in {log_path}", file=sys.stderr)
        return False

    # Find the end of the marker section
    next_section = content.find("\n---\n", marker_pos)
    if next_section == -1:
        print(f"Error: Could not find section end after '{marker}'", file=sys.stderr)
        return False

    # Insert the new session
    insertion_point = next_section + len("\n---\n")
    new_content = (
        content[:insertion_point] +
        session_entry +
        content[insertion_point:]
    )

    # Write back to file
    log_file.write_text(new_content)
    print(f"✅ Session entry added to {log_path}")
    print(f"\nPlease edit {log_path} to fill in the [TO BE FILLED] sections:")
    print("  - Deliverables")
    print("  - Key Outcomes")
    print("  - Metrics")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Update SESSION_LOG.md with new session information"
    )
    parser.add_argument(
        "--session",
        type=int,
        required=True,
        help="Session number"
    )
    parser.add_argument(
        "--task",
        type=str,
        required=True,
        help="Task description"
    )
    parser.add_argument(
        "--branch",
        type=str,
        help="Git branch name (auto-detected if not provided)"
    )
    parser.add_argument(
        "--log-path",
        type=str,
        default="SESSION_LOG.md",
        help="Path to SESSION_LOG.md (default: SESSION_LOG.md)"
    )

    args = parser.parse_args()

    # Create session entry
    session_entry = create_session_entry(args.session, args.task, args.branch)

    # Insert into log
    success = insert_session_into_log(session_entry, args.log_path)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
