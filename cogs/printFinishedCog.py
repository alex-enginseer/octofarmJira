from discord.ext import tasks, commands


class printFinishedCog(commands.Cog):
    def __init__(self, bot):
        self.index = 0
        self.printer.start()

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=5)
    async def printer(self):
        # print(self.index)
        self.index += 1


def setup(bot):
    bot.add_cog(printFinishedCog(bot))
