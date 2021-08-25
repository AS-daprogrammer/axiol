"""Axiol Bot Core."""
import os
import sys
from typing import List, NoReturn

import dotenv
from discord import Message
from discord.ext import commands

from axiol import DOTENV_PATH, PREVENT_DOUBLE_RUNTIME_ERROR, OWNER_ID
from axiol.core.context import TimedContext
from axiol.database.db_wrapper import collections
from axiol.tasks.update_presence import update_presence
from axiol.utils.logger import log

TOKEN_KEY: str = 'TOKEN'


class Bot(commands.Bot):
    """Axiol custom bot class."""

    def __init__(self, prefix: str) -> None:
        log.inform("Initializing bot...")

        self.default_prefix = prefix
        super(Bot, self).__init__(
            command_prefix=self.get_prefix,
            owner_id=OWNER_ID
        )

        self.remove_command('help')
        log.inform("Loaded Embed Templator")

    def load_extensions(self, cog_list: List[str]) -> None:
        log.inform("Loading bot extensions...")
        for cog in cog_list:
            self.load_extension(cog)

    def run(self) -> None:
        log.inform("Starting bot...")

        super(Bot, self).run(
            os.environ.get(TOKEN_KEY)
            or dotenv.dotenv_values(DOTENV_PATH).get(TOKEN_KEY)
        )

    def load_extension(self, name: str, *, _package=None) -> None:
        cog_path: str = f'axiol.cogs.{name}'
        cog_name: str = cog_path.split('.')[1]

        log.inform(f"Loading {cog_name} extension...")

        try:
            super(Bot, self).load_extension(cog_path)

        except commands.ExtensionFailed as error:
            log.warn(
                f"Could not load component '{cog_name}' "
                f"due to {error.__cause__}"
            )

        else:
            log.success(f"loaded {cog_name}")

    async def get_prefix(self, message):
        """Return current guild prefix"""
        if not message.guild:
            return self.default_prefix

        prefix_doc = (
            await collections.prefixes
            .find_one({"_id": message.guild.id})
        )

        if prefix_doc is None:
            return self.default_prefix

        return prefix_doc.get("prefix", self.default_prefix)

    async def on_connect(self) -> None:
        log.success(f"Logging in as {self.user}.")
        update_presence.start(self)

    async def get_context(self, message: Message, *, cls=TimedContext):
        return await super().get_context(message, cls=cls)

    async def on_ready(self) -> None:
        log.inform(f"{self.user} is ready for use.")

    if PREVENT_DOUBLE_RUNTIME_ERROR:
        def __del__(self) -> NoReturn:
            log.warn("Bot has been shutdown, cleaning stderr.")
            # Prevents RuntimeError when Ctrl-C.
            sys.stderr.close()
