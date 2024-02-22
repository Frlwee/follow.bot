import re
from typing import Union

from src.config import logger


async def search_group_mention(group_mention: str) -> Union[None, str]:

    match = re.search(r'vk\.com/(.+)', group_mention)

    try:
        return match.group(1)
    except Exception as e:
        logger.exception(e)
        return None
