# -*-coding:utf-8-*-
import collections
import getopt
import os
import sys
current_path = os.path.abspath(os.path.dirname(__file__))
project_path = os.path.abspath("{}/..".format(current_path))
sys.path.append(project_path)
from tools.usage import usage_help
from tools.usage import usage_help

__author__ = 'Allen Woo'


class TempTool:

    def main(self):

        s_ops = "h"
        l_ops = ["path="]
        s_opexplain = ["help"]
        l_opexplain = ["<path>"]
        opts, args = getopt.getopt(sys.argv[1:], s_ops, l_ops)
        if not opts:
            usage_help(s_ops, s_opexplain, l_ops, l_opexplain)

        self.path = None
        for op, value in opts:
            if op == "--path":
                self.path = value

        self.repair()

    def repair(self):

        with open(self.path) as rf:
            lines = rf.readlines()

        old_datas = {}
        msgid = None
        msgstr = None
        for line in lines:
            if not line:
                continue
            if line.startswith("#~ msgid"):
                if msgstr is not None:
                    old_datas[msgid] = msgstr
                msgid = line.lstrip("#~ ")
                msgstr = None
            elif line.startswith("#~ msgstr"):
                msgstr = line.lstrip("#~ ")
            else:
                line = line.lstrip("#~ ")
                if msgid and msgstr is None:
                    msgid = "{}{}".format(msgid, line)
                elif msgstr:
                    msgstr = "{}{}".format(msgstr, line)

        datas = collections.OrderedDict()
        filepath = ""
        msgid = None
        msgstr = None
        for line in lines:
            if not line:
                continue

            if line.startswith("#: "):
                if filepath and msgstr is not None:
                    if msgid in old_datas:
                        msgstr = old_datas[msgid]
                    datas[msgid] = {"msgstr": msgstr, "filepath": filepath}
                    filepath = ""
                filepath = "{}{}".format(filepath, line)
                msgid = None
                msgstr = None
            elif line.startswith("msgid"):

                msgid = line
                msgstr = None
            elif line.startswith("msgstr"):
                msgstr = line
            else:
                if msgid and msgstr is None:
                    msgid = "{}{}".format(msgid, line)
                elif msgstr:
                    msgstr = "{}{}".format(msgstr, line)

        new_po = "{}.new".format(self.path)
        with open(new_po, "w") as wf:

            for k, v in datas.items():
                wf.write(v["filepath"])
                wf.write(k)
                wf.write(v["msgstr"])


if __name__ == '__main__':

    trs = TempTool()
    trs.main()
