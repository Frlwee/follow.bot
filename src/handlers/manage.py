from typing import Union

from vkbottle.dispatch.rules.base import VBMLRule, FromUserRule
from vkbottle.bot import BotLabeler, Message
from vkbottle_types.codegen.objects import UsersUserFull

from src.utils.helper import search_group_mention
from src.utils.i18n import gettext
from src.database.models import Group
from src.rules.is_admin import IsAdminRule
from src.utils.vkscript.check_user import is_group_member

labeler = BotLabeler()


@labeler.message(IsAdminRule(), mention=True)
async def get_manageable_groups(_: Message):
    groups: list[Group] = await Group.all()

    if not groups:
        return gettext("messages.no_managed_groups")

    answer = gettext("messages.managed_groups")

    for index, group in enumerate(groups, 1):
        answer += gettext("messages.group_add_line").format(
            index=index,
            screen_name=group.screen_name,
            name=group.name,
            add_by=group.add_by
        )

    return answer


@labeler.message(VBMLRule("+ <group_mention>"), IsAdminRule())
async def add_group(message: Message, group_mention: str, user_information: UsersUserFull) -> None:

    mention: Union[None, str] = search_group_mention(group_mention)

    if mention:
        group: Group = await Group.get_or_none(screen_name=mention)

        if not group:
            group_info = (await message.ctx_api.groups.get_by_id(group_id=mention))[0]

            await Group.create(
                id=group_info.id,
                screen_name=group_info.screen_name,
                name=group_info.name,
                add_by=f"@id{user_information.id} ({user_information.first_name})",
            )

            await message.answer(gettext("messages.group_success_add").format(
                screen_name=group_info.screen_name,
                name=group_info.name
            ))


@labeler.message(VBMLRule("- <group_mention>"), IsAdminRule())
async def del_group(message: Message, group_mention: str) -> None:

    mention: Union[None, str] = search_group_mention(group_mention)

    if mention:
        group: Group = await Group.get_or_none(screen_name=mention)

        if group:
            await Group.filter(screen_name=mention).delete()

            await message.answer(gettext("messages.group_success_delete").format(
                screen_name=group.screen_name,
                name=group.name
            ))


@labeler.chat_message(FromUserRule())
async def check_user(message: Message, user_information: UsersUserFull) -> None:

    groups = await is_group_member(message.ctx_api, message.from_id)
    if isinstance(groups, str):

        await message.ctx_api.messages.delete(
            peer_id=message.peer_id,
            cmids=message.conversation_message_id,
            delete_for_all=1
        )

        await message.answer(gettext("messages.writing_condition_in_conversation").format(
            id=user_information.id,
            first_name=user_information.first_name,
            last_name=user_information.last_name,
            groups=groups
        ))