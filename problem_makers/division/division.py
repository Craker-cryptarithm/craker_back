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
    ans_str = ['' for _ in range(5 + len(calculating) * 3 // 2)]
    width = len(str(factor1)) + 1 + len(str(factor2))
    for _ in range(width - len(str(result))):
        ans_str[0] += ' '
    ans_str[0] += str(result)
    for _ in range(width - len(str(factor1))):
        ans_str[1] += ' '
    for _ in range(len(str(factor1))):
        ans_str[1] += '_'
    ans_str[1]
    ans_str[2] = str(factor2) + ')' + str(factor1)
    end = len(str(factor1)) - len(str(result)) + len(str(factor2)) + 2
    idx = 3
    for i, calc in enumerate(calculating):
        for _ in range(end - len(str(calc)) + i // 2):
            ans_str[idx] += ' '
        strt = 0
        while strt < len(str(calc)) and str(calc)[strt] == '0':
            strt += 1
            ans_str[idx] += ' '
        if strt < len(str(calc)):
            ans_str[idx] += str(calc)[strt:]
        if i != len(calculating) - 1:
            if i % 2:
                ans_str[idx] += str(factor1)[end + i // 2 - len(str(factor2)) - 1]
                idx += 1
            else:
                for _ in range(len(str(factor2)) + 1):
                    ans_str[idx + 1] += ' '
                for _ in range(len(str(factor1))):
                    ans_str[idx + 1] += '_'
                idx += 2
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
                if res >= 2:
                    return -1, difficulty
            return res, difficulty
    
    # factor1に穴がなく、factor2(割る数)に穴がある場合はランダムに埋めつつ矛盾がないか確認して再帰呼び出しする。
    if 'x' in factor2:
        int_factor1 = int(''.join(factor1))
        join_result = ''.join(result)
        min_result = join_result.replace('x', '0')
        if min_result[0] == '0':
            min_result = 10 ** (len(result) - 1) + int(min_result)
        else:
            min_result = int(min_result)
        max_result = int(join_result.replace('x', '9'))
        len_factor2 = len(factor2)
        res = 0
        for result_candidate in range(min_result, max_result + 1):
            for i, j in zip(result, str(result_candidate)):
                if 'x' != i != j:
                    break
            else:
                factor2_candidate = str(int_factor1 // result_candidate)
                for i, j in zip(factor2, factor2_candidate):
                    if 'x' != i != j:
                        break
                else:
                    print(int_factor1, ''.join(factor2_candidate), result_candidate)
                    tmp, n_difficulty = explore_answers(factor1, [i for i in factor2_candidate], calculating, [i for i in str(result_candidate)], 0)
                    difficulty += n_difficulty
                    if tmp == -1:
                        return -1, difficulty
                    res += tmp
                    if res >= 2:
                        return -1, difficulty
        return res, difficulty
    #print(factor1, factor2, calculating, result, difficulty)

    calculating_expected = []
    str_factor1 = str(''.join(factor1))
    len_factor1 = len(factor1)
    int_factor2 = int(''.join(factor2))
    str_result = ''.join(result)
    print(str_result)
    strt = len_factor1 - len(str(''.join(result)))
    num = str_factor1[:strt]
    if num == '':
        num = 0
    else:
        num = int(num)
    for i in range(strt, len_factor1):
        num *= 10
        num += int(str_factor1[i])
        num %= int_factor2
        calculating_expected.append(str(int_factor2 * int(str_result[i - strt])))
        calculating_expected.append(str(num))
    for calc, calc_ex in zip(calculating, calculating_expected):
        if len(calc) != len(calc_ex):
            return 0, difficulty
        for i, j in zip(calc, calc_ex):
            if 'x' != i != j:
                return 0, difficulty

    '''
    for i, j in enumerate(factor2):
        if j == 'x':
            res = 0
            for num in range(10):
                calculating_expected = [i for i in str(int_factor1)]
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
    '''
    return 1, difficulty




# ランダムに問題を生成する関数
def random_problem(difficulty_input, digit):
    # ランダムに上段の数字を決める
    max_num = 10 ** digit - 1
    factor1 = randint(max_num // 10, max_num)
    factor2 = randint(1, factor1 // 100)
    result = factor1 // factor2

    # 下段の数字たちを計算する
    calculating = []
    str_factor1 = str(factor1)
    len_factor1 = len(str_factor1)
    len_factor2 = len(str(factor2))
    len_result = len(str(result))
    strt = len_factor1 - len_result
    num = str_factor1[:strt]
    if num == '':
        num = 0
    else:num = int(num)
    for i in range(strt, len_factor1):
        num *= 10
        num += int(str_factor1[i])
        calc = num // factor2
        num %= factor2
        calculating.append(factor2 * int(str(result)[i - strt]))
        calculating.append(num)
    all_digit = len_factor1 + len_factor2 + sum(len(str(i)) for i in calculating) + len_result
    factor1_split = [i for i in str(factor1)]
    factor2_split = [i for i in str(factor2)]
    result_split = [i for i in str(result)]
    calculating_split = [[i for i in str(j)] for j in calculating]

    # 穴をランダムにあける
    holes = []
    min_holes = map_int(difficulty_input, 0, 9, min(difficulty_input, all_digit), all_digit // 2)
    max_holes = map_int(difficulty_input, 0, 9, min_holes, all_digit // 1.5)
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
    for hole in holes:
        if hole < len_factor1:
            factor1_hole[hole] = 'x'
        elif hole < len_factor1 + len_factor2:
            factor2_hole[hole - len_factor1] = 'x'
        elif hole < all_digit - len_result:
            tmp = hole - len_factor1 - len_factor2
            for i, j in enumerate(calculating_hole):
                if tmp < len(j):
                    calculating_hole[i][tmp] = 'x'
                    break
                tmp -= len(j)
        else:
            result_hole[len_result - all_digit + hole] = 'x'

    return factor1_hole, factor2_hole, calculating_hole, result_hole, factor1, factor2, calculating, result




def problem_maker_division(difficulty_input, digit, timeout=1):
    ans_problem = []
    ans_answer = []
    difficulties = []
    strt = time()
    t = 0
    factor1_hole, factor2_hole, calculating_hole, result_hole, factor1, factor2, calculating, result = random_problem(difficulty_input, digit)
    print_figure([factor1, factor2, calculating, result])
    print_figure([''.join(factor1_hole), ''.join(factor2_hole), [''.join(calculating) for calculating in calculating_hole], ''.join(result_hole)])
    res_ad, difficulty = explore_answers(factor1_hole, factor2_hole, calculating_hole, result_hole, 0)
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