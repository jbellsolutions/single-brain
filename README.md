# Vault — Shared Agent Memory

This directory is the `vault` — a git-backed shared memory store mounted into both the OpenClaw and Hermes containers at `/vault`.

## Setup

The vault lives as a **separate git repository** at `/srv/single-brain/vault/` on the VPS. It is not committed inside the main repo.

```bash
# On the VPS, initialize the vault from this skeleton
mkdir -p /srv/single-brain/vault
cp -r /srv/single-brain/vault-skeleton/. /srv/single-brain/vault/
cd /srv/single-brain/vault
git init
git add .
git commit -m "init: vault structure"
```

Optionally push to a private GitHub repo for off-site backup:
```bash
git remote add origin https://github.com/YOUR_USERNAME/single-brain-vault.git
git push -u origin main
```

## Structure

```
vault/
├── agents/          Agent identity files
│   ├── CLAUDE.md    Instructions for the OpenClaw main agent
│   └── voice.md     Agent persona / communication style
├── sops/            Standard Operating Procedures (per domain)
├── decisions/       Append-only log of major decisions
├── daily-logs/      One .md file per UTC day (written by agents)
└── domains/         Work product per domain
```

## Gitignore

The vault's `daily-logs/` and `domains/` are gitignored in the main repo to keep agent output separate. The vault repo tracks its own history.
