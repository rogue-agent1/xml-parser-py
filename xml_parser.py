"""XML Parser — SAX-style event parser from scratch."""
class XMLNode:
    def __init__(self, tag, attrs=None):
        self.tag = tag; self.attrs = attrs or {}
        self.children = []; self.text = ""
    def __repr__(self): return f"<{self.tag} children={len(self.children)}>"

def parse(xml):
    i = [0]
    def skip_ws():
        while i[0] < len(xml) and xml[i[0]] in ' \t\n\r': i[0] += 1
    def parse_attrs():
        attrs = {}
        while i[0] < len(xml) and xml[i[0]] not in '/>':
            skip_ws()
            if xml[i[0]] in '/>': break
            start = i[0]
            while xml[i[0]] not in '= />': i[0] += 1
            name = xml[start:i[0]]; skip_ws()
            if i[0] < len(xml) and xml[i[0]] == '=':
                i[0] += 1; skip_ws()
                q = xml[i[0]]; i[0] += 1
                start = i[0]
                while xml[i[0]] != q: i[0] += 1
                attrs[name] = xml[start:i[0]]; i[0] += 1
            skip_ws()
        return attrs
    def parse_element():
        skip_ws()
        assert xml[i[0]] == '<'; i[0] += 1
        start = i[0]
        while xml[i[0]] not in ' \t\n/>': i[0] += 1
        tag = xml[start:i[0]]; skip_ws()
        attrs = parse_attrs()
        node = XMLNode(tag, attrs)
        if xml[i[0]:i[0]+2] == '/>':
            i[0] += 2; return node
        assert xml[i[0]] == '>'; i[0] += 1
        # Content
        text_parts = []
        while i[0] < len(xml):
            if xml[i[0]:i[0]+2] == '</':
                i[0] += 2
                while xml[i[0]] != '>': i[0] += 1
                i[0] += 1; break
            elif xml[i[0]] == '<':
                node.children.append(parse_element())
            else:
                start = i[0]
                while i[0] < len(xml) and xml[i[0]] != '<': i[0] += 1
                text_parts.append(xml[start:i[0]])
        node.text = "".join(text_parts).strip()
        return node
    skip_ws()
    if xml[i[0]:].startswith('<?'):
        while xml[i[0]:i[0]+2] != '?>': i[0] += 1
        i[0] += 2
    return parse_element()

if __name__ == "__main__":
    xml = '<root attr="val"><child>Hello</child><empty/><nested><deep>World</deep></nested></root>'
    tree = parse(xml)
    assert tree.tag == "root"
    assert tree.attrs["attr"] == "val"
    assert tree.children[0].text == "Hello"
    assert tree.children[1].tag == "empty"
    assert tree.children[2].children[0].text == "World"
    print(f"Parsed: {tree}, {len(tree.children)} children")
    print("All tests passed!")
