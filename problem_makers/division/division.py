from time import time
from random import randint

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


# 等幅フォントで綺麗に筆算を表示する関数
def print_figure(arr):
    factor1, factor2, calculating, result = arr
    ans_str = ['' for _ in range(5 + len(calculating))]
    width = len(factor1) + 1 + len(factor2)
    for _ in range(width - result):
        ans_str[0] += ' '
    ans_str[0] += str(result)
    for _ in range(width - len(factor1)):
        ans_str[1] += ' '
    for _ in range(len(factor1)):
        ans_str[1] += '_'
    ans_str[1]
    ans_str[2] = str(factor2) + ')' + str(factor1)
    for line in ans_str:
        print(line)
    return '\n'.join(ans_str)




# 解が一意に定まるか検証する関数
def explore_answers(factor1, factor2, calculating, result, difficulty):
    # 基本的には穴をランダムに埋めて再帰呼び出しして矛盾がないか確認する。

    # difficultyは関数の呼び出し回数で定義
    difficulty += 1

    # factor1(上段の上)に穴がある場合はランダムな数字を入れる。
    for i, j in enumerate(factor1):
        if j == 'x':
            res = 0
            for num in range(10):
                if i == 0 and num == 0:
                    continue
                n_factor1 = [k for k in factor1]
                n_factor1[i] = str(num)
                tmp, n_difficulty = explore_answers(n_factor1, factor2, calculating, result, 0)
                difficulty += n_difficulty
                if tmp == -1 or res + tmp > 1:
                    return -1, difficulty
                res += tmp
            return res, difficulty
    
    # factor1に穴がなく、factor2(上段の下)に穴がある場合はランダムに埋めつつ矛盾がないか確認して再帰呼び出しする。
    int_factor1 = int(''.join(factor1))
    for i, j in enumerate(factor2):
        if j == 'x':
            res = 0
            for num in range(10):
                calculating_expected = [i for i in str(num * int_factor1)]
                if len(calculating_expected) != len(calculating[len(calculating) - 1 - i]):
                    continue
                for k, l in zip(calculating[len(calculating) - 1 - i], calculating_expected):
                    if 'x' != k != l:
                        break
                else:
                    n_factor2 = [k for k in factor2]
                    n_factor2[i] = str(num)
                    tmp, n_difficulty = explore_answers(factor1, n_factor2, calculating, result, 0)
                    difficulty += n_difficulty
                    if tmp == -1 or res + tmp > 1:
                        return -1, difficulty
                    res += tmp
            return res, difficulty
    
    # factor1もfactor2も埋まっている場合は矛盾がないかチェックする。
    # factor2を埋める際にcalculating(中段)では矛盾がないことが保証されるので、result(下段)で矛盾がないか確認する。
    calculating_expected = []
    for i in reversed([int(i) for i in factor2]):
        calculating_expected.append(int_factor1 * i)
    result_expected = 0
    for i, j in enumerate([i for i in calculating_expected]):
        result_expected += j * (10 ** i)
    result_expected = [i for i in str(result_expected)]
    if len(result) != len(result_expected):
        return 0, difficulty
    for i, j in zip(result, result_expected):
        if 'x' != i != j:
            return 0, difficulty
    return 1, difficulty




