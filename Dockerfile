FROM odoo:16

USER root

# Create directories for additional modules, configuration, and volumes
RUN mkdir -p /mnt/extra-addons \
    && mkdir -p /var/lib/postgresql/data/pgdata \
    && mkdir -p /var/lib/odoo \
    && mkdir -p /etc/odoo \
    && chown -R odoo:odoo /mnt/extra-addons \
    && chown -R odoo:odoo /var/lib/postgresql/data/pgdata \
    && chown -R odoo:odoo /var/lib/odoo \
    && chown -R odoo:odoo /etc/odoo

# Copy additional modules and configuration
COPY ./addons /mnt/extra-addons
COPY ./etc /etc/odoo

# Copy the startup script
COPY ./startup.sh /usr/local/bin/startup.sh

# Make the startup script executable
RUN chmod +x /usr/local/bin/startup.sh

# Expose the Odoo default port
EXPOSE 8069

# Switch to odoo user
USER odoo

# Set the ENTRYPOINT to use the startup script
ENTRYPOINT ["/usr/local/bin/startup.sh"]

# Set the CMD with conditional logic for modules
CMD bash -c "\
addons=$(ls -1 /mnt/extra-addons | tr '\n' ',' | sed 's/,$//'); \
if [ -n \"$addons\" ]; then \
  odoo --config=/etc/odoo/odoo.conf -u \"$addons\"; \
else \
  odoo --config=/etc/odoo/odoo.conf; \
fi"