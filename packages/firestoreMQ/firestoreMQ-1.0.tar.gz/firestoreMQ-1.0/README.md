# Firestore MQ Python Libary
## Install
`python3 setup.py install`

Note that watching the queue requires an index, please run `examples/worker.py` to create the index

## Examples
See `examples/` for example scripts

### Add a new task
```Python
import firestoreMQ
from firebase_admin import firestore

db = firestore.client() # TODO requires project initalisation

queue = "process_images"
data = {
  "image_path": "/path/to/images.png"
}
ttl = 3600 # seconds (optional)
priority = 0 # Higher priroty is higher number  (optional)

task = firestoreMQ.Task(queue, data, ttl=ttl, priority=priority)
task.create(db)
```

### Process tasks
```Python
import firestoreMQ
import time
from firebase_admin import firestore

db = firestore.client() # TODO requires project initalisation

worker_id = "worker_1" # Unique worker ID (NOTE one per worker instance)
queue = "process_images"

while True:
  task = firestoreMQ.next_task(db, queue, worker_id) # Blocking call for next task

  if 'image_path' in task.data:
    print(task.data['image_path'])
    time.sleep(1)
    task.complete(db)
  else:
    print('[Task %s] Invalid task data - No "image_path"' % task.id)
    task.error(db)
```