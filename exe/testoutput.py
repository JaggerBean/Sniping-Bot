import tkinter as tk
from multiprocessing import Process, Queue
import time

def worker_process(queue):
    for i in range(10):
        time.sleep(1)
        queue.put(f"Message {i} from worker process")



def start_process():
    global worker
    worker = Process(target=worker_process, args=(message_queue,))
    worker.start()
    root.after(100, check_queue)

def check_queue():
    while not message_queue.empty():
        message = message_queue.get()
        text_widget.insert(tk.END, f"{message}\n")
    root.after(100, check_queue)


root = tk.Tk()

message_queue = Queue()

text_widget = tk.Text(root, wrap='word', height=10, width=40)
text_widget.pack(padx=10, pady=10)

start_button = tk.Button(root, text="Start Process", command=start_process)
start_button.pack(pady=10)

root.mainloop()