FROM odoo:16

# Copy additional modules and configuration
COPY ./addons /mnt/extra-addons
COPY ./etc /etc/odoo
COPY ./scripts/update_module_list.py /scripts/update_module_list.py
# COPY ./scripts /scripts
# ENV ODOO_CONF=/etc/odoo/odoo.conf
# Make the script executable
# RUN chmod +x /scripts/test.sh

# Optional: Install additional Python dependencies
# RUN pip install -r /mnt/extra-addons/requirements.txt
EXPOSE 8069

CMD ["odoo"]
