def path_to_actions(path):
    actions = []
    for i in range(1, len(path)):
        x1, y1 = path[i - 1]
        x2, y2 = path[i]
        if x2 > x1:
            actions.append('move right')
        elif x2 < x1:
            actions.append('move left')
        if y2 > y1:
            actions.append('move down')
        elif y2 < y1:
            actions.append('move up')
    return actions