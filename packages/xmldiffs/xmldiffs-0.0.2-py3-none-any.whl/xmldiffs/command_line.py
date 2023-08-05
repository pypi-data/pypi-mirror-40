# Compare two XML files, with some customized options.
#
# Copyright (C) 2018 ZIJIAN JIANG
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
xmldiffs  Copyright (C) 2018  ZIJIAN JIANG

This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details.

Compare two XML files, with some customized options.
Any extra options are passed to the `diff' command.
"""
from __future__ import print_function, unicode_literals
import sys
import os
import io
import re
import xml.etree.ElementTree as ET
from tempfile import NamedTemporaryFile
import subprocess
import argparse
import configparser

config = None

def read_cfg(cfg_fpath):
    diff_cfg = {}

    config = configparser.ConfigParser()
    config.read(cfg_fpath)

    sections = config.sections()
    for section in sections:
        level, prop = section.split('.')
        dlevel = int(re.search(r"(\d+)$", level).group())
        if dlevel not in diff_cfg:
            diff_cfg[dlevel] = {
                "ignore_tags": [],
                "ignore_attrs": [],
                "sort": (None, "ascend")
            }
        for key in config[section]:
            if config[section][key] == "ignore" and prop == "tags":
                diff_cfg[dlevel]["ignore_tags"].append(key)
            if config[section][key] == "ignore" and prop == "attributes":
                diff_cfg[dlevel]["ignore_attrs"].append(key)
            if config[section][key] == "ascend":
                diff_cfg[dlevel]["sort"] = (key, "ascend")
            if config[section][key] == "descend":
                diff_cfg[dlevel]["sort"] = (key, "descend")
    #!for
    return diff_cfg

def attr_str(k, v):
    return "{}=\"{}\"".format(k,v)

def node_str(n, level, ignore_attrs=[], sort_attr=None, rsort=False):
    attrs = sorted(n.attrib.items()) if not rsort else reversed(sorted(n.attrib.items()))
    index = next((i for i,v in enumerate(attrs) if v[0].lower() == sort_attr), None)
    attrs = [attrs[index]] + attrs[:index] + attrs[index+1:] if index else attrs
    astr = " ".join(attr_str(k,v) for k,v in attrs if k.lower() not in ignore_attrs)
    s = n.tag
    if astr:
        s += " " + astr
    return s



def indent(s, level):
    return "  " * level + s

def write_sorted(stream, node, level=0):

    sort_attr, sort_method = config[level]["sort"] if level in config else (None, "ascend")
    rsort = False if sort_method == "ascend" else True
    ignore_attrs = config[level]["ignore_attrs"] if level in config else []
    ignore_tags = config[level]["ignore_tags"] if level in config else []
    if node.tag.lower() in ignore_tags:
        return

    children = node.getchildren()
    text = (node.text or "").strip()
    tail = (node.tail or "").strip()

    def node_key(n):
        return node_str(n, level, ignore_attrs, sort_attr, rsort)

    if children or text:
        children.sort(key=node_key)

        stream.write(indent("<" + node_str(node, level, ignore_attrs, sort_attr, rsort) + ">\n", level))

        if text:
            stream.write(indent(text + "\n", level))

        for child in children:
            write_sorted(stream, child, level + 1)

        stream.write(indent("</" + node.tag + ">\n", level))
    else:
        stream.write(indent("<" + node_str(node, level, ignore_attrs, sort_attr, rsort) + "/>\n", level))

    if tail:
        stream.write(indent(tail + "\n", level))

if sys.version_info < (3, 0):
    # Python 2
    import codecs
    def unicode_writer(fp):
        return codecs.getwriter('utf-8')(fp)
else:
    # Python 3
    def unicode_writer(fp):
        return fp

def write_sorted_files(file1_path, file2_path, outdir=None):
    if outdir is not None:
        file1_basename = os.path.splitext(os.path.basename(file1_path))[0]
        file2_basename = os.path.splitext(os.path.basename(file2_path))[0]
        sorted_file1_path = os.path.join(outdir, "{}.cmp.xml".format(file1_basename))
        sorted_file2_path = os.path.join(outdir, "{}.cmp.xml".format(file2_basename))
        tmp1 = unicode_writer(open(sorted_file1_path, 'w'))
        tmp2 = unicode_writer(open(sorted_file2_path, 'w'))
    else:
        tmp1 = unicode_writer(NamedTemporaryFile('w'))
        tmp2 = unicode_writer(NamedTemporaryFile('w'))

    tree = ET.parse(file1_path)
    write_sorted(tmp1, tree.getroot())
    tmp1.flush()

    tree = ET.parse(file2_path)
    write_sorted(tmp2, tree.getroot())
    tmp2.flush()
    return tmp1, tmp2

def xmldiffs(label1, file1, label2, file2, diffargs=["-u"]):
    args = [ "diff" ]
    args += diffargs
    args += [ "--label", label1, "--label", label2 ]
    args += [ file1.name, file2.name ]
    return subprocess.call(args)


def run_main():
    global config
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("file1", help="diff xml 1", type=str)
    parser.add_argument("file2", help="diff xml 2", type=str)
    parser.add_argument("-o", "--outdir", help="output compared file dir", type=str)
    parser.add_argument("-d", "--diffparams", help="diff tool command line parameters, default=\"-u\")", type=str)
    parser.add_argument("-g", "--cfg", help="config file", type=str)

    
    args = parser.parse_args()
    config = read_cfg(args.cfg or "")

    if not os.path.isfile(args.file1):
        print("xmldiffs: File {} is not valid".format(args.file1))
        exit(-1)
    if not os.path.isfile(args.file2):
        print("xmldiffs: File {} is not valid".format(args.file2))
        exit(-1)
    if args.outdir and not os.path.isdir(args.outdir):
        print("xmldiffs: Directory {} is not valid".format(args.outdir))
        exit(-1)
    diffargs = args.diffparams.split(" ") if args.diffparams else ["-u"]
    if args.outdir:
        write_sorted_files(args.file1, args.file2, args.outdir)
        exit(0)
    else:
        file1, file2 = write_sorted_files(args.file1, args.file2)
        exit(xmldiffs(args.file1, file1, args.file2, file2, diffargs))


if __name__ == '__main__':
    run_main()