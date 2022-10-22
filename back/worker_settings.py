from config import get_settings

settings = get_settings()

REDIS_URL = settings.REDIS_URI
