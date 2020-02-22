help_help = """
help    Displays help dialogs.
        Arguments:
        []          Displays this help.
        [Command]   Displays help for a command."""

help_exit = """
exit    Exits the program, prompting for a save first."""

help_commit = """
commit  Saves and instantly exits the program."""

help_save = """
save    Saves all changes made to the Everything file."""

help_todo = """
todo    Lists todo items.
        Arguments:
        []                      Displays all items on todo list.
        today                   Displays all items due today.
        week                    Displays all items due by 7 days from today or before today.
        add [item]              Adds the given item to the todo list for today.
        add [item] [iso date]   Adds the given item to the todo list at the specified date."""

help_finish = """
finish  Checks an item off the todo list, finishing it.
        Arguments:
        [number]    Required number, indicating which item on the todo list to complete."""

help_get = """
get     Gets various lists and aggregates.
        Arguments:
        people          Lists all people known to the Everything file.
        [iso date]      Gets the day's entry for a specified date.
        today           Gets the day's entry for today.
        facts [person]  Gets facts about a specific person.
                        Requires the second argument."""

help_all = 'Commands:\n' + help_help + help_exit + help_save + help_commit + help_save + help_todo + \
    help_finish + help_get

get_help = {
    '': help_all,
    None: help_all,
    'help': help_help,
    '?': help_help,
    'exit': help_exit,
    'quit': help_exit,
    'commit': help_commit,
    'save': help_save,
    'todo': help_todo,
    'finish': help_finish,
    'get': help_get,
}
