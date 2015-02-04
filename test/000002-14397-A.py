# -*- coding: utf-8 -*-
import argparse
import comparator
if __name__ == "__main__":
    desc = "code_diff путь к папке с поссылками за контест [-diff путь к программе сравнения файлов]" \
           "code_diff сравнивает попарно посслыки разных пользователей на похожесть и если пара" \
           " подозрительна " \
           "показывает в программе сравнения по умолчанию ./kdiff3" \
           "в папке с поссылками за контест файлы должны назваться runid-userid-problem.{language suffix}"
    parser = argparse.ArgumentParser(description=desc, prog="code_diff")
    parser.add_argument('contest_folder', help='путь к папке с поссылками')
    parser.add_argument('-d', '--diff', default="kdiff3", help='путь к программе сравнения файлов(kdiff3, vimdiff, '                                                           'diff и т.д.)')
    parser.add_argument('-l', '--log', default="code_diff.log", help='путь к файлу, где сохраняются подозрительные программы')
    args = parser.parse_args()

    comparator.compare_all(args.contest_folder, args.diff, args.log)
