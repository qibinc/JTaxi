from pipe import Pipe
cproc = Pipe('./core')


def optimalOrder(passengers, taxi):
    cproc.send({
        'name': 'optimalOrder',
        'passengers': passengers,
        'taxi': taxi
    })
    return cproc.recv()


def optimalOrderRoute(passengers, taxi):
    cproc.send({
        'name': 'optimalOrderRoute',
        'passengers': passengers,
        'taxi': taxi
    })
    return cproc.recv()


def wholePath(nodes):
    cproc.send({
        'name': 'wholePath',
        'nodes': nodes
    })
    return cproc.recv()


def searchTaxi(s_node, t_node, k_taxis):
    cproc.send({
        'name': 'searchTaxi',
        's': s_node,
        't': t_node,
        'k': k_taxis
    })
    return cproc.recv()
