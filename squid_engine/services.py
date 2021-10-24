import os,io
import re
import requests
import tempfile
import operator
from .models import *
import lxml.etree as ET
from zipfile import ZipFile
from requests.auth import HTTPBasicAuth
from django.core.files.storage import FileSystemStorage

class game_play(object):
    def __init__(self, level):
        self.code_base = ''
        self.level = level
        self.rules = self.fetch_rules()
        self.validations = []
        self.bugs = {}
        self.status = 'DisQualified'
        self.apiName = ''

    def code_base_git(self, repoName, branch):
        url = 'https://github.com/Seventh-Dimension/'+repoName + '/archive/refs/heads/'+branch+'.zip'
        print("~~~~~ Git URL ->", url)
        repo_response = requests.get(url, stream=True)
        print("~~~~~ Fetched from Git Repo -> ", repo_response.url, repo_response.status_code)
        zip = ZipFile(io.BytesIO(repo_response.content))
        temp_path = tempfile.mkdtemp()
        zip.extractall(path=temp_path)
        self.code_base = os.path.join(temp_path,repoName+'-'+branch)
        self.apiName = repoName
        print("~~~~~ Extracting content ~~~~", self.code_base)

    def fetch_rules(self):
        proj = Level.objects.get(Name=self.level)
        print("~~~~~ Fetching Rules ~~~~~")
        return proj.Rules.all()

    def code_validations(self):
        print("~~~~~ Code Rules ~~~~~ ")
        rules_list = [rule for rule in self.rules]
        xprules = Code_Rule.objects.filter(Name__in=rules_list)
        val=[]
        for xprule in xprules:
            print("~~~~~ RULE -> ",xprule.Name)
            scan_path = os.path.join(self.code_base,xprule.Location.url())
            print("~~~~~ SCAN PATH -> ",scan_path)
            if scan_path.endswith('.xml'):
                xml_list = [scan_path]
            else:
                xml_list = [os.path.abspath(os.path.join(root, files)) for root, dirs, files in os.walk(scan_path) for
                            files in files if files.endswith('.xml')]
            print(xml_list)
            for xml in xml_list:
                print("~~~~~ File    -> ", os.path.relpath(xml, self.code_base))
                try:
                    xpvalue = squid_utils.xpath_evaluation(xml, xprule.Condition)
                    status = squid_utils.compare(xpvalue, xprule.Comparator, xprule.Expected_Value)
                    res = {'rule': xprule.Name, 'rule_desc': xprule.Description, 'criticality': xprule.Gatekeeper.Name,
                               'location': os.path.relpath(xml, self.code_base), 'status': status}
                    print("~~~~~ Result  -> ", status)
                    val.append(res)
                except:
                    res = {'rule': xprule.Name, 'rule_desc': 'XML File Not Found! Please check the folder structure standards', 'criticality': xprule.Gatekeeper.Name,
                           'location': os.path.relpath(xml, self.code_base), 'status': True}
                    print("~~~~~ Result  -> ", True)
                    val.append(res)
        self.validations.extend(val)
    def folder_validations(self):
        rules_list = [rule for rule in self.rules]
        val = []
        fsrules = Folder_Structure_Rule.objects.filter(Name__in=rules_list)
        print("~~~~~ Folder Structure Rules ~~~~~~")
        for fsrule in fsrules:
            print("~~~~~ RULE -> ", fsrule.Name)
            root_dir = fsrule.Location.url()
            scan_path = os.path.join(self.code_base, root_dir)
            files_list = [files for root, dirs, files in os.walk(scan_path) for files in files]
            folder_list = [dirs for root, dirs, files in os.walk(scan_path) for dirs in dirs]
            if fsrule.Condition == "directoryName":
                print("~~~~~ Folder check -> ", scan_path)
                flist = folder_list
            elif fsrule.Condition == "fileName":
                print("~~~~~ File check ->", scan_path)
                flist = files_list
            status = not True in [
                squid_utils.compare(f, fsrule.Comparator, fsrule.Expected_Value) for f
                in flist]

            res = {'rule': fsrule.Name, 'rule_desc': fsrule.Description, 'criticality': fsrule.Gatekeeper.Name,
                   'location': os.path.relpath(scan_path, self.code_base), 'status': status,
                   }
            print("~~~~~ Files    ->", flist)
            print("~~~~~ Result   -> ", status)
            val.append(res)
        self.validations.extend(val)

    def getBugs(self):
        for bug in self.validations:
            if (bug['status']):
                self.bugs.setdefault(bug['criticality'], []).append(bug)

    def getStatus(self):
        bugs = self.bugs
        s = True in [len(bugs.get(criticality.Name,'')) > criticality.Max_Allowed for criticality in Gatekeeper.objects.all()]
        print("~~~~~ STATUS LIST->",[len(bugs.get(criticality.Name,'')) > criticality.Max_Allowed for criticality in Gatekeeper.objects.all()])
        if s:
            self.status= 'DisQualified'
        else:
            self.status= 'Qualified'

class squid_utils():
    @staticmethod
    def xpath_evaluation(xml,xpath_exp):
        doc = ET.parse(xml)
        return doc.xpath(xpath_exp)
    @staticmethod
    def compare(input,operation,exp_value):
        print("~~~~~ INPUT -> ",input)
        print("~~~~~ Operation -> ",operation)
        print("~~~~~ Expected Value -> ",exp_value)
        ops = {'>': operator.gt,
               '<': operator.lt,
               '>=': operator.ge,
               '<=': operator.le,
               '=': operator.eq,
               '!=': operator.ne,
               "endsWith": str.endswith,
               "startsWith": str.startswith,
               "contains": operator.contains,
               "regex":squid_utils.regex_imp,
               }
        if operation == 'regex':
            res = ops[operation](input, exp_value)
        else:
            res = ops[operation](str(input),exp_value)
        return res

    @staticmethod
    def regex_imp(string,pattern):
        print("~~~~~ Regex String -> ", string)
        print("~~~~~ Regex Pattern -> ", pattern)
        for re_str in string:
            print("~~~~~ Re str ->",re_str)
            reg_res = re.match(pattern,re_str)
            if reg_res:
                print("~~~~~ Regex Res False ->",reg_res)
                return False
            else:
                print("~~~~~ Regex Res True->", reg_res)
                return True


