# 配列を置換する関数
def replace_arr(arr, replacer):
    res = [None for i in arr]
    for i, j in enumerate(replacer):
        res[i] = arr[j]
    return res

# 一定範囲中の数を新たな範囲の数にmapする関数
def map_int(from_num, from_min, from_max, to_min, to_max):
    key = (from_num - from_min) / (from_max - from_min)
    to_float = (to_max - to_min) * key + to_min
    to_int = int(to_float)
    if to_float - to_int >= 0.5:
        to_int += 1
    return to_int