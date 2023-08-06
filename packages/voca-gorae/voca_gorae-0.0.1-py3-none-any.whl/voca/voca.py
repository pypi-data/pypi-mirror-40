import argparse
import random

import pandas as pd

from flask import Flask, render_template

app = Flask(__name__)

swap = [None, None]


def _exel2dict(file_name, _range=1):
    xls = pd.ExcelFile(file_name + ".xlsx")
    df = xls.parse(xls.sheet_names[0])

    # Todo: pandas indexing to 0, 1
    df[0] = df.pop("Unnamed: 1")
    df[1] = df.pop("Unnamed: 2")

    _dict = {}
    for i in range(_range, len(df[0])):
        _i = random.choice([0, 1])
        _dict[df[_i][i]] = df[_i ^ 1][i]
    return _dict


def _mix_dict(_dict):
    q_rand = random.sample([key for key in _dict.keys()], len(_dict))
    return q_rand, [_dict[i] for i in q_rand]


def _save2exel(question, answer, name):
    writer = pd.ExcelWriter(name + ".xlsx")

    pd.DataFrame({"질문": question}).to_excel(writer, sheet_name="질문")
    pd.DataFrame({"정답": answer}).to_excel(writer, sheet_name="정답")

    writer.save()


@app.route("/")
def _qustion():
    return render_template("index.html", q=swap[0])


@app.route("/a")
def _answer():
    return render_template("index.html", q=swap[0], a=swap[1])


def _get_parser():
    parser = argparse.ArgumentParser(usage="[path] [-s] [-i]")
    parser.add_argument("path", help="path of excel")
    parser.add_argument(
        "-s",
        "--save",
        help='where to save file. default is "exam"',
        default="exam",
        type=str,
    )
    parser.add_argument(
        "-i",
        "--index",
        help='Set the parsing loction of columm. default is "1"',
        # default,
        type=int,
    )
    parser.add_argument("-w", "--web", help="Show on web", action="store_true")
    return parser


def command_line_runner():
    parser = _get_parser()
    args = vars(parser.parse_args())

    if not args["path"]:
        print(parser.print_help())
        return

    if args["index"]:
        _dict = _exel2dict(args["path"], args["index"])
    else:
        _dict = _exel2dict(args["path"])

    swap[0], swap[1] = _mix_dict(_dict)
    _save2exel(swap[0], swap[1], args["save"])

    if args["web"]:
        app.run()


if __name__ == "__main__":
    command_line_runner()
