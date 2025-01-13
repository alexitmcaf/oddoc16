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
# COPY ./startup.sh /usr/local/bin/startup.sh

# Make the startup script executable
# RUN chmod +x /usr/local/bin/startup.sh

# Switch to odoo user
USER odoo

# Set the CMD with conditional logic for modules
CMD bash -c "\
addons=$(ls -1 /mnt/extra-addons | tr '\n' ',' | sed 's/,$//'); \
if [ -n \"$addons\" ]; then \
  odoo --config=/etc/odoo/odoo.conf -u \"$addons\"; \
else \
  odoo --config=/etc/odoo/odoo.conf; \
fi"