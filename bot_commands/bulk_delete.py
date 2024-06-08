import hikari, crescent, re
from bot_variables import state
from bot_variables.config import RolePermissions
# from wrappers.discord import get_channel_by_name

plugin = crescent.Plugin[hikari.GatewayBot, None]()
# admin ang higher level access only
delete_group = crescent.Group("delete", default_member_permissions=RolePermissions.ADMIN)
# bulk subgroup
bulk_subgroup = delete_group.sub_group("bulk")
    



@plugin.include
@delete_group.child
@crescent.command(name="role")
class DeleteRole:
    role = crescent.option(hikari.Role)
    async def callback(self, ctx: crescent.Context) -> None:
        await ctx.defer(ephemeral=True)
        await delete_role(self.role)
        await ctx.respond('deleted', ephemeral=True)
            
            
async def delete_role(role: hikari.Role):
    name = role.name.lower()
    if not re.match("sec-[0-9]{2}(|-lab)", name):
        print(f"{name} is not a section role.")
        return
    if re.match("sec-01(|-lab)", name):
        print(f"Can't delete {name} since it works as template.")
        return
    print(f"Deleting {role.mention} {role}...")
    await plugin.app.rest.delete_role(state.guild, role)



@plugin.include
@delete_group.child
@crescent.command(name="category")
class DeleteCategory:
    category = crescent.option(hikari.GuildCategory)
    async def callback(self, ctx: crescent.Context) -> None:
        await ctx.defer(ephemeral=True)
        await delete_category(self.category)
        await ctx.respond('deleted', ephemeral=True)

            
async def delete_category(category: hikari.GuildCategory):
    name = category.name.upper()
    if category.type != hikari.ChannelType.GUILD_CATEGORY:
        print(f"{name} is not a category.")
        return
    if not re.match("SECTION [0-9]{2} (THEORY|LAB)", name):
        print(f"{name} is not a section category.")
        return
    if re.match("SECTION 01 (THEORY|LAB)", name):
        print(f"Can't delete {name} since it works as template.")
        return
    for _, channel in state.guild.get_channels().items():
        if channel.parent_id == category.id:
            print(f"Deleting {channel.mention} {channel}...")
            await channel.delete()
    print(f"Deleting {category.mention} {category}...")
    await category.delete()
    
    
    

@plugin.include
@bulk_subgroup.child
@crescent.command(name="roles", description="Bulk delete all section roles.")
class DeleteBulkRoles:
    BULK_DELETE_PROMPT = "yes"#"Confirm bulk deletion!"
    confirm = crescent.option(str, 
                              f"Type in `{BULK_DELETE_PROMPT}` exactly to confirm.")
    async def callback(self, ctx: crescent.Context) -> None:
        await ctx.defer(ephemeral=True)
        if self.confirm == self.BULK_DELETE_PROMPT:
            for _, role in state.guild.get_roles().items():
                await delete_role(role)
            await ctx.respond("Deleted all section channels", ephemeral=True)
        else:
            msg = "Confimation text did not match prompt:\n"
            msg += f"```diff\n+ {self.BULK_DELETE_PROMPT}\n"
            msg += f"- {self.confirm}\n```"
            await ctx.respond(msg, ephemeral=True)    
    
    

@plugin.include
@bulk_subgroup.child
@crescent.command(name="categories", description="Bulk delete all section channels.")
class DeleteBulkCategories:
    BULK_DELETE_PROMPT = "yes"#"Confirm bulk deletion!"
    confirm = crescent.option(str, 
                              f"Type in `{BULK_DELETE_PROMPT}` exactly to confirm.")
    async def callback(self, ctx: crescent.Context) -> None:
        await ctx.defer(ephemeral=True)
        if self.confirm == self.BULK_DELETE_PROMPT:
            for _, channel in state.guild.get_channels().items():
                await delete_category(channel)
            await ctx.respond("Deleted all section channels", ephemeral=True)
        else:
            msg = "Confimation text did not match prompt:\n"
            msg += f"```diff\n+ {self.BULK_DELETE_PROMPT}\n"
            msg += f"- {self.confirm}\n```"
            await ctx.respond(msg, ephemeral=True)
            