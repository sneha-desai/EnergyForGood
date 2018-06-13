def init_action_map(a, b, c):
    count = 0
    mapping = {}
    for i in range(a):
        for j in range(b):
            for k in range(c):
                mapping[count] = [i, j, k]
                count += 1
    return mapping

def init_state_map(a, b, c):
    count = 0
    mapping = {}
    for i in range(a):
        for j in range(b):
          for k in range(c):
              mapping[count] = [i, j, k]
              count += 1
    return mapping


def get_state_index(state, state_map):
    for k, v in state_map.items():
        if v == state:
            return k


def get_action_index(action, action_map):
    for k, v in action_map.items():
        if v == action:
            return k
