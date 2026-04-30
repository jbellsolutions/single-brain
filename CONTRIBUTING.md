# Contributing

## Reporting Issues

Open an issue on GitHub with:
- What you expected to happen
- What actually happened
- Relevant logs (`docker compose logs -f openclaw-gateway`)
- Your compose.yml and .env (with secrets redacted)

## Pull Requests

1. Fork the repo
2. Create a branch: `git checkout -b fix/your-description`
3. Make your changes
4. Open a PR against `main` with a clear description

## Security Rules

**Never commit:**
- `.env`
- `openclaw/config/openclaw.json` (contains live bot tokens)
- `openclaw/config/exec-approvals.json`
- Any file with `xoxb-`, `xapp-`, or bot token patterns

These are gitignored. If you accidentally commit secrets, rotate the tokens immediately and use `git filter-branch` or BFG to remove them from history.

## Docs

If you fix a bug that isn't in `docs/changelog.md`, add an entry there so future users know it's a known issue with a known fix.
