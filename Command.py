class Command:
    def __init__(self, name: str, description: str, arguments: list, aliases: list):
        self.name = name
        self.description = description
        self.arguments = arguments
        self.aliases = aliases


    def getCommandData(self):
        if self.arguments == []:
            object_arguments = "None"
        else:
            object_arguments = (" ").join(self.arguments)

        if self.aliases == []:
            object_aliases = "None"
        else:
            object_aliases = (" ").join(self.aliases)

        return f"{self.name}:\n  Description: {self.description}\n  Arguments: {object_arguments}\n  Aliases: {object_aliases}"


    def matches(self, input: str):
        if input == "":
            return

        if str(input).startswith(self.name):
            return True
        else:
            if input.split()[0].strip() in self.aliases:
                return True
            else:
                return False


    def checkAllArguments(self, command_arguments: str):
        valid_arguments = 0

        if len(command_arguments) != len(self.arguments):
            return "ERROR"

        for i in range(len(command_arguments)):
            if (str(self.arguments[i]).startswith("<")) and (str(self.arguments[i]).endswith(">")):
                if str(command_arguments[i]).strip() == ("" or None):
                    return "ERROR"
                else:
                    valid_arguments += 1
            elif (str(self.arguments[i]).startswith("[")) and (str(self.arguments[i]).endswith("]")):
                valid_arguments += 1
            else:
                return "ERROR"

        if valid_arguments == len(command_arguments):
            return "SUCCESS"
        else:
            return "ERROR"