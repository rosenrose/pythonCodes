import sys
from lxml import etree
from pathlib import Path

path = Path(sys.argv[1]).resolve()
extList = [".html",".xml"]

def indentation(element, level=0, indent="  "):
    i = "\n" + level*indent
    if len(element):
        if not element.text or not element.text.strip():
            element.text = i + indent
        if not element.tail or not element.tail.strip():
            element.tail = i
        for elem in element:
            indentation(elem, level+1)
        if not element.tail or not element.tail.strip():
            element.tail = i
    else:
        if level and (not element.tail or not element.tail.strip()):
            element.tail = i

for file in [i for i in path.rglob("*") if i.is_file() and i.suffix in extList]:
    parser = etree.HTMLParser(encoding="utf-8") if file.suffix==".html" else etree.XMLParser(encoding="utf-8")
    xml = etree.fromstring((data:=file.read_text(encoding="utf-8")),parser=parser)
    etree.indent(xml, space="  ")
    # indentation(xml)
    if file.suffix == ".html":
        xml = etree.tostring(xml,encoding="utf-8",method="html",doctype="<!DOCTYPE html>").decode("utf-8")
    elif file.suffix == "xml":
        xml = etree.tostring(xml,encoding="utf-8",method="xml").decode("utf-8")

    if xml != data:
        file.write_text(xml,encoding="utf-8")
        print(file.relative_to(path))
    # xml = etree.parse(str(file),parser=parser)
    # xml.write(str(file),pretty_print=True,encoding="utf-8")
    
