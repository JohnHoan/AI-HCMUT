def same_column_indexes(problem_grid, i, j, N, itself=True):
    """
    Mot generator function xuat ra indexes cua cac phan tu ma cung cot voi input index;
    Parameters:
        - problem_grid (list)
        - i (int): index cua bang con.
        - j (int): index cua phan tu trong bang con.
        - N (int)
        - itself (bool) (optional=True): Cho biet co hien thi index input hay khong.
    """

    sub_grid_column = i % N
    cell_column = j % N

    for a in range(sub_grid_column, len(problem_grid), N):
        for b in range(cell_column, len(problem_grid), N):
            if (a, b) == (i, j) and not itself:
                continue

            yield a, b


def same_row_indexes(problem_grid, i, j, N, itself=True):
    """
    Mot generator function xuat ra indexes cua cac phan tu ma cung hang voi input index;

    Parameters:
        - problem_grid (list)
        - i (int): index cua bang con.
        - j (int): index cua phan tu trong bang con.
        - N (int)
        - itself (bool) (optional=True): Cho biet co hien thi index input hay khong.
    """

    sub_grid_row = int(i / N)
    cell_row = int(j / N)

    for a in range(sub_grid_row * N, sub_grid_row * N + N):
        for b in range(cell_row * N, cell_row * N + N):
            if (a, b) == (i, j) and not itself:
                continue

            yield a, b


def get_cells_from_indexes(grid, indexes):
    """
    Mot generator function xuat ra gia tri cua 1 list index input

    Parameters:
        - grid (list)
        - indexes (list) : e.g. [[1, 2], [3, 10]]

    Returns (list): e.g. [3, 4, 5]
    """

    for a, b in indexes:
        yield grid[a][b]


def same_sub_grid_indexes(problem_grid, i, j, itself=True):
    """
    Mot generator function hien thi phan tu ma co cung sub-grid voi chi so input.

    Parameters:
        - i (int): chi so sub-grid.
        - j (int): chi so cua phan tu trong sub-grid.
        - itself (bool) (optional=True): Cho biet co hien thi index input hay khong.
    """

    for k in range(len(problem_grid)):
        if k == j and not itself:
            continue

        yield i, k


