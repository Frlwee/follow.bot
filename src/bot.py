from typing import TYPE_CHECKING, NoReturn, Optional, overload

from vkbottle.api import API
from vkbottle.callback import BotCallback
from vkbottle.dispatch import BuiltinStateDispenser, Router
from vkbottle.exception_factory import ErrorHandler
from vkbottle.framework.abc import ABCFramework
from vkbottle.framework.labeler import BotLabeler
from vkbottle.modules import logger
from vkbottle.polling import BotPolling
from vkbottle.tools import LoopWrapper

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, Token
    from vkbottle.callback import ABCCallback
    from vkbottle.dispatch import ABCRouter, ABCStateDispenser
    from vkbottle.exception_factory import ABCErrorHandler
    from vkbottle.framework.labeler import ABCLabeler
    from vkbottle.polling import ABCPolling


class Bot(ABCFramework):
    @overload
    def __init__(
        self,
        token: Optional["Token"] = None,
        api: Optional["ABCAPI"] = None,
        polling: Optional["ABCPolling"] = None,
        callback: Optional["ABCCallback"] = None,
        loop_wrapper: Optional[LoopWrapper] = None,
        router: Optional["ABCRouter"] = None,
        labeler: Optional["ABCLabeler"] = None,
        state_dispenser: Optional["ABCStateDispenser"] = None,
        error_handler: Optional["ABCErrorHandler"] = None,
    ):
        ...

    @overload
    def __init__(
        self,
        token: Optional["Token"] = None,
        api: Optional["ABCAPI"] = None,
        polling: Optional["ABCPolling"] = None,
        callback: Optional["ABCCallback"] = None,
        loop_wrapper: Optional[LoopWrapper] = None,
        router: Optional["ABCRouter"] = None,
        labeler: Optional["ABCLabeler"] = None,
        state_dispenser: Optional["ABCStateDispenser"] = None,
        error_handler: Optional["ABCErrorHandler"] = None,
    ):
        ...

    def __init__(
        self,
        token: Optional["Token"] = None,
        api: Optional["ABCAPI"] = None,
        polling: Optional["ABCPolling"] = None,
        callback: Optional["ABCCallback"] = None,
        loop_wrapper: Optional[LoopWrapper] = None,
        router: Optional["ABCRouter"] = None,
        labeler: Optional["ABCLabeler"] = None,
        state_dispenser: Optional["ABCStateDispenser"] = None,
        error_handler: Optional["ABCErrorHandler"] = None,
    ):
        self.api: API = api or API(token)  # type: ignore
        self.error_handler = error_handler or ErrorHandler()
        self.loop_wrapper = loop_wrapper or LoopWrapper()
        self.labeler = labeler or BotLabeler()
        self.state_dispenser = state_dispenser or BuiltinStateDispenser()
        self._polling = polling or BotPolling(self.api)
        self._callback = callback or BotCallback()
        self._router = router or Router()

    @property
    def polling(self) -> "ABCPolling":
        return self._polling.construct(self.api, self.error_handler)

    @property
    def router(self) -> "ABCRouter":
        return self._router.construct(
            views=self.labeler.views(),
            state_dispenser=self.state_dispenser,
            error_handler=self.error_handler,
        )

    @router.setter
    def router(self, new_router: "ABCRouter"):
        self._router = new_router

    @property
    def on(self) -> "ABCLabeler":
        return self.labeler

    async def run_polling(self, custom_polling: Optional["ABCPolling"] = None):
        polling = custom_polling or self.polling
        logger.info("Starting polling for {!r}", polling.api)

        async for event in polling.listen():
            logger.debug("New event was received: {}", event)
            for update in event["updates"]:
                self.loop_wrapper.add_task(self.router.route(update, polling.api))

    def run_forever(self) -> NoReturn:  # type: ignore
        logger.info("Loop will be run forever")
        self.loop_wrapper.add_task(self.run_polling())
        self.loop_wrapper.run()

    async def process_event(self, event: dict):
        await self.router.route(event, self.api)
