from back import problem_maker

difficulty_input = int(input('difficulty (0-9): '))
digit = int(input('digit: '))
timeout = 3

res = problem_maker(difficulty_input, digit, timeout)
print(res)