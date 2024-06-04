import hikari, crescent

plugin = crescent.Plugin[hikari.GatewayBot, None]()

# faculty_post_group = crescent.Group("publish", default_member_permissions=RolePermissions.FACULTY)

# @plugin.include
# @faculty_post_group.child
# @crescent.command(name="marks")
# async def post_marks(ctx: crescent.Context) -> None:
#     await ctx.defer(ephemeral=True)
#     await ctx.respond(f"Not implemented yet.")