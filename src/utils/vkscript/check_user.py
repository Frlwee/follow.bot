from typing import List, Union

from vkbottle import API

from src.database.models import Group


async def is_group_member(api: API, user_id: int) -> Union[str, bool]:
    groups: List[Group] = await Group.all()

    for group in groups:
        if not await api.groups.is_member(group_id=group.screen_name, user_id=user_id):
            result = ''.join(
                [f'{index}. @{group.screen_name} ({group.name})\n' for index, group in enumerate(groups, 1)]
            )
            return result
    return True
