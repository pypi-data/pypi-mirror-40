# -*- coding:utf-8 -*-
import os
import re
import xlrd
import logging
import ConfigParser
from comm_xml import *

logging.basicConfig(level=logging.INFO)
Base_dir = os.path.dirname(os.path.abspath(__file__))

class Config():
    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read(os.path.join(Base_dir, "config.ini"))
        sections = conf.sections()
        if os.path.exists(conf.get(sections[0], "excel_file_name")):
            self.excel_file_path = conf.get(sections[0], "excel_file_name")
        else:
            raise Exception("%s current path not find! please modify the path" % conf.get(sections[0], "excel_file_name"))
        if os.path.exists(conf.get(sections[0], "export_xml_file_name")):
            self.write_xml_file_path = conf.get(sections[0], "export_xml_file_name")
        else:
            self.write_xml_file_path = os.path.join(Base_dir, conf.get(sections[0], "export_xml_file_name"))
        self.project_name = conf.get(sections[0], "project_name")
        # self.user = conf.get(sections[1], "user")
        # self.password = conf.get(sections[1], "password")

_Config = Config()

sectionlist = []

class Excel(xml_element):
    def __init__(self):
        self.project_name = ""
        self.Test_Modules = []
        self.Test_Module = []
        self.TestPoint = []
        self.TestRun = []
        self.Summary = []
        self.Description = []
        self.ExpectedResults = []

    def clean(self):
        self.Test_Module = []
        self.TestRun = []
        self.Summary = []
        self.Description = []
        self.ExpectedResults = []
        self.TestPoint = []
        self.Test_Modules = []

    def open_excel(self, path):
        return xlrd.open_workbook(path)

    def get_sheet(self, path, sheet_name):
        return self.open_excel(path=path).sheet_by_name(sheet_name=sheet_name)

    def get_sheet_names(self, path):
        return self.open_excel(path=path).sheet_names()

    def get_sheet_data(self, path, sheet_name):
        table = self.get_sheet(path, sheet_name)
        rows = table.nrows
        Test_Module_index = 0
        Summary_index = 0
        Test_Level_index = 0
        TestRun_index = 0
        Description_index = 0
        ExpectedResults_index = 0

        for index, name in enumerate(table.row_values(0)):
            if name == "Test Module":
                Test_Module_index = index
            elif name == "Test Level":
                Test_Level_index = index
            elif name == "TestRun":
                TestRun_index = index
            elif name == "Summary":
                Summary_index = index
            elif name == "Description":
                Description_index = index
            elif name == "ExpectedResults":
                ExpectedResults_index = index

        j = 0
        for row in range(1, rows):
            _Test_Module = table.cell(row, Test_Module_index).value.replace('"', "'")
            _Test_Level = table.cell(row, Test_Level_index).value.replace('"', "'")
            _TestRun = table.cell(row, TestRun_index).value.replace('"', "'")
            _Summary = table.cell(row, Summary_index).value.replace('"', "'")
            _ExpectedResults = table.cell(row, ExpectedResults_index).value.replace('"', "'")
            _Description = table.cell(row, Description_index).value.replace('"', "'")
            """ filter empty row """
            if _Test_Module == "" and _Test_Level == "" and _TestRun == "" \
                    and _Summary == "" and _ExpectedResults == "" and _Description == "":
                j = j + 1
            else:
                self.Test_Module.append(_Test_Module)
                self.TestRun.append(_TestRun)
                if len(_Summary) > 200:
                    raise Exception(
                        "SheetName is: %s; \n row is: %s ;check this row value.\n summary is: %s" %
                        (sheet_name, row - j + 1, _Summary))
                else:
                    self.Summary.append(_Summary)
                if len(_Description) > 1500:
                    raise Exception(
                        "SheetName is: %s; \n row is: %s ;check this row value.\n Description is: %s".format(sheet_name, row - j + 1, _Description))
                else:
                    self.Description.append(_Description)
                self.ExpectedResults.append(_ExpectedResults)
        self._get_test_point()
        self._get_test_module()


    def _get_test_point(self):
        """get test point"""
        TestRun_Dict = {}
        Summary_Dict = {}

        for k, v in enumerate(self.TestRun):
            TestRun_Dict[k] = v

        for k, v in enumerate(self.Summary):
            Summary_Dict[k] = v

        for (k1, v1), (k2, v2) in zip(TestRun_Dict.items(), Summary_Dict.items()):
            if v1 == "" and v2:
                self.TestPoint.append(k1)
        self.TestPoint.append(len(self.Summary))


    def _get_test_module(self):
        if len(self.Test_Module) != 0:
            for module in self.Test_Module:
                if module:
                    self.Test_Modules.append(self.Test_Module.index(module))
            self.Test_Modules.append(len(self.Test_Module)+1)
        else:
            raise Exception("Test Module value is empty")

    def create_xml_root(self):
        return etree.Element("suite")

    def create_xml_header(self, root, project_name):
        etree.SubElement(root, "master")
        self.create_sub_element_text(root, "id", "S5")
        self.create_sub_element(root, "description")
        sections = etree.SubElement(root, "sections")
        section = etree.SubElement(sections, "section")
        self.create_sub_element_text(section, "name", project_name)
        etree.SubElement(section, "description")
        return section


    def deal_sheet_data(self, test_sheet=False):
        list_cases = []
        for TestModuleValue, TestRunValue, SummaryValue in zip(self.Test_Module, self.TestRun, self.Summary):

            if TestModuleValue:
                if test_sheet is False:
                    section1 = self.create_element("section")
                    sectionlist.append(section1)
                    self.create_sub_element_text(section1, "name", TestModuleValue)
                    self.create_sub_element(section1, "description")
                    sections2 = self.create_sub_element(section1, "sections")

            if TestRunValue == "" and SummaryValue.strip():
                section2 = self.create_sub_element(sections2, "section")
                self.create_sub_element_text(section2, "name", SummaryValue)
                self.create_sub_element(section2, "description")
                cases = self.create_sub_element(section2, "cases")
                list_cases.append(cases)

        i = 0
        for case, testPoint in zip(list_cases, self.TestPoint[:-1]):
            for SummaryValue, TestRunValue, DescriptionValue, ExpectedResultsValue in zip(
                    self.Summary[int(self.TestPoint[i]) + 1:int(self.TestPoint[i + 1])],
                    self.TestRun[int(self.TestPoint[i]) + 1:int(self.TestPoint[i + 1])],
                    self.Description[int(self.TestPoint[i]) + 1:int(self.TestPoint[i + 1])],
                    self.ExpectedResults[int(self.TestPoint[i]) + 1:int(self.TestPoint[i + 1])]):

                caseElement = etree.SubElement(case, "case")
                self.create_sub_element_text(caseElement, "id", "110")
                self.create_sub_element_text(caseElement, "title", SummaryValue)
                self.create_sub_element_text(caseElement, "template", "Test Case (Text)")
                self.create_sub_element_text(caseElement, "type", "Other")
                self.create_sub_element_text(caseElement, "priority", "Medium")
                customElement = etree.SubElement(caseElement, "custom")
                self.create_sub_element_text(customElement, "test_run", TestRunValue)
                if DescriptionValue:
                    self.create_sub_element_text(customElement, "case_description", DescriptionValue)
                else:
                    self.create_sub_element_text(customElement, "case_description", SummaryValue)
                self.create_sub_element_text(customElement, "expected", ExpectedResultsValue)
            i += 1

data = Excel()

def cratet_xml_file(data, excel_file_path, sheets):
    for sheet_name in sheets:
        data.get_sheet_data(excel_file_path, sheet_name)
        data.deal_sheet_data()
        data.clean()

def excle_to_xml(excel_file_path, project_name, write_xml_file_path):
    root = data.create_xml_root()
    section = data.create_xml_header(root, project_name)
    sheets = []
    for sheet_name in data.get_sheet_names(excel_file_path):
        match = re.search("TestCase[_-]*", sheet_name)
        if match:
            logging.info(sheet_name)
            sheets.append(sheet_name)
    cratet_xml_file(data, excel_file_path, sheets)
    sections1 = data.create_sub_element(section, "sections")
    """"""
    for section in sectionlist:
        sections1.append(section)
    data.write_xml(root, write_xml_file_path)
    logging.info("write xml file success!")

if __name__ == "__main__":
    excle_to_xml(_Config.excel_file_path, _Config.project_name, _Config.write_xml_file_path)
