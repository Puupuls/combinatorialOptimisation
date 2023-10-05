import random
from copy import deepcopy
from datetime import datetime
from threading import Thread
from time import sleep

import numpy as np

from my_types import Point, Domain, Solution, GraphNode


def create_test_domain():
    domain = Domain()
    domain.points.append(
        Point(
            x=0,
            y=0,
        )
    )
    domain.points.append(
        Point(
            x=150,
            y=50,
        )
    )
    domain.points.append(
        Point(
            x=350,
            y=-200,
        )
    )
    domain.points.append(
        Point(
            x=100,
            y=250,
        )
    )
    domain.points.append(
        Point(
            x=50,
            y=250,
        )
    )
    domain.points.append(
        Point(
            x=400,
            y=150,
        )
    )
    domain.points.append(
        Point(
            x=250,
            y=50,
        )
    )
    domain.time_limit = 1700
    return domain


class Optimizer(Thread):
    def __init__(self, domain):
        super().__init__()
        self.domain: Domain = domain
        self.fill_distances()
        self.is_running = False

    def fill_distances(self):
        points = self.domain.points
        distances = [[0] * len(points) for i in range(len(points))]
        for i, point1 in enumerate(points):
            for j, point2 in enumerate(points):
                dst = ((point1.x-point2.x)**2 + (point1.y-point2.y)**2) ** 0.5
                distances[i][j] = dst
        self.domain.distances = distances

    def get_starting_solution(self) -> Solution:
        # Iegūstam alkatīgo risinājumu izvēloties tuvāko neapmeklēto punktu līdz izveidots aplis
        solution = Solution()
        solution.links = [[0] * len(self.domain.points) for i in range(len(self.domain.points))]
        # return solution
        cur_point = self.domain.start_point_idx
        seen_points = [cur_point]
        while True:
            distances = deepcopy(self.domain.distances[cur_point])
            # Neiesim uz punktu kurā jau esam
            distances[cur_point] = -1

            # Neiesim uz jau aplūkotu punktu
            for i in seen_points:
                # Neļaujam iet uz finišu kamēr visi pārējie punkti nav apstaigāti
                if i != self.domain.finish_point_idx \
                        or len(seen_points) <= len(self.domain.points)-1:
                    distances[i] = -1

            # Atrodam mazāko nenegatīvo vērtību un ejam uz to
            min_dst = min([i for i in distances if i >= 0])
            min_idx = distances.index(min_dst)
            solution.links[cur_point][min_idx] = 1
            cur_point = min_idx
            seen_points.append(cur_point)

            # Ja esam nonākuši finišā, un viss ir apmeklēts, tad beidzam
            if cur_point == self.domain.finish_point_idx:
                break
        return solution

    def get_next_solutions(self, solution: Solution, n: int) -> list[Solution]:
        i = 0
        solutions = []
        solutions_used = set()
        while i < n:
            sol = Solution()
            sol.links = deepcopy(solution.links)
            for y in sol.links:
                for x, v in enumerate(y):
                    if v > 0:  # Notīram, lai nepaliek atmiņa par iepriekšējo īsāko ceļu
                        y[x] = 1
                    else:
                        y[x] = 0

            # Izvēlamies nejaušu saiti un apmainam tās tipu (ja bija saite - izdzēšam, ja nebija - pieliekam)
            rand_x = random.randint(0, len(sol.links)-1)
            rand_y = random.randint(0, len(sol.links)-1)
            if rand_x == rand_y:  # Neļaujam veidot saiti ar sevi
                continue
            value = sol.links[rand_y][rand_x]
            if value == 1 and random.random() > 0.75:
                # Ar 25% iespēju apmainam ceļa virzienu
                sol.links[rand_y][rand_x] = 0
                sol.links[rand_x][rand_y] = 1
            else:
                sol.links[rand_y][rand_x] = 0 if value else 1
            if f"{sol}" not in solutions_used:  # Ja šāds piedāvātais risinājums vel nav ietverts šajā apkaimē
                solutions.append(sol)
                solutions_used.add(f"{sol}")
                i += 1
        return solutions

    def build_graph(self, solution: Solution):
        nodes = []
        for p in self.domain.points:
            nodes.append(
                GraphNode(
                    point=p
                )
            )

        def process_node(node: GraphNode):
            idx = self.domain.points.index(node.point)
            for i, l in enumerate(solution.links[idx]):
                if l > 0:
                    child_node = nodes[i]
                    node.links.append(child_node)
                    if len(child_node.links) == 0:
                        process_node(child_node)

        start_node: GraphNode = nodes[self.domain.start_point_idx]
        process_node(start_node)

        def find_path(node: GraphNode, cur_path: list[GraphNode], cur_dist) -> tuple[list[GraphNode], float]:
            if self.domain.points.index(node.point) == self.domain.finish_point_idx and len(cur_path):
                return cur_path, cur_dist
            if node not in cur_path:
                cur_path.append(node)

                best_path = []
                best_dst = 0
                for n in node.links:
                    path, dst = find_path(
                        n,
                        cur_path[:],
                        cur_dist + self.domain.distances[self.domain.points.index(node.point)][self.domain.points.index(n.point)]
                    )
                    if dst >= 0:
                        if len(best_path) < len(path) or (len(best_path) == len(path) and best_dst > dst):
                            best_path = path
                            best_dst = dst

                return best_path, best_dst
            else:
                return [], -1

        best_path, best_dst = find_path(start_node, [], 0)

        solution.best_path_steps = len(best_path)
        solution.best_path_len = best_dst
        solution.best_path_value = sum([n.point.value for n in best_path])

        for i, node in enumerate(best_path):
            point_idx = self.domain.points.index(node.point)

            next = node.links[0]
            if len(node.links) > 1:
                for nnode in node.links:
                    if self.domain.points.index(nnode.point) == self.domain.finish_point_idx or (len(best_path) > i+1 and nnode.point == best_path[i+1].point):
                        next=nnode
            next_idx = self.domain.points.index(next.point)
            solution.links[point_idx][next_idx] = 2

    def evaluate_solution(self, solution: Solution):
        # Aprēķinam ceļa garumu un izmaksas
        self.build_graph(solution)

        links = np.array(solution.links)
        distances = np.array(self.domain.distances)
        # Mērķi:
        #   maksimāli daudz apmeklēti punkti
        node_goal = 1 - (solution.best_path_steps / len(self.domain.points))
        #   minimāla distance
        dist_goal = solution.best_path_len / np.sum(distances) if solution.best_path_len else np.sum(self.domain.distances)
        #   maksimāla savākto punktu vērtība
        point_goal = 1 - solution.best_path_value / sum([i.value for i in self.domain.points])
        #   minimāls neizmantoto ceļu skaits
        spare_links = np.count_nonzero(links == 1) / len(self.domain.points) ** 2
        #   minimāla neizmantotā distance
        links[links == 2] = 1
        spare_dist_goal = (1 - solution.best_path_len / np.sum(distances * links)) if solution.best_path_len else np.sum(self.domain.distances)
        #   pieņemsim ka solution.time_limit ir distance limit, sodam par parsniegto distanci
        overtime_penalty = max(0, solution.best_path_len - self.domain.time_limit) / self.domain.time_limit
        #   sodam arī par neizmantotu laiku
        undertime_penalty = max(0, self.domain.time_limit - solution.best_path_len) / self.domain.time_limit

        # Pielietojam koeficientus lai mainītu fokusu
        #   izvelkam sakni, lai ievērojami sodītu par pārtērēto
        overtime_penalty = overtime_penalty ** 0.25
        #   kāpinam, lai ļautu būt nedaudz zem atvēlētā laika un par to sodītu mazāk
        undertime_penalty = undertime_penalty ** 3
        #   kāpinam lai samazinātu ietekmi, jo vērtība vairāk vai mazāk dublē point_goal
        node_goal = node_goal ** 2
        #   kāpinam lai samazinātu ietekmi, jo neļauj modelim izvēlēties labus ceļus ja ir lieki posmi
        spare_links = spare_links ** 2

        solution.cost = node_goal + dist_goal + point_goal + spare_links + overtime_penalty + undertime_penalty
        solution.cost_parts = {
            "Apmeklētās virsotnes": round(node_goal, 4),
            "Īsākais ceļš": round(dist_goal, 4),
            "Savāktie punkti": round(point_goal, 4),
            # "Liekā distance": round(spare_dist_goal, 4),
            "Liekie savienojumi": round(spare_links, 4),
            "Pārtērētais laiks": round(overtime_penalty, 4),
            "Neizmantotais laiks": round(undertime_penalty, 4),
            "Ceļa garums": round(solution.best_path_len, 4)
        }

    def solve(self):
        if len(self.domain.points) < 2:
            return
        if len(self.domain.solutions) == 0:
            # Ja vel nav risinājumu, iegūstam sākotnējo risinājumu
            solution = self.get_starting_solution()
            self.build_graph(solution)
            self.evaluate_solution(solution)
            self.domain.solutions.append(solution)
        else:
            if len(self.domain.bad_solutions) > 10 and random.random() > 0.005:
                # Ja vēsturē ir vairāk kā 10 mēginājumi, kas nekļuva par labākajiem risinājumiem
                # Izvēlamies risinājumu kas bija pirms desmit iterācijām kā sākuma risinājumu jaunu ģenerēšanai
                # 0.5% iespēja ka tā nedaram lai ļautu apskatīt "jaunus ceļus"
                prev_solution = self.domain.bad_solutions[-10]
            else:
                prev_solution = self.domain.solutions[-1]

            solutions = self.get_next_solutions(prev_solution, min((len(self.domain.points)-1)*2, 60))
            best_solution = None
            # Atrodam labāko grupā
            for solution in solutions:
                self.build_graph(solution)
                self.evaluate_solution(solution)
                if not best_solution or solution.cost < best_solution.cost:
                    best_solution = solution

            # Ja labākais grupā nedod pienesumu, pievienojam neveiksmīgajiem
            # Citādi pievienojam kā jaunu labāko risinājumu
            if best_solution.cost < self.domain.solutions[-1].cost:
                self.domain.solutions.append(best_solution)
                self.domain.bad_solutions = []
                # print("Found:", best_solution.cost, prev_solution.cost)
            else:
                self.domain.bad_solutions.append(best_solution)
                self.domain.bad_solutions = self.domain.bad_solutions[-11:]
        # print("Time taken: ", datetime.now() - start)

    def run(self) -> None:
        self.is_running = True
        while self.is_running:
            self.solve()
            sleep(1)  # Iepauzējam uz brīdi lai citi pavedieni var darboties

    def stop(self):
        self.is_running = False


if __name__ == '__main__':
    domain = create_test_domain()
    optimizer = Optimizer(domain)
    optimizer.solve()
    solution = optimizer.domain.solutions[-1]

    print(domain.to_json(indent=4))

    for i, a in enumerate(solution.links):
        print(', '.join([str(j) for j in a]))
    print(solution.cost)

    visited_nodes = []
