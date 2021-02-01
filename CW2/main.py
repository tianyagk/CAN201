import os
import socket
import json
import time
import argparse

NEXT_HOP = 'next_hop'
NEIGHBOUR = 'neighbour'
DISTANCE = 'distance'

parser = argparse.ArgumentParser(description='Input the start node')
parser.add_argument("--node", help='node name')


def update_news(sock, this_node, this_node_ip, dv):
    for neighbor in this_node_ip.keys():
        if neighbor is not this_node:
            neighbor_info = this_node_ip.get(neighbor)  # List like ['127.0.0.1', 10003]
            # Sign on the dv
            sock.sendto(json.dumps({this_node: dv}).encode(), (neighbor_info[0], neighbor_info[1]))


def main(this_node):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    count = 0

    # distance vector
    with open(f"{this_node}_distance.json", "r")as f:
        this_node_dis = json.loads(f.read())  # dict
        # turns the key, value to a list
        keys, values = zip(*this_node_dis.items())
        nodes = keys
        distance = values

        dv = {}
        for i in range(len(nodes)):
            dv[keys[i]] = {"distance": values[i], NEXT_HOP: keys[i]}

        print(dv)

    # ip vector
    with open(f"{this_node}_ip.json", "r") as f:
        this_node_ip = json.loads(f.read())

    sock.bind((this_node_ip[this_node][0], this_node_ip[this_node][1]))
    print(f"Bind to ip: {this_node_ip[this_node][0]}, port: {this_node_ip[this_node][1]}")

    time.sleep(3)

    while count < 10:
        update_news(sock, this_node, this_node_ip, dv)
        dv_copy = dv.copy()

        for neighbor in this_node_ip.keys():
            if neighbor is not this_node:
                dv_receive = json.loads(sock.recv(1024).decode())
                sender = list(dv_receive.keys())[0]
                dv_receive = dv_receive.get(sender)

                for node in dv_receive:
                    distance = dv_receive[node].get("distance") + dv[sender].get("distance")
                    if node not in dv.keys():
                        dv[node] = {"distance": distance, "next_hop": sender}
                    else:
                        if distance < dv[node].get("distance"):
                            dv[node] = {"distance": distance, "next_hop": sender}

        # If dv doesn't change, then count increases
        if dv == dv_copy:
            count += 1

    del dv[this_node]
    with open(f"{this_node}_output.json", "w") as f:
        f.write(json.dumps(dv))


if __name__ == "__main__":
    args = parser.parse_args()
    node = args.node

    print(f"Start work {node}")
    main(node)



