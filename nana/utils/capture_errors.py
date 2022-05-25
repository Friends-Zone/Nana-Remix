import sys
import traceback
from functools import wraps

from pyrogram.types import InlineKeyboardButton

from pykeyboard import InlineKeyboard

from nana import Owner
from nana import setbot
from nana.utils.parser import split_limits


def capture_err(func):
    @wraps(func)
    async def capture(client, message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type, value=exc_obj, tb=exc_tb,
            )
            error_feedback = split_limits(
                '**ERROR** | `{}` | `{}`\n\n```{}```\n\n```{}```\n'.format(
                    message.from_user.id if message.from_user else 0,
                    message.chat.id if message.chat else 0,
                    message.text or message.caption,
                    ''.join(errors),
                )
            )

            button = InlineKeyboard(row_width=1)
            button.add(
                InlineKeyboardButton(
                    '🐞 Report bugs',
                    callback_data='report_errors',
                ),
            )
            for x in error_feedback:
                await setbot.send_message(
                    Owner,
                    x,
                    reply_markup=button,
                )
            raise err
    return capture
