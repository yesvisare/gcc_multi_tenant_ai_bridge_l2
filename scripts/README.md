# Scripts Directory

Helper scripts for managing the gcc_multi_tenant_ai_bridge_l2 repository.

---

## update_session_log.py

**Purpose:** Automatically update `SESSION_LOG.md` with new session information by extracting git commit details.

### Usage

**Basic usage:**
```bash
python scripts/update_session_log.py --session 2 --task "Create validation script for M14.3"
```

**With custom branch:**
```bash
python scripts/update_session_log.py \
  --session 2 \
  --task "Add integration tests" \
  --branch "feature/integration-tests"
```

**With custom log path:**
```bash
python scripts/update_session_log.py \
  --session 2 \
  --task "Update documentation" \
  --log-path "../SESSION_LOG.md"
```

### What It Does

1. **Extracts Git Information:**
   - Latest commit hash and message
   - Files changed (with NEW/MODIFIED/DELETED status)
   - Current branch name
   - Insertion/deletion statistics

2. **Generates Session Entry:**
   - Creates formatted session entry with template
   - Inserts it into SESSION_LOG.md at correct position
   - Pre-fills git details automatically

3. **Prompts for Manual Entry:**
   - Deliverables section (manual fill-in)
   - Key Outcomes (manual fill-in)
   - Metrics (manual fill-in)

### Options

- `--session N` (required): Session number
- `--task "description"` (required): Task description
- `--branch name`: Git branch (auto-detected if omitted)
- `--log-path path`: Path to SESSION_LOG.md (default: SESSION_LOG.md)

### Example Output

```markdown
## Session 2 - 2025-11-18

### Task Description
Create validation script for M14.3

### Deliverables
**[TO BE FILLED]**

### Files Changed
- `scripts/validate_m14_3.py` (NEW)
- `tests/test_validation.py` (NEW)

### Git Details
- **Branch:** `feature/validation-script`
- **Commit:** `abc1234` - "Add M14.3 validation script"
- **Status:** ✅ Committed and Pushed
- **Stats:** 2 files changed, 150 insertions(+)

### Key Outcomes
**[TO BE FILLED]**

### Metrics
**[TO BE FILLED]**

### Notes
[Add any important notes or follow-ups]
```

### After Running

1. Open `SESSION_LOG.md`
2. Fill in the `[TO BE FILLED]` sections:
   - **Deliverables:** List what was created/modified with descriptions
   - **Key Outcomes:** List success criteria met, standards followed
   - **Metrics:** Add relevant metrics (files, lines, features, etc.)
   - **Notes:** Add any important context
3. Commit the updated `SESSION_LOG.md`

---

## Manual Alternative

If you prefer not to use the script, you can manually update `SESSION_LOG.md` using the template in `.github/SESSION_TEMPLATE.md`.

### Steps:

1. Copy template from `.github/SESSION_TEMPLATE.md`
2. Fill in all sections
3. Insert into `SESSION_LOG.md` under "## Future Sessions"
4. Update "Quick Stats" section at bottom
5. Commit changes

---

## Tips

**For Claude Code Sessions:**
- Run the script at the END of each session after pushing commits
- The script captures the most recent commit, so ensure your work is committed first
- Fill in the manual sections immediately while context is fresh
- Use the session log to track progress across multiple sessions

**For Long Tasks:**
- Create intermediate session entries for major milestones
- Use session numbers with decimals (e.g., 2.1, 2.2) for sub-sessions
- Reference previous sessions in Notes section when building on prior work

**For Team Collaboration:**
- Include your name in the task description
- Link to PRs in the "PR Available" field
- Add context about decisions made or alternatives considered

---

## Future Enhancements

Potential improvements to this script:

- [ ] Auto-detect session number (increment latest)
- [ ] Parse git commit messages for common patterns
- [ ] Generate metrics from code analysis (LOC, complexity)
- [ ] Extract PR information from GitHub API
- [ ] Auto-update "Quick Stats" section
- [ ] Support for multiple commits in one session
- [ ] Markdown formatting validation
