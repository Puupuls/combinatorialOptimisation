# Ir doti n punkti, kur katram ir noteikta vērtība v[i].
# Ir dots sākuma punkts s un finiša punkts f (vai tas ir tas pats?).
# Dota laika matrica d, kurā jau iepriekš sarēķināts nepieciešamais laiks, lai nokļūtu no katra uz katru punktu.
# Uzdevums ir atrast tādu punktu virkni, kas sākas punktā s un beidzas punktā f un dod vislielāko vērtību, bet prasa ne vairāk laika kā dotais limits t.
from copy import deepcopy
import numpy as np
from my_types import Point, Domain, Solution

domain = Domain()
domain.points.append(
    Point(
        x=0,
        y=0,
        value=1
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
        y=1,
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
            dst = ((point1.x-point2.x)**2 + (point1.x-point2.x)**2) ** 0.5
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


def evaluate_solution(solution: Solution):
    # Aprēķinam ceļa garumu un izmaksas
    distances = np.array(solution.domain.distances)
    route = np.array(solution.links)

    distance = np.sum(distances * route)
    overtime = min(0, solution.domain.time_limit - distance) * -1

    solution.cost = distance + 5 * overtime


def solve(domain: Domain) -> Solution:
    pass


fill_distances(domain)

print(domain.to_json(indent=4))

solution = get_starting_solution(domain)
evaluate_solution(solution)
for i, a in enumerate(solution.links):
    print(', '.join([str(j) for j in a]))
    idx = a.index(1)
print(solution.cost)