
class Enforcement_Handler():
    def __init__(self, bot):
        self.bot = bot

    def enforce(self, role: discord.Role = None, member: discord.Member = None):
        print("Attempting to enforce " + member.display_name + " due to role " + role.name)
        #Find the identity that corresponds with the role.