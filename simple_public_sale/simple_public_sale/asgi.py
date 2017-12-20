import os
from channels.asgi import get_channel_layer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simple_public_sale.settings")

channel_layer = get_channel_layer()