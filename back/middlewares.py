import redis
from rq import Queue
from starlette.middleware.base import BaseHTTPMiddleware

class RedisMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, settings):
        super().__init__(app)
        self.app = app
        self.redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
        )
        self.queue  = Queue(connection=self.redis)


    async def dispatch(self, request, call_next):
        request.state.queue = self.queue

        return await call_next(request)