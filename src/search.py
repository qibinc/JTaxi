from pprint import pprint
import numpy as np
from api import *
NODE_FILE = '../data/road.cnode'
EDGE_FILE = '../data/road.nedge'
CAR_FILE = '../data/car.txt'
R_earth = 6371000.0


def read_lines(fname):
    with open(fname) as f:
        lines = f.read().split('\n')[:-1]
        return lines


def load_nodes():
    lines = read_lines(NODE_FILE)
    N = len(lines)
    geo = np.zeros((N, 2))
    for i, line in enumerate(lines):
        x = line.split()
        geo[i] = float(x[1]), float(x[2])
    return geo.shape[0], geo


def load_edges():
    lines = read_lines(EDGE_FILE)
    assert int(lines[0].split()[1]) == len(lines) - 1
    lines = lines[1:]
    edges = [[] for i in range(N_NODES)]
    for i, line in enumerate(lines):
        fr, to, w = [int(num) for num in line.split()]
        edges[fr].append((to, w))
    return edges


N_NODES, nodes_geo = load_nodes()
nodes_inout_edges = load_edges()


def load_taxis():
    lines = read_lines(CAR_FILE)
    N_TAXIS = len(lines)
    taxi_pos = np.zeros(N_TAXIS, dtype=int)
    taxi_passengers_pos = [[] for i in range(N_TAXIS)]
    taxis_on_node = [[] for i in range(N_NODES)]
    for i, line in enumerate(lines):
        nums = line.split()
        assert int(nums[1]) == len(nums) - 3
        taxi_pos[i] = int(nums[2].split(',')[-1])
        taxis_on_node[taxi_pos[i]].append(i)
        for num in nums[3:]:
            taxi_passengers_pos[i].append(int(num.split(',')[-1]))
    return N_TAXIS, taxi_pos, taxi_passengers_pos, taxis_on_node


N_TAXIS, taxi_pos, taxi_passengers_pos, taxis_on_node = load_taxis()


def distance(a1, b1, a2, b2):
    if b1 < 0:
        b1 = abs(b1) + 180
    if b2 < 0:
        b2 = abs(b2) + 180
    a1 = a1 * np.pi / 180
    b1 = b1 * np.pi / 180
    a2 = a2 * np.pi / 180
    b2 = b2 * np.pi / 180
    x = R_earth * np.cos(b1) * np.cos(a1) - R_earth * np.cos(b2) * np.cos(a2)
    y = R_earth * np.cos(b1) * np.sin(a1) - R_earth * np.cos(b2) * np.sin(a2)
    z = R_earth * np.sin(b1) - R_earth * np.sin(b2)
    AB = np.sqrt(x * x + y * y + z * z)
    A_B = 2 * np.arcsin(AB / (2 * R_earth)) * R_earth
    return A_B


a2 = nodes_geo[:, 0]
b2 = np.array(
    list(map(lambda x: abs(x) + 180 if x < 0 else x, nodes_geo[:, 1])))
a2 = a2 * np.pi / 180
b2 = b2 * np.pi / 180
cache_x2 = R_earth * np.cos(b2) * np.cos(a2)
cache_y2 = R_earth * np.cos(b2) * np.sin(a2)
cache_z2 = R_earth * np.sin(b2)


def cached_distance_make(a1, b1):
    if b1 < 0:
        b1 = abs(b1) + 180
    a1 = a1 * np.pi / 180
    b1 = b1 * np.pi / 180
    x1 = R_earth * np.cos(b1) * np.cos(a1)
    y1 = R_earth * np.cos(b1) * np.sin(a1)
    z1 = R_earth * np.sin(b1)
    return x1, y1, z1


def cached_distance(cache, i):
    x1, y1, z1 = cache
    x = x1 - cache_x2[i]
    y = y1 - cache_y2[i]
    z = z1 - cache_z2[i]
    AB = np.sqrt(x * x + y * y + z * z)
    A_B = 2 * np.arcsin(AB / (2 * R_earth)) * R_earth
    return A_B


def nearest_node(lngt, lat):
    min_dis = 10000000
    cache = cached_distance_make(lngt, lat)
    for i in range(N_NODES):
        dis = cached_distance(cache, i)
        if dis < min_dis:
            min_dis = dis
            ret = i
    return ret


if __name__ == '__main__':
    while True:
        # line = input("Input 打车经纬度\n").split()
        # src_lngt, src_lat, des_lngt, des_lat = map(float, line)
        # src_lngt, src_lat, des_lngt, des_lat = 115, 38, 130, 50
        # src_node = nearest_node(src_lngt, src_lat)
        # des_node = nearest_node(des_lngt, des_lat)
        src_node, des_node = 288218, 288220
        taxis_rets = searchTaxi(src_node, des_node, 6)
        print('found taxis:')
        pprint(taxis_rets)
        taxis = map(lambda x: x['id'], taxis_rets)
        for taxi in taxis:
            passengers = taxi_passengers_pos[taxi].copy()
            passengers.append(des_node)
            order = optimalOrderRoute(passengers, taxi)
            order = [taxi, src_node] + order
            for node in order:
                print(nodes_geo[node])
            route = wholePath(order)
        break
