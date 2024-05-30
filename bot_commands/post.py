import hikari, crescent

plugin = crescent.Plugin[hikari.GatewayBot, None]()

bot_admin_group = crescent.Group("post",
                                 default_member_permissions=hikari.Permissions.MANAGE_GUILD)

@plugin.include
@bot_admin_group.child
@crescent.command(name="rules")
async def post_rules(ctx: crescent.Context) -> None:
    await ctx.defer(ephemeral=True)
    import asyncio
    await asyncio.sleep(2)
    await ctx.channel.send("Rules")
    await ctx.respond(f"Posted rules in {ctx.channel.mention}.")
    