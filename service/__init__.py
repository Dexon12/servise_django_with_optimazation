from .celery_app import app as celery_app

__all__ = ('celery_app',) # Записывается в __init__.py чтобы celery стартанула вмете с Django