from pathlib import Path

TEST_PROBLEM_INDICES = [
    26051461,
    6896729,
    15308998,
    14513511,
    27757158,
    5987395,
    24912391,
    188234,
    3167397,
    32200128,
]

SAMPLE_SOLUTION = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0],
    [1, 0, 0, 1, 1],
    [1, 0, 1, 1, 1],
]


def line_clues(line):
    runs = []
    count = 0

    for cell in line:
        if int(cell) == 1:
            count += 1
        elif count > 0:
            runs.append(count)
            count = 0

    if count > 0:
        runs.append(count)

    return runs or [0]


def derive_hints(solution):
    top_hints = []
    left_hints = []

    for row in solution:
        left_hints.append(line_clues(row))

    width = len(solution[0])
    height = len(solution)
    for column_index in range(width):
        column = []
        for row_index in range(height):
            column.append(solution[row_index][column_index])
        top_hints.append(line_clues(column))

    return top_hints, left_hints


def get_sample_problem():
    return derive_hints(SAMPLE_SOLUTION)


def print_puzzle(hints, solution, name=None):
    top_hints, left_hints = hints

    max_left_hint_len = max(len(hint) for hint in left_hints)
    max_top_hint_len = max(len(hint) for hint in top_hints)

    def left_hint_text(hint):
        text = " ".join(str(number) for number in hint)
        return text.rjust(max_left_hint_len * 2 - 1)

    if name is not None:
        print(name)

    # Print hints above the board (from top line to bottom line)
    for top_line_index in range(max_top_hint_len):
        line_numbers = []
        for hint in top_hints:
            empty_slots = max_top_hint_len - len(hint)
            if top_line_index < empty_slots:
                line_numbers.append(" ")
            else:
                number_index = top_line_index - empty_slots
                line_numbers.append(str(hint[number_index]))
        print(" " * (max_left_hint_len * 2 + 2) + " ".join(line_numbers))

    board_width = len(" ".join("0" for _ in top_hints))
    print(" " * (max_left_hint_len * 2) + "-" * (board_width + 2))

    for row_hint, row_values in zip(left_hints, solution):
        row_text = " ".join(str(value) for value in row_values)
        print(f"{left_hint_text(row_hint)} | {row_text}")


def show_incorrect_solution(hints, reference, solution):
    print_puzzle(hints, reference, "Expected solution:")
    print()
    print_puzzle(hints, solution, "Your solution:")


def normalize_grid(grid):
    if len(grid) != 5:
        raise ValueError(f"Solver returned {len(grid)} rows, expected 5")

    normalized = []
    for row in grid:
        if len(row) != 5:
            raise ValueError(f"Solver row has {len(row)} columns, expected 5")
        normalized.append([int(value) for value in row])
    return normalized


def parse_test_case_line(line):
    values = line.strip()
    if len(values) != 25:
        raise ValueError(f"Invalid test case length: expected 25 values, got {len(values)}")
    if any(ch not in {"0", "1"} for ch in values):
        raise ValueError("Test case must contain only 0/1 values")

    flat_values = [int(ch) for ch in values]
    return [flat_values[i:i + 5] for i in range(0, 25, 5)]


def load_test_set(path):
    cases = []
    for line in Path(path).read_text().splitlines():
        stripped = line.strip()
        if stripped:
            cases.append(parse_test_case_line(stripped))
    return cases


def iter_test_set(path):
    with Path(path).open() as file:
        for line in file:
            stripped = line.strip()
            if stripped:
                yield parse_test_case_line(stripped)


def validate_sample(solution):
    if normalize_grid(solution) == SAMPLE_SOLUTION:
        print("Valid sample solution")
    else:
        print("Invalid sample solution")
        show_incorrect_solution(get_sample_problem(), SAMPLE_SOLUTION, normalize_grid(solution))


def validate_with_test_set(solver_fn, path="data/5x5/tests.txt", max_failure_details=10):
    passed_count = 0
    failed_count = 0
    failure_details = []
    total_cases = 0

    for case_index, expected_solution in enumerate(iter_test_set(path), start=1):
        total_cases = case_index
        top_hints, left_hints = derive_hints(expected_solution)
        try:
            actual_solution = normalize_grid(solver_fn(top_hints, left_hints))
        except Exception as error:
            failed_count += 1
            if len(failure_details) < max_failure_details:
                failure_details.append(
                    {
                        "index": case_index,
                        "error": str(error),
                        "hints": (top_hints, left_hints),
                        "expected": expected_solution,
                        "actual": None,
                    }
                )
            continue

        if actual_solution == expected_solution:
            passed_count += 1
        else:
            failed_count += 1
            if len(failure_details) < max_failure_details:
                failure_details.append(
                    {
                        "index": case_index,
                        "error": None,
                        "hints": (top_hints, left_hints),
                        "expected": expected_solution,
                        "actual": actual_solution,
                    }
                )

    print(f"{passed_count} out of {total_cases} test cases solved")

    for result in failure_details:
        print()
        print(f"Test case {result['index']} failed")
        if result["error"] is not None:
            print(f"solver error: {result['error']}")
        else:
            show_incorrect_solution(result["hints"], result["expected"], result["actual"])

    omitted_failures = failed_count - len(failure_details)
    if omitted_failures > 0:
        print()
        print(f"... {omitted_failures} additional failed cases omitted from detailed output")

    return failed_count == 0


def validate_with_all_problem_set(solver_fn, path="data/5x5/tests_random_10000.txt", max_failure_details=10):
    return validate_with_test_set(solver_fn, path=path, max_failure_details=max_failure_details)


def validate_with_small_problem_set(solver_fn, path="data/5x5/tests.txt", max_failure_details=10):
    return validate_with_test_set(solver_fn, path=path, max_failure_details=max_failure_details)
