#!/usr/bin/env python3
"""
Interactive script to add a session to SESSION_LOG.md.

Instead of copying a template, this script prompts you for information
and formats it correctly.

Usage:
    python scripts/add_session.py
"""

import sys
from datetime import datetime
from pathlib import Path


def get_multiline_input(prompt):
    """Get multiline input from user (end with Ctrl+D or empty line)."""
    print(f"\n{prompt}")
    print("(Paste content, then press Ctrl+D when done, or empty line + Enter)")
    print("-" * 60)

    lines = []
    try:
        while True:
            line = input()
            if not line and lines:  # Empty line after some content
                break
            lines.append(line)
    except EOFError:
        pass

    return '\n'.join(lines)


def main():
    print("="*60)
    print("Add Session to SESSION_LOG.md")
    print("="*60)

    # Get session number
    session_num = input("\nSession number: ")

    # Get date (default to today)
    date_input = input(f"Date (YYYY-MM-DD) [default: today]: ").strip()
    if not date_input:
        date_input = datetime.now().strftime("%Y-%m-%d")

    # Get task description
    task_desc = input("\nTask description (one line): ")

    # Get deliverables (multiline)
    deliverables = get_multiline_input(
        "\n📦 Deliverables section:"
        "\n(Copy from Claude's output and paste here)"
    )

    # Get quality standards (multiline)
    quality = get_multiline_input(
        "\n🎯 Quality Standards Met section:"
        "\n(Copy from Claude's output and paste here)"
    )

    # Get summary (multiline)
    summary = get_multiline_input(
        "\n📊 Summary section:"
        "\n(Copy from Claude's output and paste here)"
    )

    # Get git details (multiline)
    git_details = get_multiline_input(
        "\n🚀 Git Status section:"
        "\n(Copy from Claude's output and paste here)"
    )

    # Get usage (multiline)
    usage = get_multiline_input(
        "\n🎓 Usage section:"
        "\n(Copy from Claude's output and paste here)"
    )

    # Get metrics (multiline)
    metrics = get_multiline_input(
        "\nMetrics:"
        "\n(Copy from Claude's output and paste here)"
    )

    # Get notes (optional)
    notes = get_multiline_input(
        "\nNotes (optional):"
        "\n(Any additional context)"
    )

    # Build session entry
    entry = f"""
## Session {session_num} - {date_input}

### Task Description
{task_desc}

### 📦 Deliverables

{deliverables}

### 🎯 Quality Standards Met

{quality}

### 📊 Summary

{summary}

### 🚀 Git Status

{git_details}

### 🎓 Usage

{usage}

### Metrics

{metrics}
"""

    if notes.strip():
        entry += f"""
### Notes

{notes}
"""

    entry += "\n---\n"

    # Show preview
    print("\n" + "="*60)
    print("PREVIEW:")
    print("="*60)
    print(entry)

    # Confirm
    confirm = input("\nAdd this to SESSION_LOG.md? (y/n): ")
    if confirm.lower() != 'y':
        print("Cancelled.")
        return 1

    # Find SESSION_LOG.md
    log_path = Path("SESSION_LOG.md")
    if not log_path.exists():
        print(f"Error: {log_path} not found!")
        return 1

    # Read current content
    content = log_path.read_text()

    # Find insertion point
    marker = "## Future Sessions"
    marker_pos = content.find(marker)

    if marker_pos == -1:
        print(f"Error: Could not find '{marker}' in SESSION_LOG.md")
        return 1

    # Find the end of the marker section
    next_section = content.find("\n---\n", marker_pos)
    if next_section == -1:
        print("Error: Could not find section end")
        return 1

    # Insert the new session
    insertion_point = next_section + len("\n---\n")
    new_content = (
        content[:insertion_point] +
        entry +
        content[insertion_point:]
    )

    # Write back
    log_path.write_text(new_content)

    print(f"\n✅ Session {session_num} added to SESSION_LOG.md")
    print("\nNext steps:")
    print("  git add SESSION_LOG.md")
    print(f"  git commit -m 'Add session {session_num} deliverables'")
    print("  git push")

    return 0


if __name__ == "__main__":
    sys.exit(main())
