from .celery import app as celery_app

__all__ = ('celery_app',)

JAZZMIN_SETTINGS = {
    "site_title": "Inventory Admin",
    "site_header": "Inventory Manager",
    "welcome_sign": "Welcome to the Inventory Management System",
    "search_model": "inventory_app.Product",
    "topmenu_links": [
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View Site", "url": "/"},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": ["inventory_app", "auth"],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "inventory_app.Product": "fas fa-box",
        "inventory_app.Bill": "fas fa-file-invoice-dollar",
    },
}
