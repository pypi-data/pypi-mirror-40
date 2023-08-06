# -*- coding=utf-8 -*-
import os
import re
import sys
import xlrd
import logging
from lxml import etree
import ConfigParser

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Process(object):

    def __init__(self):
        self.Summary = []
        self.TestRun = []
        self.TestPoints = []
        self.Test_Module = []
        self.Match_sheets = []
        self.TestModuleIndex = []
        self.test_points_elements = []
        self.node = ['map', 'node']
        self.column_name = ['Test Module', 'Summary', 'TestRun']

    def clean(self):
        self.Summary = []
        self.TestRun = []
        self.TestPoints = []
        self.Test_Module = []
        self.Match_sheets = []
        self.TestModuleIndex = []
        self.test_points_elements = []

    def open_excel(self, file_path):
        return xlrd.open_workbook(file_path)

    def get_sheet(self, file_path, sheet_name):
        return self.open_excel(file_path).sheet_by_name(sheet_name=sheet_name)

    def get_sheet_names(self, file_path):
        return self.open_excel(file_path).sheet_names()

    def create_root_node(self):
        root_node = etree.Element(self.node[0], version="0.8.1")
        return root_node

    def match_sheets(self, file_path):
        for sheet_name in self.get_sheet_names(file_path):
            match = re.search('TestCase[_-]*', sheet_name)
            if match:
                logging.info(sheet_name)
                self.Match_sheets.append(sheet_name)

    def get_sheet_data(self, file_path, sheet_name):
        TestModule_index = 0
        Summary_index = 0
        TestRun_index = 0
        table = self.get_sheet(file_path, sheet_name)
        rows = table.nrows
        for index, name in enumerate(table.row_values(0)):
            if name == self.column_name[0]:
                TestModule_index = index
            elif name == self.column_name[1]:
                Summary_index = index
            elif name == self.column_name[2]:
                TestRun_index = index

        j = 0
        for row in range(1, rows):
            col_1 = table.cell(row, TestModule_index).value.replace('"', "'")
            col_2 = table.cell(row, Summary_index).value.replace('"', "'")
            col_3 = table.cell(row, TestRun_index).value.replace('"', "'")
            """ filter row empty"""
            if col_1 == "" and col_2 == "":
                j = j + 1
            else:
                self.Test_Module.append(col_1)
                self.Summary.append(col_2)
                self.TestRun.append(col_3)

    def deal_sheet_data(self, file_path, sheet_name, _parent, _testcase):
        self.get_sheet_data(file_path, sheet_name)
        TestRun_Dict = {}
        Summary_Dict = {}
        for k, v in enumerate(self.TestRun):
            TestRun_Dict[k] = v
        for k, v in enumerate(self.Summary):
            Summary_Dict[k] = v

        for (k1, v1), (k2, v2) in zip(TestRun_Dict.items(), Summary_Dict.items()):
            if v1 == "" and v2:
                self.TestPoints.append(k1)
        self.TestPoints.append(len(self.Summary))

        for _TestModule in self.Test_Module:
            if _TestModule:
                self.TestModuleIndex.append(self.Test_Module.index(_TestModule))

        self.TestModuleIndex.append(len(self.Test_Module)+1)

        try:
            i = 0
            for index in range(len(self.TestModuleIndex)-1):
                for _TestModule, _Summary, _TestRun in zip(self.Test_Module[self.TestModuleIndex[i]:self.TestModuleIndex[i+1]],
                                                           self.Summary[self.TestModuleIndex[i]:self.TestModuleIndex[i+1]],
                                                           self.TestRun[self.TestModuleIndex[i]:self.TestModuleIndex[i+1]]):

                    if _TestModule:
                        print _TestModule
                        TestModule_node =etree.SubElement(_parent, self.node[1], TEXT=_TestModule)
                    if _Summary and _TestRun == "":
                        test_point = etree.SubElement(TestModule_node, self.node[1], TEXT=_Summary)
                        self.test_points_elements.append(test_point)
                i = i + 1

        except Exception, e:
            print e

        if _testcase == "true":
            j = 0
            for test_point_element, TestPoint in zip(self.test_points_elements, self.TestPoints[:-1]):
                for _summary in self.Summary[self.TestPoints[j]+1:self.TestPoints[j+1]]:
                    etree.SubElement(test_point_element, self.node[1], TEXT=_summary)
                j += 1

def excel_to_xMind(file_path, project_name, _testcase):
    _process = Process()
    map_node = _process.create_root_node()
    _project_name_node = etree.SubElement(map_node, _process.node[1], TEXT=project_name)
    _process.match_sheets(file_path)
    for sheet in _process.Match_sheets:
        _sheet_name_node = etree.SubElement(_project_name_node, _process.node[1], TEXT=sheet)
        _process.deal_sheet_data(file_path, sheet, _sheet_name_node, _testcase)
        _process.clean()
    etree.ElementTree(map_node).write(os.path.join(BASE_DIR, "%s.mm" % project_name), pretty_print=True, xml_declaration=True, encoding="utf-8", method="xml")

if __name__ == "__main__":
    conf = ConfigParser.ConfigParser()
    conf.read(os.path.join(BASE_DIR, "config.ini"))
    excel_file_name = conf.get(conf.sections()[0], "excel_file_name")
    project_name = conf.get(conf.sections()[0], "project_name")
    is_test_level = conf.get(conf.sections()[0], "is_test_level")
    file_path = os.path.join(BASE_DIR, excel_file_name)
    excel_to_xMind(file_path, project_name, _testcase=is_test_level)
    print "sccess"






















