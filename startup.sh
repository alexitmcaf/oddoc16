#!/bin/bash

# Remove cache to reflect updated addons
rm -rf /var/lib/odoo/.local/share/Odoo/*

# Collect all addon names
addons=$(ls -1 /mnt/extra-addons | tr '\n' ',' | sed 's/,$//')

# Run Odoo with or without addons
if [ -n "$addons" ]; then
  exec odoo --config=/etc/odoo/odoo.conf -u "$addons"
else
  exec odoo --config=/etc/odoo/odoo.conf
fi
