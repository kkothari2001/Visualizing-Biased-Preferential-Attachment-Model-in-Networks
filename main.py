from manim import *
import random
from colour import Color

n = 15  # Number of vertices
r = 0.3  # Probability of a red node
col = [RED, BLUE]
rho = 0.5  # Degree of homophily


class MovingVertices(Scene):
    def construct(self):
        # Initializing the animation
        vertices = list(range(n))
        edges = []
        g = Graph(vertices, edges, layout="circular", layout_scale=3)
        for i in range(n):
            g[i].set_color(Color(BLACK))
        self.play(Create(g, run_time=0.1))
        self.wait()

        # Initializing the graph
        vc = []
        graph = []
        for i in range(n):
            graph.append([])

        # First 2 vertices being initialised
        vc.append(0)
        self.play(g[0].animate(run_time=0.2).set_color(RED))
        vc.append(1)
        self.play(g[1].animate(run_time=0.8).set_color(BLUE))
        graph[0].append(1)
        graph[1].append(0)
        self.play(g.animate(run_time=0.5).add_edges((1, 0)))

        # Each new vertex being added
        vset = [0, 1]
        for i in range(2, n):
            # Selecting a colour for the newest vertices with probability of red being r
            cch = random.choices([0, 1], weights=[r, 1-r], k=1)[0]
            vc.append(cch)
            self.play(g[i].animate(run_time=0.2).set_color(col[cch]))

            tdeg = 0
            for a in range(len(vset)):
                tdeg += len(graph[a])
            probs = []
            for a in range(len(vset)):
                probs.append(len(graph[a]) / tdeg)

            # Process of randomly selecting a neighbour from the probability distribution defined by the degree of the existing vertices
            match_found = False
            while not match_found:
                u = random.choices(vset, weights=probs, k=1)[0]
                if vc[u] == cch:
                    match_found = True
                    graph[i].append(u)
                    graph[u].append(i)
                    self.play(g.animate(run_time=0.5).add_edges((i, u)))
                else:
                    # Since the vertices were of a different colour, we now check if the edge can be made with the homophily contraint
                    rch = random.choices([0, 1], weights=[1-rho, rho], k=1)[0]
                    if rch:
                        match_found = True
                        graph[i].append(u)
                        graph[u].append(i)
                        self.play(g.animate(run_time=0.5).add_edges((i, u)))

            # Adding latest vertex to the set of exiting vertices
            vset.append(i)
        self.wait(10)
