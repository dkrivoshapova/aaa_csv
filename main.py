import csv


def read_file(filename: str) -> list:
    '''Return data from csv file'''
    with open(filename, newline='') as csvfile:
        spamreader = list(csv.reader(csvfile, delimiter=';'))
        return spamreader


def menu() -> None:
    '''Print options'''
    print('Введите номер действия, которое хотите совершить:')
    options_map = ['    1. Вывести в понятном виде иерархию команд',
                   '    2. Вывести сводный отчёт по департаментам ',
                   '    3. Выгрузить сводный отчёт по департаментам в csv',
                   '    4. Завершить программу']
    print(*options_map, sep='\n')


def get_answer() -> int:
    '''Geting and processing of the response'''
    menu()
    answer = input()
    int_answer = 0
    try:
        int_answer = int(answer)
        if int_answer not in [1, 2, 3, 4]:
            print('Неверный формат! Введите только число 1, 2, 3 или 4')
            int_answer = get_answer()
    except Exception:
        print('Неверный формат! Введите только число 1, 2, 3 или 4')
        int_answer = get_answer()
    return int_answer


def select_option(answer: int, hierarchy: dict, report: dict) -> None:
    '''Execute a function depending on the response'''
    if answer == 1:
        print_command_hierarchy(hierarchy)
    if answer == 2:
        print_report(report)
    if answer == 3:
        report_to_csv(report)


def get_command_hierarchy(data: list) -> dict[str, list]:
    '''Form a hierarchy of departments'''
    hierarchy: dict[str, list] = {}
    for i in range(1, len(data)):
        if data[i][1] in hierarchy:
            hierarchy[data[i][1]].append(data[i][2])
        else:
            hierarchy[data[i][1]] = [data[i][2]]
    return hierarchy


def print_command_hierarchy(hierarchy: dict) -> None:
    '''Print a hierarchy of departments'''
    for k, v in hierarchy.items():
        print('Департамент: ', k)
        print('Команды:', end=' ')
        print(*list(set(v)), sep=', ', end='\n\n')


def get_report(data: list) -> dict[str, list]:
    '''Form a report by department'''
    report: dict[str, list] = {}
    for i in range(1, len(data)):
        if data[i][2] in report:
            report[data[i][2]].append(float(data[i][5]))
        else:
            report[data[i][2]] = [float(data[i][5])]
    result = {}
    for k, v in report.items():
        result[k] = [len(v), min(v), max(v), int(sum(v)/len(v))]
    return result


def print_report(report: dict[str, list]) -> None:
    '''Print a report by department'''
    print('')
    print('{:<22}{:<10} {:<20}{:<25}'.format('Название',
          'Численность', 'Зарплатная вилка', 'Средняя зарплата'))
    for name, data in report.items():
        count, min, max, mean = data
        print('{:<22} {:<10} {:<20} {:<25}'.format(
            name, count, str(min) + ' - ' + str(max), mean))
    print('')


def report_to_csv(report: dict[str, list]) -> None:
    '''Export a report by department to csv file'''
    with open('report.csv', 'w', newline='') as output_file:
        data_writer = csv.writer(output_file,  delimiter=';')
        data_writer.writerow(['Название', 'Численность',
                              'Минимальная зарплата', 'Максимальная зарплата',
                              'Средняя зарплата'])
        for k, v in report.items():
            data_writer.writerow([k] + v)
    print('Отчет успешно выгружен в текущую деректорию с названием report.csv')


if __name__ == '__main__':
    data = read_file('Corp_Summary.csv')
    hierarchy = get_command_hierarchy(data)
    report = get_report(data)
    answer = get_answer()
    while answer != 4:
        select_option(answer, hierarchy, report)
        answer = get_answer()
