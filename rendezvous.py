import numpy as np
import math
import matplotlib.pyplot as plt

class Agent:
    def __init__(self, id, pos) -> None:
        self.id = id
        self.pos = pos

NUM_ITERS = 5
NEIGHBOR_RADIUS = 5
WORLD_SIZE = 5
NUM_AGENTS = 3

def get_neighbors(agents, agent_x):
    neighbors = []
    for agent_j in agents:
        if agent_j.id != agent_x.id:
            if math.dist(agent_j.pos, agent_x.pos) <= NEIGHBOR_RADIUS:
                neighbors.append(agent_j)
    return neighbors

fig, ax = plt.subplots(figsize=(WORLD_SIZE, WORLD_SIZE))

def display(agents):
    agent_x = []
    agent_y = []
    for agent in agents:
        agent_x.append(agent.pos[0])
        agent_y.append(agent.pos[1])
    plt.cla()
    ax.scatter(agent_x, agent_y)
    plt.show()

agents = []
prev_state = dict()
neighbor_matrix = np.zeros((NUM_AGENTS, NUM_AGENTS))

def build_agents():
    for i in range(0, NUM_AGENTS):
        pos = np.array([np.random.randint(0, WORLD_SIZE), np.random.randint(0, WORLD_SIZE)]) # np.random.randint(0, WORLD_SIZE)
        agents.append(Agent(i, pos))
        prev_state.update({i: pos})
        print("Agent {id}: {pos}\n".format(id=i, pos=pos))

def build_neighbor_matrix(): # randomize neighbors
    for i in range(0, NUM_AGENTS):
        for j in range(0, NUM_AGENTS):
            if i != j:
                neighbor_matrix[i][j] = np.random.choice([0, 1])
                neighbor_matrix[j][i] = neighbor_matrix[i][j]
    print(neighbor_matrix)

def main():
    build_agents()
    # build_neighbor_matrix()
    for i in range(0, NUM_ITERS):
        print("ITERATION: {iter}".format(iter=i))
        # update positions
        for agent in agents:
            neighbors = get_neighbors(agents=agents, agent_x=agent)
            dpos = np.zeros_like(agent.pos)
            for neighbor in neighbors:
                dpos += (prev_state.get(neighbor.id) - agent.pos) # (prev_state.get(neighbor.id) - agent.pos)
            agent.pos += dpos
            agent.pos[0] = agent.pos[0] % WORLD_SIZE
            agent.pos[1] = agent.pos[1] % WORLD_SIZE
            # agent.pos = agent.pos % WORLD_SIZE # constrain it to a world size
            print("Agent {id}: {pos}".format(id=agent.id, pos=agent.pos))

        for agent in agents:
            prev_state.update({agent.id: agent.pos})

        # display(agents)

main()
