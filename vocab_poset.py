import networkx as nx
import re
# md = 'ps' for all

def link_to_parents(G,pos,parents_and_vals,pos_ind=None):
    if pos_ind is None:
        pos_ind = max([int(re.sub("[^0-9]", "", node)) for node in G.nodes() if (pos + re.sub("[^0-9]", "", node)==node)], default=0)+1
    newnodename=pos+str(pos_ind)
    G.add_node(newnodename,pos=pos)
    G.add_edges_from([(pair[0],newnodename,{'att':pair[1]}) for pair in parents_and_vals])
    print(f"Created node named {newnodename} with pos={pos}.")


G=nx.DiGraph()

name1='Devon'
name2='Barbara'

seed1='politics'
seed2='politics student nonprofit activism'

G.add_node('name1',root=True,val=name1)
G.add_node('name2',root=True,val=name2)
G.add_node('seed1',root=True,val=seed1)
G.add_node('seed2',root=True,val=seed2)


#n1
link_to_parents(G,'n',[('name1','rel_rhy'),('seed2','topics')])
#adj1
link_to_parents(G,'adj',[('n1','rc')])
#v1
link_to_parents(G,'v',[('n1','rel_rhy'),('seed1','topics')])
#adv1
link_to_parents(G,'adv',[('adj1','sl'),('v1','rc'),('seed2','topics')])
#v2
link_to_parents(G,'v',[('n1','sl'),('v1','lc')])
#adv2
link_to_parents(G,'adv',[('adj1','sl'),('v2','rc')])


#n2
link_to_parents(G,'n',[('name2','rel_rhy'),('seed2','topics')])
#adj2
link_to_parents(G,'adj',[('n2','rc')])
#v3
link_to_parents(G,'v',[('n2','rel_rhy'),('seed1','topics')])
#adv3
link_to_parents(G,'adv',[('adj2','sl'),('v3','rc'),('seed2','topics')])
#v4
link_to_parents(G,'v',[('n2','sl'),('v3','lc')])
#adv4
link_to_parents(G,'adv',[('adv3','sl'),('v4','rc')])



# import matplotlib.pyplot as plt
# nx.draw_networkx(G)
# plt.show()
