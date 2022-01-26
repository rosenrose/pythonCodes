import sys
from lxml import etree

data = open(sys.argv[1],encoding="utf-8").read()
# data = "\n".join([i.lstrip() for i in data.splitlines()])
xml = etree.fromstring(data,parser=etree.HTMLParser(encoding="utf-8"))
etree.indent(xml,space=" "*int(sys.argv[2]))
xml = etree.tostring(xml,encoding="utf-8",method="html",doctype="<!DOCTYPE html>")
open(sys.argv[1],"w",encoding="utf-8").write(xml.decode("utf-8"))