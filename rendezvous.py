import numpy as np
import math
import matplotlib.pyplot as plt

class Agent:
    def __init__(self, id, pos) -> None:
        self.id = id # an int corresponding to its index in the adjacency matrix
        self.pos = pos # a 2-dimensional vector representing its [x,y] position
        self.neighbors = [] # a list containing the ids of all the agent's neighbors. Only used for limited communication network agents
        self.num_neighbors = 0 # also known as the degree of the node in graph form

NUM_ITERS = 100
NEIGHBOR_RADIUS = 3
WORLD_SIZE = 5
NUM_AGENTS = 10
DT = 0.01

def get_neighbors(agents, agent_x):
    neighbors = []
    for agent_j in agents:
        if agent_j.id != agent_x.id:
            if math.dist(agent_j.pos, agent_x.pos) <= NEIGHBOR_RADIUS:
                neighbors.append(agent_j)
    return neighbors

fig = plt.figure(figsize=(WORLD_SIZE, WORLD_SIZE), dpi=96)
ax = plt.gca()

def display(agents):
    agent_x = []
    agent_y = []
    for agent in agents:
        agent_x.append(agent.pos[0])
        agent_y.append(agent.pos[1])
    plt.cla()
    plt.scatter(agent_x, agent_y)
    ax.set(xlim=(0, WORLD_SIZE), ylim=(0, WORLD_SIZE))
    ax.set_aspect('equal')
    plt.pause(0.1)

agents = []
prev_state = dict()
neighbor_matrix = np.zeros((NUM_AGENTS, NUM_AGENTS))

def build_agents():
    for i in range(0, NUM_AGENTS):
        pos = np.array([np.random.randint(0, WORLD_SIZE), np.random.randint(0, WORLD_SIZE)])
        agents.append(Agent(i, pos))
        prev_state.update({i: pos})
        # print("Agent {id}: {pos}\n".format(id=i, pos=pos))

"""Builds the graph laplacian with the signs flipped (-L)"""
def build_neighbor_matrix(): # randomize neighbors
    for i in range(0, NUM_AGENTS):
        for j in range(i, NUM_AGENTS):
            if i != j:
                if np.random.choice([0, 1]) == 1:
                    neighbor_matrix[i][j] = 1
                    neighbor_matrix[j][i] = 1
                    agents[i].neighbors.append(j)
                    agents[j].neighbors.append(i)
                    agents[i].num_neighbors += 1
                    agents[j].num_neighbors += 1
        print(agents[i].neighbors)
        neighbor_matrix[i][i] = -1 * agents[i].num_neighbors
    print(neighbor_matrix)

def main():
    build_agents()
    build_neighbor_matrix()
    for i in range(0, NUM_ITERS):
        # print("ITERATION: {iter}".format(iter=i))
        # update positions
        for agent in agents:
            prev_state.update({agent.id: agent.pos})
            # TODO: change the calculation of velocity to use the graph laplacian
            velocity = np.zeros_like(agent.pos)
            for neighbor in agent.neighbors:
                velocity += (prev_state.get(neighbor) - agent.pos)
            agent.pos = agent.pos + velocity * DT
            agent.pos[0] = agent.pos[0] % WORLD_SIZE # makes the agents loop back around the world if they go out of bounds
            agent.pos[1] = agent.pos[1] % WORLD_SIZE
            # print("Agent {id}: {pos}".format(id=agent.id, pos=agent.pos))

        display(agents)
    plt.show()

main()
