from support import get_sample_problem, validate_sample, validate_with_test_set


def solver(vertical_hints, horizontal_hints):
    result = [[0]*5]*5

    return result

if __name__ == '__main__':
    """ 
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
    v_hints, h_hints = get_sample_problem()
    solution = solver(v_hints, h_hints)

    # validate_sample(solution)
    validate_with_test_set(solver_fn=solver)