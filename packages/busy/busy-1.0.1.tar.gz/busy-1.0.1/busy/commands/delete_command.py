from ..commander import QueueCommand
from ..commander import Commander

class DeleteCommand(QueueCommand):

    command = 'delete'

    @classmethod
    def register(self, parser):
        super().register(parser)
        parser.add_argument('--yes', action='store_true')

    def execute_on_queue(self, parsed, queue):
        itemlist = queue.list(*parsed.criteria or [1])
        indices = [i[0]-1 for i in itemlist]
        if hasattr(parsed, 'yes') and parsed.yes:
            confirmed = True
        else:
            print('\n'.join([str(i[1]) for i in itemlist]))
            confirmed = input('Delete? (Y/n) ').startswith('Y')
        if not confirmed:
            print("Deletion must be confirmed")
        else:
            queue.delete_by_indices(*indices)

Commander.register(DeleteCommand)
