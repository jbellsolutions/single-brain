#!/bin/bash
# Pull the latest vault commits from the VPS and sync to a local copy.
# Vault is a git repo at /srv/single-brain/vault/ on the VPS.
#
# Set LOCAL_VAULT to wherever you want the vault synced on your Mac.
# Requires the SSH alias 'your-server' to be configured in ~/.ssh/config (see docs/setup.md).

LOCAL_VAULT=~/Desktop/single-brain/vault/

mkdir -p "$LOCAL_VAULT"

echo "Syncing vault from your-server:/srv/single-brain/vault/ ..."
rsync -avz --exclude='.git' your-server:/srv/single-brain/vault/ "$LOCAL_VAULT"

echo ""
echo "Done. Local vault at: $LOCAL_VAULT"