# ランダムに問題を生成する関数
def random_problem(difficulty_input, digit):
    # ランダムに上段の数字を決める
    max_num = 10 ** digit - 1
    factor1 = randint(1, max_num)
    factor2 = randint(1, factor1 // 100)
    result = factor1 // factor2

    # 下段の数字たちを計算する
    calculating = []
    strt = 0
    str_factor1 = str(factor1)
    len_factor1 = len(str_factor1)
    for i in range(len_factor1):
        if int(str_factor1[:i + 1]) >= factor2:
            strt = i
            break
    num = int(str_factor1[:strt])
    for i in range(strt, len_factor1):
        num *= 10
        num += int(str_factor1[i])
        calc = num // factor2
        num %= factor2
        calculating.append(num)
    num_of_digit = len_factor1 + len(str(factor2)) + sum(len(str(i)) for i in calculating) + len(str(result))
    print(factor1, factor2, result, calculating, num_of_digit)

    # 穴をランダムにあける
    holes = []
    min_holes = map_int(difficulty_input, 0, 9, min(difficulty_input, num_of_digit), num_of_digit // 2)
    max_holes = map_int(difficulty_input, 0, 9, min_holes, num_of_digit // 1.5)
    num_of_holes = randint(min_holes, max_holes)
    # 穴をあける場所を決める
    for _ in range(num_of_holes):
        if len(holes) == all_digit:
            break
        tmp = randint(0, all_digit - 1)
        while tmp in holes:
            tmp = randint(0, all_digit - 1)
        holes.append(tmp)
    holes.sort()

    # 決めた場所に穴をあける(xに置換する)
    factor1_hole = [i for i in factor1_split]
    factor2_hole = [i for i in factor2_split]
    calculating_hole = [[i for i in j] for j in calculating_split]
    result_hole = [i for i in result_split]
    len_num_of_digit = len(num_of_digit)
    for hole in holes:
        tmp = 0
        for i in range(1, len_num_of_digit):
            if num_of_digit[i - 1] <= hole < num_of_digit[i]:
                tmp = i
                break
        if tmp == 0:
            factor1_hole[hole - 0] = 'x'
        elif tmp == 1:
            factor2_hole[hole - num_of_digit[tmp - 1]] = 'x'
        elif tmp == len_num_of_digit - 1:
            result_hole[hole - num_of_digit[-2]] = 'x'
        else:
            calculating_hole[tmp - 2][hole - num_of_digit[tmp - 1]] = 'x'
    return factor1_hole, factor2_hole, calculating_hole, result_hole, factor1, factor2, calculating, result




def problem_maker_division(difficulty_input, digit, timeout=1):
    ans_problem = []
    ans_answer = []
    difficulties = []
    strt = time()
    t = 0
    factor1_hole, factor2_hole, calculating_hole, result_hole, factor1, factor2, calculating, result = random_problem(difficulty_input, digit)
    '''
    # タイムアウトするまたは問題が10個見つかるまで問題を作成し、解の一意性を検証する。
    while time() - strt < timeout and t < 10:
        factor1_hole, factor2_hole, calculating_hole, result_hole, factor1, factor2, calculating, result = random_problem(difficulty_input, digit)
        res_ad, difficulty = explore_answers(factor1_hole, factor2_hole, calculating_hole, result_hole, 0)
        admissible = res_ad == 1
        if not admissible:
            continue
        t += 1
        difficulties.append(difficulty)
        ans_problem.append([''.join(factor1_hole), ''.join(factor2_hole), [''.join(i) for i in calculating_hole], ''.join(result_hole)])
        ans_answer.append([str(factor1), str(factor2), [str(i) for i in calculating], str(result)])
    '''
    # 採用する問題を選ぶ
    print(len(difficulties), 'answers found')
    if ans_problem:
        print('problem found')
        difficulties_sort = sorted(difficulties)
        key = -1
        if difficulty_input == 0:
            # 最も簡単な問題を選ぶ
            key = difficulties_sort[0]
        elif difficulty_input == 9:
            # 最も難しい問題を選ぶ
            key = difficulties_sort[-1]
        else:
            # 実測難易度(difficulties)の中央値の問題を選ぶ
            key = difficulties_sort[len(difficulties_sort) // 2]
        idx = difficulties.index(key)
        print(print_figure(ans_problem[idx]))
        print('answer:')
        print(print_figure(ans_answer[idx]))
        print('difficulty:', difficulties[idx])
        print(time() - strt, 'sec')
        return print_figure(ans_problem[idx]), print_figure(ans_answer[idx]), difficulties[idx]
    else:
        # 問題が見つからなかった場合
        print('problem not found')
        print(time() - strt, 'sec')
        return -1, -1, -1