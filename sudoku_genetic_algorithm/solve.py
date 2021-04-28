from math import sqrt
from random import shuffle, randint
from ultility import *


def solve(problem_grid, population_size=1000, selection_rate=0.5, max_generations_count=1000, mutation_rate=0.05):
    """
    Giai bai toan Sudoku bang thuat toan GA
    Gia su cac tham so deu hop le

    Parameters:
        - selection_rate (int)m_grid (list): Mot ma tran NxN.
        - population_size (int): The initial po
        - max_generations_count (int)
        - mutation_rate (int)

    Raises:
            - Exception: bai toan khong the giai duoc
    """

    # square root of the problem grid's size
    N = int(sqrt(len(problem_grid)))

    def empty_grid(elem_generator=None):
        """
        tra ve mot ma tran trong.

        Parameters:
            - elem_generator (function) (optional=None): dung de khoi tao gia tri trong luoi sudoku.
              Neu cac phan tu trong o trong thi chung ta dien "None".
        """

        return [
            [
                (None if elem_generator is None else elem_generator(i, j))
                for j in range(len(problem_grid))
            ] for i in range(len(problem_grid))
        ]

    def deep_copy_grid(grid):
        """
        tra ve 1 deep copy cua mang.

        Parameters:
            - grid (list)
        """

        return empty_grid(lambda i, j: grid[i][j])

    # this is done to avoid changes in the input argument
    problem_grid = deep_copy_grid(problem_grid)


    def fill_predetermined_cells():
        """
        Dien tien gia tri cua cac o

        Raises:
            - Exception: Bai toan khong the giai.
        """

        # TODO:

        track_grid = empty_grid(lambda *args: [val for val in range(1, len(problem_grid) + 1)])

        def pencil_mark(i, j):
            """
            danh dau gia tri cua pha tu grid[i][j] neu no trong hang, cot va mang con
            Parameters:
                - i (int): chi so cua mang con.
                - j (int): chi so phan tu con trong mang.

            Returns: ban hoan thien hon cua mang.
            """

            # remove from same sub-grid cells
            for a, b in same_sub_grid_indexes(problem_grid, i, j, itself=False):
                try:
                    track_grid[a][b].remove(problem_grid[i][j])
                except (ValueError, AttributeError) as e:
                    pass

            # remove from same row cells
            for a, b in same_row_indexes(problem_grid, i, j, N, itself=False):
                try:
                    track_grid[a][b].remove(problem_grid[i][j])
                except (ValueError, AttributeError) as e:
                    pass

            # remove from same column cells
            for a, b in same_column_indexes(problem_grid, i, j, N, itself=False):
                try:
                    track_grid[a][b].remove(problem_grid[i][j])
                except (ValueError, AttributeError) as e:
                    pass

        for i in range(len(problem_grid)):
            for j in range(len(problem_grid)):
                if problem_grid[i][j] is not None:
                    pencil_mark(i, j)

        while True:
            anything_changed = False

            for i in range(len(problem_grid)):
                for j in range(len(problem_grid)):
                    if track_grid[i][j] is None:
                        continue

                    if len(track_grid[i][j]) == 0:
                        raise Exception('The puzzle is not solvable.')
                    elif len(track_grid[i][j]) == 1:
                        problem_grid[i][j] = track_grid[i][j][0]
                        pencil_mark(i, j)

                        track_grid[i][j] = None

                        anything_changed = True

            if not anything_changed:
                break

        return problem_grid

    def generate_initial_population():
        """
        Khoi tao tap dan so theo kich co dan so nhap vao
        Returns (list): mot tap cac ung vien
        """

        candidates = []
        for k in range(population_size):
            candidate = empty_grid()
            for i in range(len(problem_grid)):
                shuffled_sub_grid = [n for n in range(1, len(problem_grid) + 1)]
                shuffle(shuffled_sub_grid)

                for j in range(len(problem_grid)):
                    if problem_grid[i][j] is not None:
                        candidate[i][j] = problem_grid[i][j]

                        shuffled_sub_grid.remove(problem_grid[i][j])

                for j in range(len(problem_grid)):
                    if candidate[i][j] is None:
                        candidate[i][j] = shuffled_sub_grid.pop()

            candidates.append(candidate)

        return candidates

    def fitness(grid):
        """
        tinh toan ham dinh gia

        Parameters:
            - grid (list)

        Returns (int): gia tri sau khi dinh gia cua moi ung vien.
        """

        row_duplicates_count = 0

        # calculate rows duplicates
        for a, b in same_column_indexes(problem_grid, 0, 0, N):
            row = list(get_cells_from_indexes(grid, same_row_indexes(problem_grid, a, b, N)))

            row_duplicates_count += len(row) - len(set(row))

        return row_duplicates_count

    def selection(candidates):
        """
        Tra ve phan ("selection_rate") cua ung vien dua tren gia tri cua ham dinh gia (cang thap cang tot)
        Parameters:
            - candidates (list)

        Returns (list)
        """

        # TODO: Probabilistically selection.

        index_fitness = []
        for i in range(len(candidates)):
            index_fitness.append(tuple([i, fitness(candidates[i])]))

        index_fitness.sort(key=lambda elem: elem[1])

        selected_part = index_fitness[0: int(len(index_fitness) * selection_rate)]
        indexes = [e[0] for e in selected_part]


        return [candidates[i] for i in indexes], selected_part[0][1]

    fill_predetermined_cells()

    population = generate_initial_population()
    best_fitness = None

    for i in range(max_generations_count):
        population, best_fitness = selection(population)

        if i == max_generations_count - 1 or fitness(population[0]) == 0:
            break

        shuffle(population)
        new_population = []

        while True:
            solution_1, solution_2 = None, None

            try:
                solution_1 = population.pop()
            except IndexError:
                break

            try:
                solution_2 = population.pop()
            except IndexError:
                new_population.append(solution_2)
                break

            cross_point = randint(0, len(problem_grid) - 2)

            temp_sub_grid = solution_1[cross_point]
            solution_1[cross_point] = solution_2[cross_point + 1]
            solution_2[cross_point + 1] = temp_sub_grid

            new_population.append(solution_1)
            new_population.append(solution_2)

        # mutation
        for candidate in new_population[0:int(len(new_population) * mutation_rate)]:
            random_sub_grid = randint(0, 8)
            possible_swaps = []
            for grid_element_index in range(len(problem_grid)):
                if problem_grid[random_sub_grid][grid_element_index] is None:
                    possible_swaps.append(grid_element_index)

            if len(possible_swaps) > 1:
                shuffle(possible_swaps)
                first_index = possible_swaps.pop()
                second_index = possible_swaps.pop()
                tmp = candidate[random_sub_grid][first_index]
                candidate[random_sub_grid][first_index] = candidate[random_sub_grid][second_index]
                candidate[random_sub_grid][second_index] = tmp

        population.extend(new_population)

    return population[0], best_fitness
