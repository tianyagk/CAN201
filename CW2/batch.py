import threading
import os 

def func(node):
    os.system(f'python main.py --node {node}')

threads = []

nodes = ["x", "v", "w", "u"]
for item in nodes:
    threads.append(threading.Thread(target=func,args=(item,)))

for t in threads:
    t.start()