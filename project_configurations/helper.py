# Function for read and load bootstrap commands
def load_bootstrap(file):
    with open(file) as f2:
        commands = []
        for line in f2:
            commands.append(line)
    #print(commands)
    return commands


