from typing import Union, List

from vkbottle import API, run_multibot
from vkbottle.bot import Bot, Message, rules
from vkbottle_types.objects import UsersUserFull

from src.database.models import Group
from src.database import init_database

from src.utils import loop, loop_wrapper
from src.utils.helper import search_group_mention
from src.utils.vkscript.check_user import is_group_member

from src.config import config
from src.rules import IsAdminRule
from src.middlewares import middlewares


bot = Bot(
    loop=loop,
    loop_wrapper=loop_wrapper,
)


@bot.on.message(rules.VBMLRule("/"), IsAdminRule())
async def get_groups(message: Message) -> None:

    groups: List[Group] = await Group.all()
    result = ''.join(
        [f'{index}. @{group.screen_name} ({group.name})\nДобавил: {group.add_by}\n\n' for index, group in enumerate(groups, 1)]
    )

    await message.answer(
        f"📚 Список сообществ, которые бот проверяет:\n\n{result if result else '👀 Пусто'}"
    )


@bot.on.message(rules.VBMLRule("+ <group_mention>"), IsAdminRule())
async def add_group(message: Message, group_mention: str, user_info: UsersUserFull) -> None:

    mention: Union[None, str] = await search_group_mention(group_mention)

    if mention:
        group: Group = await Group.get_or_none(screen_name=mention)

        if not group:
            group_info = (await message.ctx_api.groups.get_by_id(group_id=mention))[0]

            await Group.create(
                id=group_info.id,
                screen_name=group_info.screen_name,
                name=group_info.name,
                add_by=f"@id{user_info.id} ({user_info.first_name})",
            )

            await message.answer(
                f"✅ Группа: @{group_info.screen_name} ({group_info.name}) успешно добавлена в базу данных."
            )


@bot.on.message(rules.VBMLRule("- <group_mention>"), IsAdminRule())
async def del_group(message: Message, group_mention: str) -> None:

    mention: Union[None, str] = await search_group_mention(group_mention)

    if mention:
        group: Group = await Group.get_or_none(screen_name=mention)

        if group:
            await Group.filter(screen_name=mention).delete()

            await message.answer(
                f"✅ Группа: @{group.screen_name} ({group.name}) успешно удалена из базы данных."
            )


@bot.on.chat_message(rules.FromUserRule())
async def check_user(message: Message, user_info: UsersUserFull) -> None:

    groups = await is_group_member(message.ctx_api, message.from_id)
    if isinstance(groups, str):

        await message.ctx_api.messages.delete(
            peer_id=message.peer_id,
            cmids=message.conversation_message_id,
            delete_for_all=1
        )

        await message.answer(
            f"@id{user_info.id} ({user_info.first_name} {user_info.last_name}), чтобы писать в беседу, вступи в группы:\n\n"
            "➖➖➖➖➖\n"
            f"{groups}"
            "➖➖➖➖➖\n\n"
            "📝 Хочешь добавить свою группу тоже?\n🖌 Пиши Администратору: @shoopblack"
        )


def __main__():

    for middleware in middlewares:
        bot.labeler.message_view.register_middleware(middleware)

    loop_wrapper.add_task(init_database())
    loop_wrapper.add_task(
        run_multibot(
            bot,
            apis=([API(token) for token in config.vk.bot.tokens])
        )
    )

    loop_wrapper.run_forever(loop=loop)


if __name__ == "__main__":
    __main__()
