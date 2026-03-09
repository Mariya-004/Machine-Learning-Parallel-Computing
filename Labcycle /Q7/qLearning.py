import gym
from gym import spaces
import numpy as np, random, time

class MazeEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.maze=np.array([[0,0,0,0],[1,1,0,1],[0,0,0,1],[1,0,0,2]])
        self.start=(0,0); self.goal=(3,3); self.state=self.start
        self.action_space=spaces.Discrete(4)

    def reset(self):
        self.state=self.start
        return np.array(self.state)

    def step(self,a):
        moves=[(-1,0),(1,0),(0,-1),(0,1)]
        x=self.state[0]+moves[a][0]; y=self.state[1]+moves[a][1]
        if x<0 or y<0 or x>=4 or y>=4 or self.maze[x][y]==1:
            return np.array(self.state),-1,False,{}
        self.state=(x,y)
        if self.state==self.goal: return np.array(self.state),10,True,{}
        return np.array(self.state),-0.1,False,{}

    def render(self):
        g=self.maze.copy().astype(object)
        for i in range(4):
            for j in range(4):
                g[i][j]="." if g[i][j]==0 else "#" if g[i][j]==1 else "G"
        x,y=self.state; g[x][y]="A"
        print()
        for r in g: print(" ".join(r))

env=MazeEnv()
Q=np.zeros((4,4,4))

alpha,gamma,epsilon=0.1,0.9,0.2

# Training
for _ in range(400):
    s=env.reset(); done=False
    while not done:
        a=random.randint(0,3) if random.random()<epsilon else np.argmax(Q[s[0],s[1]])
        ns,r,done,_=env.step(a)
        Q[s[0],s[1],a]+=alpha*(r+gamma*np.max(Q[ns[0],ns[1]])-Q[s[0],s[1],a])
        s=ns

print("\nLearned Q-table:\n",Q)

# Test
s=env.reset()
env.render()

for _ in range(20):
    s,_,d,_=env.step(np.argmax(Q[s[0],s[1]]))
    env.render()
    time.sleep(0.4)
    if d:
        print("\nGoal Reached!")
        break
