FROM odoo:16

USER root

# Create required directories and set permissions
RUN mkdir -p /mnt/extra-addons \
    /var/lib/postgresql/data/pgdata \
    /var/lib/odoo \
    /etc/odoo && \
    chown -R odoo:odoo /mnt/extra-addons \
    /var/lib/postgresql/data/pgdata \
    /var/lib/odoo \
    /etc/odoo

# Copy additional modules and configuration
COPY ./addons /mnt/extra-addons
COPY ./etc /etc/odoo
COPY ./startup.sh /usr/local/bin/startup.sh

# Make the startup script executable
RUN chmod +x /usr/local/bin/startup.sh

# Switch to odoo user
USER odoo

# Set the startup script as the entrypoint
ENTRYPOINT ["/usr/local/bin/startup.sh"]
