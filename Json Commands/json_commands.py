import json


def open_json(file):
    with open(file) as f:
        data = json.load(f)
    return data


def save_json(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)


def scan(data, search_term, looking_for=None):
    if looking_for is not None:
        for x in data:
            if x[looking_for] == search_term:
                return True
        return False
    else:
        for x in data:
            if x == search_term:
                return True
        return False


def delete(data, search_term, looking_for=None):
    if looking_for is not None:
        for x in data:
            i = 0
            if x[looking_for] == search_term:
                data.pop(i)
            i += 1
    else:
        for x in data:
            i = 0
            if x == search_term:
                data.pop(i)
            i += 1


def delete_and_save(data, file, search_term, looking_for=None):
    if looking_for is not None:
        for x in data:
            i = 0
            if x[looking_for] == search_term:
                data.pop(i)
                save_json(data, file)
            i += 1
    else:
        for x in data:
            i = 0
            if x == search_term:
                data.pop(i)
                save_json(data, file)
            i += 1


def update(data, change, new, search_term, looking_for=None):
    if looking_for is not None:
        for x in data:
            if x[looking_for] == search_term:
                x[change] = new
                return True
        return False
    else:
        for x in data:
            if x == search_term:
                x[change] = new
                return True
        return False


def update_and_save(data, file, change, new, search_term, looking_for=None):
    if looking_for is not None:
        for x in data:
            if x[looking_for] == search_term:
                x[change] = new
                save_json(data, file)
        return False
    else:
        for x in data:
            if x == search_term:
                x[change] = new
                save_json(data, file)
                return True
        return False


def return_data(data, return_term, search_term, looking_for=None):
    if looking_for is not None:
        for x in data:
            if x[looking_for] == search_term:
                try:
                    return x[return_term]
                except KeyError:
                    return False
        return False
    else:
        for x in data:
            if x == search_term:
                try:
                    return x[return_term]
                except KeyError:
                    return False
        return False
