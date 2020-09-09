# TIMES
from random import randint
from time import time

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


def explore_answers(factor1, factor2, calculating, result):
    global difficulty
    difficulty += 1
    print(factor1, factor2, calculating, result)
    for i, j in enumerate(factor1):
        if j == 'x':
            res = 0
            for num in range(10):
                n_factor1 = [k for k in factor1]
                n_factor1[i] = str(num)
                tmp = explore_answers(n_factor1, factor2, calculating, result)
                if tmp == -1 or res + tmp > 1:
                    return -1
                res += tmp
            return res
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
                    tmp = explore_answers(factor1, n_factor2, calculating, result)
                    if tmp == -1 or res + tmp > 1:
                        return -1
                    res += tmp
            return res
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
        return 0
    for i, j in zip(result, result_expected):
        if 'x' != i != j:
            return 0
    return 1

def make_problem(mn_factor, mx_factor, num_of_holes):
    factor1 = randint(mn_factor, mx_factor)
    factor2 = randint(mn_factor, mx_factor)
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
    for _ in range(num_of_holes):
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


difficulty_input = int(input('difficulty (0, 1, 2): '))
mn_factor = int(input('min factor: '))
mx_factor = int(input('max factor: '))
num_of_holes = int(input('number of holes: '))

ans_problem = []
ans_answer = []
difficulties = []

strt = time()
timeout = 1
while time() - strt < timeout:
    factor1_hole, factor2_hole, calculating_hole, result_hole, factor1, factor2, calculating, result = make_problem(mn_factor, mx_factor, num_of_holes)
    difficulty = 0
    admissible = explore_answers(factor1_hole, factor2_hole, calculating_hole, result_hole) == 1
    if not admissible:
        continue
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
    if difficulty_input == 0:
        idx = 0
    elif difficulty_input == 2:
        idx = -1
    else:
        difficulties_sort = sorted(difficulties)
        median = difficulties_sort[len(difficulties_sort) // 2]
        idx = difficulties.index(median)
    print_figure(ans_problem[idx])
    print('')
    print('answer:')
    print_figure(ans_answer[idx])
    print('difficulty:', difficulties[idx])
else:
    print('problem not found')
print(time() - strt, 'sec')

