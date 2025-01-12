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

# Uncomment if scripts and additional dependencies are needed
# COPY ./scripts/update_module_list.py /scripts/update_module_list.py
# COPY ./scripts /scripts
# ENV ODOO_CONF=/etc/odoo/odoo.conf
# Make the script executable
# RUN chmod +x /scripts/test.sh

# Optional: Install additional Python dependencies
# RUN pip install -r /mnt/extra-addons/requirements.txt

# Expose the Odoo default port
EXPOSE 8069

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