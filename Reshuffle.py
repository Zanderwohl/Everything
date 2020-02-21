import Parse
import Console

Parse.backup_file()

roots, person_manager = Parse.parse_everything()
todo = Parse.get_todo(roots)

Console.save(roots, todo)
