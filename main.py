import os
import socket
import json
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


def main():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    count = 0
    this_node = node_name

    # distance vector
    with open(f"{node_name}_distance.json", "r")as f:
        this_node_dis = json.loads(f.read())  # dict
        # turns the key, value to a list
        keys, values = zip(*this_node_dis.items())
        nodes = keys
        distance = values

        dv = {}
        for i in range(len(nodes)):
            dv[keys(i)] = {"distance": distance(i), NEXT_HOP: keys(i)}

    # ip vector
    with open(f"{node_name}_ip.json", "r") as f:
        this_node_ip = json.loads(f.read())

    sock.bind((this_node_ip[this_node][0], this_node_ip[this_node][1]))

    while count < 10:
        update_news(sock, this_node, this_node_ip, dv)
        dv_copy = dv.copy()

        for neighbor in this_node_ip.keys():
            if neighbor is not this_node:
                dv_receive = json.loads(sock.recv(1024).decode())
                sender = dv_receive.keys()[0]
                dv_receive = dv_receive.get(sender)

                for node in dv_receive:
                    distance = dv_receive[node].get("distance") + dv[sender].get("distance")
                    if node not in dv.keys():
                        dv[node] = {"distance": distance, "next_hop": sender}
                    else:
                        if distance < dv[node].get("distance"):
                            dv[node] = {"distance": distance, "next_hop": sender}

        # 如果dv没有变化，则count增加
        if dv == dv_copy():
            count += 1
        

    with open(f"{node_name}_output.json", "w") as f:
        f.write(json.dumps(dv))


if __name__ == "__main__":
    args = parser.parse_args()
    node_name = args.node
    update_news()



