#!/bin/bash
# SSH into the Single Brain VPS.
# Requires an SSH alias configured in ~/.ssh/config on your Mac:
#
#   Host your-server
#       HostName YOUR.SERVER.IP
#       User claw
#       IdentityFile ~/.ssh/id_ed25519
#
# See docs/setup.md for full SSH config instructions.
exec ssh your-server "$@"
