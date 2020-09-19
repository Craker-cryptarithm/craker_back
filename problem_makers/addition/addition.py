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
    factor1, factor2, result = arr
    ans_str = ['' for _ in range(4)]
    width = len(str(result)) + 1
    space = width - len(str(factor1))
    for _ in range(space):
        ans_str[0] += ' '
    for i in str(factor1):
        ans_str[0] += i
    space = width - len(str(factor2))
    for _ in range(space):
        ans_str[1] += ' '
    for i in str(factor2):
        ans_str[1] += i
    ans_str[2] += '+'
    for _ in range(width - 1):
        ans_str[2] += '_'
    space = width - len(str(result))
    for _ in range(space):
        ans_str[3] += ' '
    for i in str(result):
        ans_str[3] += i
    return '\n'.join(ans_str)




def explore_answers(factor1, factor2, result, difficulty):
    # 基本的には穴をランダムに埋めて再帰呼び出しして矛盾がないか確認する。

    # difficultyは関数の呼び出し回数で定義
    difficulty += 1

    for ii, j in enumerate(reversed(factor1)):
        i = len(factor1) - 1 - ii
        if j == 'x':
            res = 0
            for num in range(10):
                if i == 0 and num == 0:
                    continue
                n_factor1 = [k for k in factor1]
                n_factor1[i] = str(num)
                tmp, n_difficulty = explore_answers(n_factor1, factor2, result, 0)
                difficulty += n_difficulty
                if tmp == -1 or res + tmp > 1:
                    return -1, difficulty
                res += tmp
            return res, difficulty
    
    calculating = [0 for _ in range(len(result))]
    for ii, j in enumerate(reversed(factor2)):
        i = len(factor2) - 1 - ii
        if j == 'x':
            res = 0
            for num in range(10):
                if i == 0 and num == 0:
                    continue
                tmp = 0
                if len(factor1) - 1 - ii >= 0:
                    tmp = int(factor1[len(factor1) - 1 - ii])
                if str(calculating[i] + num + tmp)[-1] == result[len(result) - 1 - ii]:
                    n_factor2 = [k for k in factor2]
                    n_factor2[i] = str(num)
                    tmp, n_difficulty = explore_answers(factor1, n_factor2, result, 0)
                    difficulty += n_difficulty
                    if tmp == -1 or res + tmp > 1:
                        return -1, difficulty
                    res += tmp
            return res, difficulty
        else:
            tmp = 0
            if len(factor1) - 1 - ii >= 0:
                tmp = int(factor1[len(factor1) - 1 - ii])
            sum_sub_int = tmp + int(j)
            sum_sub = [k for k in str(sum_sub_int)]
            for k, l in enumerate(reversed(sum_sub)):
                calculating[i - k] += int(l)
    factor1_int = int(''.join(factor1))
    factor2_int = int(''.join(factor2))
    result_expected = str(factor1_int + factor2_int)
    for i, j in zip(result, result_expected):
        if 'x' != i != j:
            return 0, difficulty
    return 1, difficulty





def random_problem(difficulty_input, digit):
    # ランダムに上段の数字を決める
    max_num = 10 ** digit - 1
    factor1 = randint(1, max_num)
    factor2 = randint(1, max_num)
    result = factor1 + factor2
    len_factor1 = len(str(factor1))
    len_factor2 = len(str(factor2))
    len_result = len(str(result))
    all_digit = len_factor1 + len_factor2 + len_result
    factor1_split = [i for i in str(factor1)]
    factor2_split = [i for i in str(factor2)]
    result_split = [i for i in str(result)]

    # 穴をランダムにあける
    holes = []
    min_holes = map_int(difficulty_input, 0, 9, 1, all_digit // 4)
    max_holes = map_int(difficulty_input, 0, 9, min_holes, all_digit // 3)
    num_of_holes = randint(min_holes, max_holes)
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
    result_hole = [i for i in result_split]
    for hole in holes:
        if hole < len_factor1:
            factor1_hole[hole] = 'x'
        elif hole < len_factor1 + len_factor2:
            factor2_hole[hole - len_factor1] = 'x'
        else:
            result_hole[hole - len_factor1 - len_factor2] = 'x'
    return factor1_hole, factor2_hole, result_hole, factor1, factor2, result



def problem_maker_addition(difficulty_input, digit, timeout=1):
    ans_problem = []
    ans_answer = []
    difficulties = []
    strt = time()
    t = 0

    while time() - strt < timeout and t < 10:
        factor1_hole, factor2_hole, result_hole, factor1, factor2, result = random_problem(difficulty_input, digit)
        res_ad, difficulty = explore_answers(factor1_hole, factor2_hole, result_hole, 0)
        admissible = res_ad == 1
        if not admissible:
            continue
        t += 1
        difficulties.append(difficulty)
        ans_problem.append([''.join(factor1_hole), ''.join(factor2_hole), ''.join(result_hole)])
        ans_answer.append([str(factor1), str(factor2), str(result)])
    
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