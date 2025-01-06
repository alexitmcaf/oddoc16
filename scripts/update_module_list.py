from odoo import api, SUPERUSER_ID

def update_module_list(cr):
    """
    Updates the module list in Odoo 16 without entering developer mode.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    module_obj = env['ir.module.module']
    print("Updating module list...")
    module_obj.update_list()
    modules = env['ir.module.module'].search([])
    for module in modules:
        print(f"Module: {module.name}, State: {module.state}")
    print("Module list updated successfully.")

if __name__ == '__main__':
    import odoo
    import os
    import sys

    try:
        config_path = os.getenv('ODOO_CONF', '/etc/odoo/odoo.conf')
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found at {config_path}")

        odoo.tools.config.parse_config(['-c', config_path])

        # Override database connection settings for Docker
        odoo.tools.config['db_host'] = os.getenv('DB_HOST', 'psql')  # Default to 'db' for Docker
        odoo.tools.config['db_port'] = os.getenv('DB_PORT', '5432')
        odoo.tools.config['db_user'] = os.getenv('DB_USER', 'odoo16')
        odoo.tools.config['db_password'] = os.getenv('DB_PASSWORD', 'odoo16')
        db_name = odoo.tools.config.get('db_name', os.getenv('DB_NAME', 'postgres'))

        print(f"Connecting to database: {db_name} at {odoo.tools.config['db_host']}:{odoo.tools.config['db_port']}")

        with odoo.sql_db.db_connect(db_name).cursor() as cr:
            cr.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'ir_module_module';")
            if cr.fetchone()[0] == 0:
                raise RuntimeError("Database not initialized. Run Odoo with `-i base` to initialize.")

            update_module_list(cr)
            cr.commit()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
