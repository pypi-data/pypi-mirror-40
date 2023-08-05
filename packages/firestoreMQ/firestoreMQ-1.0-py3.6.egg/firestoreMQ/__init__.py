import datetime
import google.api_core.exceptions
import time

class Task:
    errored_collection = 'errored'
    assigned_collection = 'assigned'
    unassigned_collection = 'unassigned'

    '''Static method create a task from a doc'''
    def from_doc(doc):
        dict = doc.to_dict()

        return Task(dict.queue, dict.data, dict.ttl, doc.id, doc.ref, dict.assigned_to)

    def __init__(self, queue, data, ttl=None, id=None, ref=None, assigned_to=None):
        self.queue = queue
        self.data = data
        self.ttl = ttl
        self.id = id
        self.ref = ref
        self.assigned_to = assigned_to

    def to_dict(self):
        task_dict = {
            'created': datetime.datetime.now(),
            'data': self.data,
            'ttl': None,
            'assigned_to': None
        }

        if self.ttl is not None:
            task_dict['ttl'] = task_dict['created'] + datetime.timedelta(seconds=self.ttl)

        if self.assigned_to is not None:
            task_dict['assigned_to'] = self.assigned_to

        return task_dict

    '''Add a task to a queue'''
    def create(self, db):
        self.ref = db.collection('queues').document(self.queue).collection(Task.unassigned_collection).document();
        self.id = self.ref.id
        self.ref.create(self); # TODO create if dosen't exist?

    '''Assign to a worker
    Returns Boolean - True if assign successful
    '''
    def assign(self, db, worker_id):
        self.ref.delete()
        self.assigned_to = worker_id
        new_ref = db.collection('queues').document(self.queue).collection(Task.assigned_collection).document(self.id);
        try:
            new_ref.create(self)
            self.ref = new_ref
        except google.api_core.exceptions.AlreadyExists:
            return False

        return True

    '''Remove the current document'''
    def complete(self, db):
        self.ref.delete()

    def error(self, db):
        self.ref.delete()
        self.ref = db.collection('queues').document(self.queue).collection(Task.errored_collection).document(self.id);
        self.ref.create(self);

    def __repr__(self):
        if self.id is None:
            return 'new task'
        else:
            return self.id

'''Blocking call for next task'''
def next_task(db, queue, worker_id, poll_interval=2):
    while True:
        # .orderBy('created', 'asc')
        docs = db.collection('queues').document(queue).collection(Task.unassigned_collection).orderBy('priority', 'desc').get()

        # TODO if docs empty?

        for task_doc in docs:
            task = Task.from_doc(task_doc)

            # Try and assign to this worker
            success = task.assign(db, worker_id)
            if success:
                return task

        time.sleep(poll_interval)

