import re
from typing import Union


def search_group_mention(group_mention: str) -> Union[None, str]:
    match = re.search(r'vk\.com/(.+)', group_mention)

    try:
        return match.group(1)
    except: # noqa
        return None
