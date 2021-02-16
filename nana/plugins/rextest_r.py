from pyrogram import filters
from rextester_py import rexec_aio
from rextester_py import rextester_aio

from nana import AdminSettings
from nana import app
from nana import COMMAND_PREFIXES
from nana import edit_or_reply

__MODULE__ = 'Rextester'
__HELP__ = """
Yet the Another Developer Plugin.

──「 **Rextester** 」──
-> `rex` (*lanuguage) (*code)
Executes the give code with the given language

-> **Currently Supported Languages**
```
| ada  |   bash   |   brainfuck   |   c   |
| c++  |  elixir  |    erlang     |   f#  |
| go   |  fortran |    haskell    |   d   |
| java |  kotlin  |  objective-c  |   js  |
| lua  |   mysql  |   postgresql  |  node |
| lisp |   ocaml  | python3 - py3 |  php  |
| perl |  oracle  |  python - py  |  perl |
| vb   |   nasm   |     pascal    |  sql  |
| ruby |  octave  |     scheme    |   r   |
| tcl  |  scheme  |     scala     | swift |
```
"""


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('rex', COMMAND_PREFIXES),
)
async def rex_tester(_, message):
    try:
        args = message.text.split(None, 2)
        language = args[1]
        code = args[2]
    except IndexError:
        await edit_or_reply(
            message,
            text='Format: `rex lang code`',
        )
        return
    try:
        output = await rexec_aio(language, code)
        final = f'**Language:** `{language}`\n'
        final += f'**Input:**\n`{code}`\n'
        if output.results:
            final += f'**Output:**\n`{output.results}`\n'
        if output.warnings:
            final += f'**Warning:**\n`{output.warnings}`\n'
        if output.errors:
            final += f'**Error:**\n`{output.errors}`\n'
        if output.files:
            final += f'**Files:**\n`{output.files}`\n'
        status = output.stats.split(', ')
        final += '**Status:**\n'
        for x in status:
            final += f'`{x}`\n'
        await edit_or_reply(message, text=final, parse_mode='markdown')
    except rextester_aio.UnknownLanguage:
        await edit_or_reply(message, text='Wrong language!')
