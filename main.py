from support import get_sample_problem, validate_sample, validate_with_test_set


def solver(top_hints, left_hints):
    result = [[0]*5]*5

    return result

if __name__ == '__main__':
    """
    Jarik krutoy
    Sample problem:
              1        
          3 0 1 2 2
        -----------
      0 | 0 0 0 0 0
      0 | 0 0 0 0 0
    1 1 | 1 0 1 0 0
    1 2 | 1 0 0 1 1
    1 3 | 1 0 1 1 1
    """
    t_hints, l_hints = get_sample_problem()
    solution = solver(t_hints, l_hints)

    validate_sample(solution)
    # validate_with_test_set(solver_fn=solver)