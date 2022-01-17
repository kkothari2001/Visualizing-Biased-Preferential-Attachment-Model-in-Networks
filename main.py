from functools import reduce
from colour import Color
from manim import *
import random

n = 15
r = 0.3
col = [RED, BLUE]
rho = 0.5


class MovingVertices(Scene):
    def construct(self):
        vertices = list(range(n))
        edges = []
        g = Graph(vertices, edges, layout="circular", layout_scale=3)
        for i in range(n):
            g[i].set_color(Color(BLACK))
        self.play(Create(g, run_time=0.1))
        self.wait()

        vc = []
        graph = []
        for i in range(n):
            graph.append([])

        vc.append(0)
        self.play(g[0].animate(run_time=0.2).set_color(RED))
        vc.append(1)
        self.play(g[1].animate(run_time=0.8).set_color(BLUE))
        graph[0].append(1)
        graph[1].append(0)
        self.play(g.animate(run_time=0.5).add_edges((1, 0)))

        vset = [0, 1]
        for i in range(2, n):
            cch = random.choices([0, 1], weights=[r, 1-r], k=1)[0]
            vc.append(cch)
            self.play(g[i].animate(run_time=0.2).set_color(col[cch]))

            tdeg = 0
            for a in range(len(vset)):
                tdeg += len(graph[a])

            probs = []
            for a in range(len(vset)):
                probs.append(len(graph[a]) / tdeg)

            mf = False
            while not mf:
                u = random.choices(vset, weights=probs, k=1)[0]
                if vc[u] == cch:
                    mf = True
                    graph[i].append(u)
                    graph[u].append(i)
                    self.play(g.animate(run_time=0.5).add_edges((i, u)))
                else:
                    rch = random.choices([0, 1], weights=[1-rho, rho], k=1)[0]
                    if rch:
                        mf = True
                        graph[i].append(u)
                        graph[u].append(i)
                        self.play(g.animate(run_time=0.5).add_edges((i, u)))
            vset.append(i)
        self.wait()
