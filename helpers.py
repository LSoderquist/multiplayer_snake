def process_player_data(data):
    x_vals = []
    y_vals = []
    color = None
    val_is_x = True
    for val in data:
        if val.isalpha(): color = val
        elif val_is_x: x_vals.append(int(val))
        else: y_vals.append(int(val))
        val_is_x = not val_is_x

    return [(x, y) for x, y in zip(x_vals, y_vals)], color