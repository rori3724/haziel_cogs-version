import os
def AutoCogs(self):
    cogs = []
    for i in os.listdir('./cogs'):
        if i.endswith('.py'):
            cogs.append(i.replace(".py", ""))
    for i in cogs:
        self.load_extension(f'cogs.{i}')

def AutoCogsReload(self):
    cogs = []
    for i in os.listdir('./cogs'):
        if i.endswith('.py'):
            cogs.append(i.replace(".py", ""))
    for i in cogs:
        self.reload_extension(f'cogs.{i}')