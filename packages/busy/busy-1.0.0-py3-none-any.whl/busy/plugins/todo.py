from ..queue import Queue
from ..item import Item
from ..file import File
from ..commander import Command
from ..commander import Commander
import busy.future
import busy
from ..future import date_for

TODO_STATE = 't'
PLAN_STATE = 'p'
DONE_STATE = 'd'

class Task(Item):

    def __init__(self, description=None, plan_date=None):
        super().__init__(description)
        self._state = TODO_STATE
        if plan_date: self.as_plan(plan_date)

    def as_plan(self, date):
        self._state = PLAN_STATE
        self._plan_date = busy.future.absolute_date(date)
        return self

    def as_todo(self):
        self._state = TODO_STATE
        return self

    @property
    def plan_date(self):
        return self._plan_date

    @property
    def project(self):
        tags = self.tags
        return tags[0] if tags else None


class TodoQueue(Queue):
    itemclass = Task
    key = 'todo'

    def __init__(self, manager=None):
        super().__init__(manager)
        self.plans = manager.get_queue('plan') if manager else PlanQueue()

    def defer(self, date, *criteria):
        indices = self.select(*(criteria or [1]))
        plans = [self.get(i+1).as_plan(date) for i in indices]
        self.plans.add(*plans)
        self.delete_by_indices(*indices)

    def activate(self, *criteria, today=False):
        if today:
            func = lambda t: t.plan_date <= busy.future.today()
            indices = self.plans.select(func)
        else:
            indices = self.plans.select(*criteria)
        tasks = [self.plans.get(i+1).as_todo() for i in indices]
        self.add(*tasks, index=0)
        self.plans.delete_by_indices(*indices)

Queue.register(TodoQueue, default=True)


class PlanQueue(Queue):
    itemclass = Task
    key = 'plan'
    schema = ['plan_date', 'description']
    listfmt = "{1.plan_date:%Y-%m-%d}  {1.description}"

Queue.register(PlanQueue)


class TodoCommand(Command):

    def execute(self, parsed):
        return self.execute_todo(parsed, self._root.get_queue(TodoQueue.key))


class DeferCommand(TodoCommand):

    command = 'defer'

    @classmethod
    def register(self, parser):
        parser.add_argument('--to','--for',dest='time_info')

    def execute_todo(self, parsed, queue):
        tasklist = queue.list(*parsed.criteria or [1])
        indices = [i[0]-1 for i in tasklist]
        if hasattr(parsed, 'time_info') and parsed.time_info:
            time_info = parsed.time_info
        else:
            print('\n'.join([str(i[1]) for i in tasklist]))
            time_info = input('Defer to [tomorrow]: ').strip() or 'tomorrow'
        queue.defer(date_for(time_info), *parsed.criteria)

Commander.register(DeferCommand)


class ActivateCommand(TodoCommand):

    command = 'activate'

    @classmethod
    def register(self, parser):
        parser.add_argument('--today','-t', action='store_true')

    def execute_todo(self, parsed, queue):
        if hasattr(parsed, 'today') and parsed.today:
            queue.activate(today=True)
        else:
            queue.activate(*parsed.criteria)

Commander.register(ActivateCommand)


class StartCommand(TodoCommand):

    command = 'start'

    @classmethod
    def register(self, parser):
        parser.add_argument('project', action='store', nargs='?')

    def execute_todo(self, parsed, queue):
        if parsed.criteria:
            raise RuntimeError('Start takes only an optional project name')
        queue.activate(today=True)
        if queue.count() < 1:
            raise RuntimeError('There are no active tasks')
        project = parsed.project or queue.get().project
        if not project:
            raise RuntimeError('The `start` command required a project')
        queue.manage(project)
        result = queue.pop(project)


Commander.register(StartCommand)
