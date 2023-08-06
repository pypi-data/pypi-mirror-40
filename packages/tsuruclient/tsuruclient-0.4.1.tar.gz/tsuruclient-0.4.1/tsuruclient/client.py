from tsuruclient import (apps, nodes, templates, pools,
                         machines, containers, events, users,
                         healings, plans, deploys)


class Client(object):
    def __init__(self, target, token):
        self.apps = apps.Manager(target, token)
        self.nodes = nodes.Manager(target, token)
        self.templates = templates.Manager(target, token)
        self.pools = pools.Manager(target, token)
        self.machines = machines.Manager(target, token)
        self.containers = containers.Manager(target, token)
        self.events = events.Manager(target, token)
        self.users = users.Manager(target, token)
        self.healings = healings.Manager(target, token)
        self.plans = plans.Manager(target, token)
        self.deploys = deploys.Manager(target, token)
