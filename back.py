from random import randint
from time import time

def replace_arr(arr, replacer):
    res = [None for i in arr]
    for i, j in enumerate(replacer):
        res[i] = arr[j]
    return res

def map_int(from_num, from_min, from_max, to_min, to_max):
    key = (from_num - from_min) / (from_max - from_min)
    to_float = (to_max - to_min) * key + to_min
    to_int = int(to_float)
    if to_float - to_int >= 0.5:
        to_int += 1
    return to_int

def print_figure(arr):
    factor1, factor2, calculating, result = arr
    ans_str = ['' for _ in range(5 + len(calculating))]
    width = max(len(str(factor1)), len(str(factor2)), len(str(result)) - 1)
    for i, j in enumerate(calculating):
        width = max(width, len(str(j)) + i)
    for line_num, factor in enumerate([factor1, factor2]):
        tmp = ''
        for _ in range(width + 1 - len(str(factor))):
            tmp += ' '
        tmp += str(factor)
        ans_str[line_num] = tmp
    ans_str[2] = 'x' + '_' * width
    for i, factor in enumerate(calculating):
        line_num = i + 3
        tmp = ''
        for _ in range(width + 1 - i - len(str(factor))):
            tmp += ' '
        tmp += str(factor)
        tmp += ' ' * i
        ans_str[line_num] = tmp
    ans_str[-2] = '_' * (width + 1)
    ans_str[-1] = ' ' * (width + 1 - len(str(result))) + str(result)
    for line in ans_str:
        print(line)


def explore_answers(factor1, factor2, calculating, result, difficulty):
    difficulty += 1
    for i, j in enumerate(factor1):
        if j == 'x':
            res = 0
            for num in range(10):
                n_factor1 = [k for k in factor1]
                n_factor1[i] = str(num)
                tmp, n_difficulty = explore_answers(n_factor1, factor2, calculating, result, 0)
                difficulty += n_difficulty
                if tmp == -1 or res + tmp > 1:
                    return -1, difficulty
                res += tmp
            return res, difficulty
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
    calculating_expected = []
    for i in reversed([int(i) for i in factor2]):
        calculating_expected.append(int_factor1 * i)
    '''
    calculating_expected = [[i for i in str(j)] for j in calculating_expected]
    for i in range(len(calculating)):
        if len(calculating[i]) != len(calculating_expected[i]):
            return []
        for j, k in zip(calculating[i], calculating_expected[i]):
            if 'x' != j != k:
                return []
    '''
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

def make_problem(difficulty_input, digit):
    max_num = 10 ** digit - 1
    factor1 = randint(1, max_num)
    factor2 = randint(1, max_num)
    result = factor1 * factor2
    #print(factor1, factor2, result)

    calculating = []
    for i in reversed([int(i) for i in str(factor2)]):
        calculating.append(factor1 * i)
    #print(calculating)

    #print_figure(factor1, factor2, calculating, result)

    factor1_split = [i for i in str(factor1)]
    factor2_split = [i for i in str(factor2)]
    calculating_split = [[i for i in str(j)] for j in calculating]
    result_split = [i for i in str(result)]
    num_of_digit = [len(factor1_split), len(factor2_split)]
    for i in calculating_split:
        num_of_digit.append(len(i))
    num_of_digit.append(len(result_split))
    all_digit = sum(num_of_digit)
    for i in range(1, len(num_of_digit)):
        num_of_digit[i] += num_of_digit[i - 1]
    #print(num_of_digit, all_digit)

    holes = []
    len_problem = len(str(factor1)) + len(str(factor2)) - 1
    hole_problem = map_int(difficulty_input, 0, 9, 1, len_problem)
    hole_calc_res = randint(1, all_digit - len_problem - 2)
    for _ in range(hole_problem):
        if len(holes) == all_digit:
            break
        tmp = randint(0, len_problem)
        while tmp in holes:
            tmp = randint(0, len_problem)
        holes.append(tmp)
    for _ in range(hole_calc_res):
        if len(holes) == all_digit:
            break
        tmp = randint(0, all_digit - 1)
        while tmp in holes:
            tmp = randint(0, all_digit - 1)
        holes.append(tmp)
    holes.sort()
    #print('holes', holes)

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

def problem_maker(difficulty_input, digit, timeout=1):
    ans_problem = []
    ans_answer = []
    difficulties = []
    strt = time()
    t = 0
    while time() - strt < timeout and t < 10:
        factor1_hole, factor2_hole, calculating_hole, result_hole, factor1, factor2, calculating, result = make_problem(difficulty_input, digit)
        res_ad, difficulty = explore_answers(factor1_hole, factor2_hole, calculating_hole, result_hole, 0)
        admissible = res_ad == 1
        if not admissible:
            continue
        t += 1
        difficulties.append(difficulty)
        ans_problem.append([''.join(factor1_hole), ''.join(factor2_hole), [''.join(i) for i in calculating_hole], ''.join(result_hole)])
        ans_answer.append([factor1, factor2, calculating, result])
        '''
        difficulty_distance = 0 if difficulty_low <= difficulty <= difficulty_high else min(abs(difficulty_low - difficulty), abs(difficulty_high - difficulty))
        if difficulty_distance == 0:
            ans_problem = [''.join(factor1_hole), ''.join(factor2_hole), [''.join(i) for i in calculating_hole], ''.join(result_hole)]
            ans_answer = [factor1, factor2, calculating, result]
            ans_difficulty = difficulty
            break
        elif difficulty_distance < near_difficulty_distance:
            ans_problem_near = [''.join(factor1_hole), ''.join(factor2_hole), [''.join(i) for i in calculating_hole], ''.join(result_hole)]
            ans_answer_near = [factor1, factor2, calculating, result]
            near_difficulty_distance = difficulty_distance
            ans_difficulty_near = difficulty

        if admissible == 1:
            print('This problem is admissible')
            print('difficulty', cnt)
            print(time() - strt, 'sec')
        else:
            print('This problem should not be asked')
            print(time() - strt, 'sec')
        '''

    print(len(difficulties), 'answers found')
    if ans_problem:
        print('problem found')
        idx = -2
        difficulties_sort = sorted(difficulties)
        key = -1
        if difficulty_input == 0:
            key = difficulties_sort[0]
        elif difficulty_input == 9:
            key = difficulties_sort[-1]
        else:
            key = difficulties_sort[len(difficulties_sort) // 2]
        idx = difficulties.index(key)
        print_figure(ans_problem[idx])
        print('')
        print('answer:')
        print_figure(ans_answer[idx])
        print('difficulty:', difficulties[idx])
        print(time() - strt, 'sec')
        return ans_problem[idx], ans_answer[idx], difficulties[idx]
    else:
        print('problem not found')
        print(time() - strt, 'sec')
        return -1



difficulty_input = int(input('difficulty (0-9): '))
digit = int(input('digit: '))
timeout = 3

res = problem_maker(difficulty_input, digit, timeout)
print(res)