#!/bin/bash

# Fix permissions for PostgreSQL data directory
chown -R odoo:odoo /var/lib/postgresql/data/pgdata

# Execute the provided command (CMD or arguments)
exec "$@"
