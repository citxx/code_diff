# -*- coding: utf-8 -*-
import argparse
import comparator
import os

if __name__ == "__main__":
    desc = "code_diff сравнивает попарно посслыки разных пользователей на похожесть и если пара" \
           " подозрительна " \
           "показывает в программе сравнения (по умолчанию ./kdiff3) " \
           "в папке с поссылками за контест файлы должны назваться runid-userid-problem.{language suffix}"
    parser = argparse.ArgumentParser(description=desc, prog="code_diff")
    parser.add_argument('contest_folder', help='путь к папке с поссылками')
    parser.add_argument('-d', '--diff', default="./kdiff3", help='путь к программе сравнения файлов(kdiff3, vimdiff, '
                                                               'diff и т.д.)')
    parser.add_argument('-l', '--log', default="./code_diff.log",
                        help='путь к файлу, где сохраняются подозрительные программы')
    parser.add_argument('-m', '--mode', default='last', choices=['all', 'last'], help='режим работы; all - проверять все '
                                                                                      'поссылки; last - проверять только '
                                                                                      'последнюю поссылку пользователя по '
                                                                                      'каждой задаче')
    parser.add_argument('-w', '--without-problem', dest='without', action="append",  help='задача которую не нужно проверять, '
                                                                                          'можно использовать несколько раз, если таких '
                                                                                          'задач много')
    parser.add_argument('--version', action='version', version='%(prog)s 0.0')
    parser.add_argument('--max-common-len', '-mcl', type=float, dest='mcl', help='максимальное соотношение '
                                                                               'при котором файлы считаются не '
                                                                               'подозрительными')
    parser.add_argument('-q', '--quiet', action="store_true", help='если указан парметр, то все подозрительные просто '
                                                                   'будут сохранены в log, и не будет вызываться '
                                                                   'программа сравнения')
    args = parser.parse_args()

    if args.without is None:
        args.without = list()

    if args.mode == "last":
        comparator.compare_list(comparator.choice_last(os.listdir(args.contest_folder)), args.contest_folder,
                                args.diff, args.log, args.without, args.mcl, args.quiet)
    else:
        comparator.compare_all(args.contest_folder, args.diff, args.log, args.without, args.mcl, args.quiet)
