from lxml import etree

class xml_element:

    def create_element(self, tag):
         element = etree.Element(tag, attrib=None, nsmap=None)
         return element

    def create_element_text(self, tag, text):
        element = self.create_element(tag, attrib=None, nsmap=None)
        element.text = text

    def create_sub_element(self, parent, tag):
        element = etree.SubElement(parent, tag, attrib=None, nsmap=None)
        return element

    def create_sub_element_text(self, parent, tag, text):
        element = etree.SubElement(parent, tag, attrib=None, nsmap=None)
        element.text = text

    def write_xml(self, root, path):
        etree.ElementTree(root).write(path,  pretty_print=True, xml_declaration=True, encoding="utf-8", method="xml")






























