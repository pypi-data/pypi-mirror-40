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

def node_str(n, ignore_attrs=[], sort_attr=None):
    attrs = sorted(n.attrib.items())
    index = next((i for i,v in enumerate(attrs) if v[0].lower() == sort_attr), None)
    attrs = [attrs[index]] + attrs[:index] + attrs[index+1:] if index else attrs
    astr = " ".join(attr_str(k,v) for k,v in attrs if k.lower() not in ignore_attrs)
    s = n.tag
    if astr:
        s += " " + astr
    return s



def indent(s, level):
    return "  " * level + s

def write_sorted(stream, node, level=0, cfg={}):

    child_sort_attr, child_sort_method = cfg[level+1]["sort"] if level+1 in cfg else (None, "ascend")
    sort_attr, sort_method = cfg[level]["sort"] if level in cfg else (None, "ascend")
    rsort = False if child_sort_method == "ascend" else True
    child_ignore_attrs = cfg[level+1]["ignore_attrs"] if level+1 in cfg else []
    ignore_attrs = cfg[level]["ignore_attrs"] if level in cfg else []
    ignore_tags = cfg[level]["ignore_tags"] if level in cfg else []
    if node.tag.lower() in ignore_tags:
        return

    children = node.getchildren()
    text = (node.text or "").strip()
    tail = (node.tail or "").strip()

    def node_key(n):
        return node_str(n, child_ignore_attrs, child_sort_attr)

    if children or text:
        children.sort(key=node_key, reverse=rsort)
        stream.write(indent("<" + node_str(node, ignore_attrs, sort_attr) + ">\n", level))

        if text:
            stream.write(indent(text + "\n", level))

        for child in children:
            write_sorted(stream, child, level + 1, cfg)

        stream.write(indent("</" + node.tag + ">\n", level))
    else:
        stream.write(indent("<" + node_str(node, ignore_attrs, sort_attr) + "/>\n", level))

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

def write_sorted_file(fpath, outdir=None, cfg=None):
    if outdir is not None:
        fbasename = os.path.splitext(os.path.basename(fpath))[0]
        sorted_fpath = os.path.join(outdir, "{}.cmp.xml".format(fbasename))
        tmp = unicode_writer(open(sorted_fpath, 'w'))
    else:
        tmp = unicode_writer(NamedTemporaryFile('w'))
    
    tree = ET.parse(fpath)
    write_sorted(tmp, tree.getroot(), cfg=cfg)
    tmp.flush()
    return tmp

def xmldiffs(label1, file1, label2, file2, diffargs=["-u"]):
    args = [ "diff" ]
    args += diffargs
    args += [ "--label", label1, "--label", label2 ]
    args += [ file1.name, file2.name ]
    return subprocess.call(args)


def run_main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("file1", help="diff xml 1", type=str)
    parser.add_argument("file2", help="diff xml 2", type=str)
    parser.add_argument("-o", "--outdir", help="output compared file dir", type=str)
    parser.add_argument("-d", "--diffparams", help="diff tool command line parameters, default=\"-u\")", type=str)
    parser.add_argument("-g", "--cfg", help="config file", type=str)

    
    args = parser.parse_args()
    cfg = read_cfg(args.cfg or "")

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
        write_sorted_file(args.file1, args.outdir, cfg=cfg)
        write_sorted_file(args.file2, args.outdir, cfg=cfg)
        exit(0)
    else:
        file1 = write_sorted_file(args.file1, cfg=cfg)
        file2 = write_sorted_file(args.file2, cfg=cfg)
        exit(xmldiffs(args.file1, file1, args.file2, file2, diffargs))

if __name__ == '__main__':
    run_main()