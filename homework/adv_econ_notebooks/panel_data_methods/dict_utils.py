def set_at(dic, path, value):
    for key in path[:-1]:
        dic = dic.setdefault(key, {})
    dic[path[-1]] = value
