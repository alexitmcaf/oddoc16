FROM odoo:16

# Copy additional modules and configuration
COPY ./custom-addons /mnt/extra-addons
COPY ./config /etc/odoo
# COPY ./scripts /scripts

# Make the script executable
# RUN chmod +x /scripts/test.sh

# Optional: Install additional Python dependencies
# RUN pip install -r /mnt/extra-addons/requirements.txt

CMD ["odoo"]
