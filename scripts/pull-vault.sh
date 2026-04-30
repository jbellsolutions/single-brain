#!/bin/bash
# Pull the latest vault commits from the VPS and sync to a local copy.
# Vault is a git repo at /srv/single-brain/vault/ on the VPS.

LOCAL_VAULT=~/Desktop/OpenClaw\ 10X/vault/

mkdir -p "$LOCAL_VAULT"

echo "Syncing vault from single-brain:/srv/single-brain/vault/ ..."
rsync -avz --exclude='.git' single-brain:/srv/single-brain/vault/ "$LOCAL_VAULT"

echo ""
echo "Done. Local vault at: $LOCAL_VAULT"
