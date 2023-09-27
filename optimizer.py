from copy import deepcopy
import numpy as np
from my_types import Point, Domain, Solution, GraphNode

domain = Domain()
domain.points.append(
    Point(
        x=0,
        y=0,
    )
)
domain.points.append(
    Point(
        x=3,
        y=1,
    )
)
domain.points.append(
    Point(
        x=4,
        y=-3,
    )
)
domain.points.append(
    Point(
        x=2,
        y=5,
    )
)
domain.points.append(
    Point(
        x=1,
        y=5,
    )
)
domain.points.append(
    Point(
        x=8,
        y=3,
    )
)
domain.points.append(
    Point(
        x=5,
        y=1,
    )
)


def fill_distances(domain: Domain):
    domain.distances = [[0] * len(domain.points) for i in range(len(domain.points))]
    for i, point1 in enumerate(domain.points):
        for j, point2 in enumerate(domain.points):
            dst = ((point1.x-point2.x)**2 + (point1.y-point2.y)**2) ** 0.5
            domain.distances[i][j] = dst


def get_starting_solution(domain: Domain) -> Solution:
    solution = Solution(
        domain=domain
    )
    solution.links = [[0] * len(domain.points) for i in range(len(domain.points))]
    cur_point = domain.start_point_idx
    seen_points = [cur_point]
    while True:
        distances = deepcopy(domain.distances[cur_point])
        # Neiesim uz punktu kurā jau esam
        distances[cur_point] = -1

        # Neiesim uz jau aplūkotu punktu
        for i in seen_points:
            # Neļaujam iet uz finišu kamēr visi pārējie punkti nav apstaigāti
            if i != domain.finish_point_idx \
                    or len(seen_points) <= len(domain.points)-1:
                distances[i] = -1

        # Atrodam mazāko nenegatīvo vērtību un ejam uz to
        min_dst = min([i for i in distances if i >= 0])
        min_idx = distances.index(min_dst)
        solution.links[cur_point][min_idx] = 1
        cur_point = min_idx
        seen_points.append(cur_point)

        # Ja esam nonākuši finišā, un viss ir apmeklēts, tad beidzam
        if cur_point == domain.finish_point_idx:
            break
    return solution


def get_next_solutions(solution: Solution, n: int) -> list[Solution]:
    i = 0
    while i < n:
        pass


def build_graph(solution: Solution):
    domain = solution.domain
    nodes = []
    for p in domain.points:
        nodes.append(
            GraphNode(
                point=p
            )
        )

    def process_node(node: GraphNode):
        idx = domain.points.index(node.point)
        for i, l in enumerate(solution.links[idx]):
            if l == 1:
                child_node = nodes[i]
                node.links.append(child_node)
                if len(child_node.links) == 0:
                    process_node(child_node)

    start_node: GraphNode = nodes[domain.start_point_idx]
    solution.graph = start_node
    process_node(start_node)

    def get_path_length(path: list[GraphNode]) -> float:
        path_len = 0
        for n1, n2 in zip(path[:-1], path[1:]):
            idx1 = domain.points.index(n1.point)
            idx2 = domain.points.index(n2.point)
            path_len += domain.distances[idx1][idx2]
        return path_len


    def find_path(node: GraphNode, cur_path: list[GraphNode]) -> list[GraphNode]:
        if domain.points.index(node.point) == domain.finish_point_idx and len(cur_path):
            return cur_path
        cur_path.append(node)

        best_path = []
        for n in node.links:
            path = find_path(
                n,
                cur_path[:]
            )
            if len(best_path) == 0 \
                    or len(best_path) > len(path):
                best_path = path

        return best_path

    bpath = find_path(start_node, [])

    solution.best_path_steps = len(bpath)
    solution.best_path_len = get_path_length(bpath)
    for node in bpath:
        node.is_shortest_path = True


def evaluate_solution(solution: Solution):
    # Aprēķinam ceļa garumu un izmaksas
    build_graph(solution)

    distances = np.array(solution.domain.distances)
    route = np.array(solution.links)

    distance = np.sum(distances * route)
    overtime = min(0, solution.domain.time_limit - distance) * -1
    wasted_distance = distance - solution.best_path_len

    path_steps_score = 1 - (solution.best_path_steps / len(solution.domain.points))

    # Mērķi:
    #   overtime = 0
    #   distance = best_path_len (risinājumā nav ceļi kas nekur nenoved)
    #   wasted_distance = 0   (risinājumā nav ceļi kas nekur nenoved)
    #   best_path_len --> 0 (Risinājums atrod īsāko ceļu)
    #   path_steps_score --> 0 (Risinājums iekļauj visus punktus)

    # Reizinam best_path_len un path_steps_score lai nesodītu modeli par papildus punktu pielikšanu

    solution.cost = overtime + wasted_distance + solution.best_path_len * (0.25 + path_steps_score * 0.75)

    solution.cost_parts = {
        "distance": distance,
        "wasted_distance": wasted_distance,
        "overtime": overtime,
        "path_len": solution.best_path_len,
        "path_steps": solution.best_path_steps,
        "path_steps_score": path_steps_score,
        "formula": f"{overtime} + {wasted_distance} + {solution.best_path_len} * (0.25 + {path_steps_score} * 0.75)"
    }


def solve(domain: Domain) -> Solution:
    pass


fill_distances(domain)

solution = get_starting_solution(domain)
build_graph(solution)
evaluate_solution(solution)

if __name__ == '__main__':
    print(domain.to_json(indent=4))

    for i, a in enumerate(solution.links):
        print(', '.join([str(j) for j in a]))
        idx = a.index(1)
    print(solution.cost)

    visited_nodes = []
    def print_graph(node: GraphNode):
        for n in node.links:
            print(f"{solution.domain.points.index(node.point)} --> {solution.domain.points.index(n.point)}")
            if solution.domain.points.index(n.point) not in visited_nodes:
                visited_nodes.append(solution.domain.points.index(n.point))
                print_graph(n)

    print_graph(solution.graph)
