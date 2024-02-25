from src.middlewares.no_bot import NoBotMiddleware
from src.middlewares.user_information import UserInformationMiddleware


middlewares = (NoBotMiddleware, UserInformationMiddleware)


__all__ = (middlewares,)
