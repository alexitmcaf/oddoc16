FROM odoo:16

USER root

# Create a directory for additional modules and set permissions
RUN mkdir -p /mnt/extra-addons && chown -R odoo:odoo /mnt/extra-addons

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
addons=$(ls /mnt/extra-addons); \
if [ -n \"$addons\" ]; then \
  odoo --config=/etc/odoo/odoo.conf -u $addons; \
else \
  odoo --config=/etc/odoo/odoo.conf; \
fi"
