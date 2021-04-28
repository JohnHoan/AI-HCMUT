from solve import *
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Input file that contains Sudoku's problem.")
    parser.add_argument("-o", "--output-file", help="Output file to store problem's solution.",
                        type=str, default=None)
    parser.add_argument("-p", "--population-size", type=int, default=10000)
    parser.add_argument("-s", "--selection-rate", type=float, default=0.5)
    parser.add_argument("-m", "--max-generations-count", type=int, default=1000)
    parser.add_argument("-u", "--mutation-rate", type=float, default=0.05)
    parser.add_argument("-q", "--quiet", action="store_true")
    args = parser.parse_args()

    try:
        with open(args.file, "r") as input_file:
            file_content = input_file.read()
            file_lines = file_content.split('\n')
            problem_grid = [[] for i in range(len(file_lines))]
            sqrt_n = int(sqrt(len(file_lines)))
            for j in range(len(file_lines)):
                line_values = [(int(value) if value != '-' else None) for value in file_lines[j].split(' ')]
                for i in range(len(line_values)):
                    problem_grid[
                        int(i / sqrt_n) +
                        int(j / sqrt_n) * sqrt_n
                        ].append(line_values[i])

            try:
                solution, best_fitness = solve(
                    problem_grid,
                    population_size=args.population_size,
                    selection_rate=args.selection_rate,
                    max_generations_count=args.max_generations_count,
                    mutation_rate=args.mutation_rate
                )
                output_str = "Best fitness value: " + str(best_fitness) + '\n\n'
                for a, b in same_column_indexes(solution, 0, 0, sqrt_n):
                    row = list(get_cells_from_indexes(solution, same_row_indexes(solution, a, b, sqrt_n)))

                    output_str += " ".join([str(elem) for elem in row]) + '\n'
                output_str = output_str

                if args.output_file:
                    with open(args.output_file, "w") as output_file:
                        output_file.write(output_str)

                if not args.quiet:
                    print(output_str[:-1])

            except:
                exit('Input problem is not solvable.')
    except FileNotFoundError:
        exit("Input file not found.")
