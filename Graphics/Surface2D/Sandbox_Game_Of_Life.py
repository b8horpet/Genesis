import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

N=20
fig = plt.figure(figsize=(5,5))
world = np.zeros((N,N),np.byte)
#world[2,0]=1
#world[2,1]=1
#world[2,2]=1
#world[1,2]=1
#world[0,1]=1
for i in range(0,N):
    for j in range(0,N):
        world[i,j]=np.random.choice((0,1))
backworld = world.copy()


p = plt.scatter([],[],200,"000000",marker='s')
plt.axis([0,N,0,N])

def updateworld():
    global world,backworld
    for i in range(0,N):
        for j in range(0,N):
            im1=(i-1)%N
            ip1=(i+1)%N
            jm1=(j-1)%N
            jp1=(j+1)%N
            c=world[im1,jm1]+world[i,jm1]+world[ip1,jm1]+world[im1,j]+world[i,j]+world[ip1,j]+world[im1,jp1]+world[i,jp1]+world[ip1,jp1]
            if c==3:
                backworld[i,j]=1
            elif c==4:
                backworld[i,j]=world[i,j]
            else:
                backworld[i,j]=0
    t=backworld
    backworld=world
    world=t


def update(tick):
    updateworld()
    l=[]
    for i in range(0,N):
        for j in range(0,N):
            if world[i,j]==1:
                l.append((i+.5,j+.5))
    p.set_offsets(l)
    return p,


if False:
    anim=animation.FuncAnimation(fig,update,interval=100,frames=200)
    anim.save('game_of_life.gif', writer='imagemagick', fps=10, dpi=40)
else:
    anim=animation.FuncAnimation(fig,update,interval=100)
    plt.show()