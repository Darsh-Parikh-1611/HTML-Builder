from utility import *
import os
###############################################################################
class RuleExtractionError(StopIteration):
    def __init__(self, message="") -> None:
        super().__init__(message)
class TemplateExtractionError(StopIteration):
    def __init__(self, message="") -> None:
        super().__init__(message)
class ContentExtractionError(StopIteration):
    def __init__(self, message="") -> None:
        super().__init__(message)
###############################################################################
#------------------------------------------------------------------------------
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# Aspects of the sections manager:
#       - Extracts key sections of the rules, templates, and content files:
#               - Rule     : #Head
#               - Rule     : #Templates
#               - Rule     : #Data
#               - Template : #Script
#               - Template : #Body
#               - Content  : Item
#               - Content  : Text
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#------------------------------------------------------------------------------
def extractRuleSections(rule_file):
    rules = filter(None, (line.rstrip() for line in rule_file))
    rule_sections = {
        "Head" : {
            "title"  : "",
            "author" : ""
        },
        "Templates" : {
            "header" : "",
            "body"   : "",
            "footer" : ""
        } ,
        "Title" : "",
        "Data"  : []
    }
    if not find(rules, "# Head"):
        raise RuleExtractionError("\'# Head\' section not found")
    rule_sections["Head"]["title"]  = str(next(rules))
    rule_sections["Head"]["author"] = str(next(rules))
    rule_sections["Title"] = str(next(rules))
    if not find(rules, "# Templates"):
        raise RuleExtractionError("\'# Templates\' section not found")
    rule_sections["Templates"]["header"] = str(next(rules))
    rule_sections["Templates"]["body"]   = str(next(rules))
    rule_sections["Templates"]["footer"] = str(next(rules))
    if not find(rules, "# Data"):
        raise RuleExtractionError("\'# Data\' section not found")
    while True:
        try:
            rule_sections["Data"].append(str(next(rules)))
        except StopIteration:
            break
    return rule_sections
#------------------------------------------------------------------------------
def extractTemplateSections(template_file):
    lines = filter(None, (line.rstrip() for line in template_file))
    templ_sections = {
        "Script" : [],
        "Body"   : []
    }
    if not find(lines, "# Script"):
        raise TemplateExtractionError("\'# Script\' section not found")
    while True:
        try:
            line = str(next(lines))
        except StopIteration:
            raise TemplateExtractionError("No end to \'# Script\' section")
        if (line == "#~**~#"):
            break;
        else:
            templ_sections["Script"].append(line)
    if not find(lines, "# Body"):
        raise TemplateExtractionError("\'# Body\' section not found")
    while True:
        try:
            line = str(next(lines))
        except StopIteration:
            raise TemplateExtractionError("No end to \'# Body\' section")
        if (line == "#~**~#"):
            break;
        else :
            templ_sections["Body"].append(line)
    return templ_sections
#------------------------------------------------------------------------------
def extractNextContentBlock(line_iter):
    try:
        top_line = re.split("---# (.*) #---", str(next(line_iter)))
    except StopIteration:
        return '/NULL', []
    if len(top_line) != 3:
        raise ContentExtractionError(f"Invalid Block Label encountered")
    text = []
    while True:
        try:
            line = str(next(line_iter))
        except StopIteration:
            raise ContentExtractionError(f"No end to block \"{top_line[1]}\"")
        if (line == "#~**~#"):
            break;
        else :
            text.append(line)
    return top_line[1], text
#------------------------------------------------------------------------------
def extractContentSections(content_file):
    lines = filter(None, (line.rstrip() for line in content_file))
    content_sections = {
        "Item" : {
            "redirect" : "",
            "img_path" : "",
            "title"    : "",
            "desc"     : []
        },
        "Text" : {}
    }
    if not find(lines, "<!>Item-Section"):
        raise ContentExtractionError("\'<!>Item-Section\' not found")
    content_sections["Item"]["redirect"] = str(next(lines))
    content_sections["Item"]["img_path"] = str(next(lines))
    content_sections["Item"]["title"]    = str(next(lines))
    while True:
        try:
            line = str(next(lines))
        except StopIteration:
            raise ContentExtractionError("No end to \'<!>Item-Section\'")
        if (line == "#~**~#"):
            break;
        else :
            content_sections["Item"]["desc"].append(line)
    if not find(lines, "<!>Text-Section"):
        raise ContentExtractionError("\'<!>Text-Section\' not found")
    while True:
        label, text = extractNextContentBlock(lines)
        if label == '/NULL':
            break
        else:
            content_sections["Text"][label] = text
    return content_sections
#------------------------------------------------------------------------------
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# Aspects of the files manager:
#       - Provide an interface to open & close files, and extracting their data
#       - Provides a function convert from img/ path to relative path
#               - Needs the path of the image from img/
#               - Needs the path of the result file relative to "result"/
#                       - Same as the path of rule file relative to rules/
#       - Finds template files
#       - Finds content files
#       - Creates the result file
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#------------------------------------------------------------------------------
__rule_name = ''
'''name of the current rule file'''
__rulefile_path = ''
'''folder relative to `rules/`'''
open_files = []
'''list of open files'''
#------------------------------------------------------------------------------
def imagePath(file_path:str) -> str:
    '''`file_path` is relative the user input `img_path`'''
    global __rulefile_path, seperator
    i = 1
    for c in __rulefile_path:
        if (c == seperator): i += 1
    route = ''
    for _ in range(i-1):
        route += "../"
    return (route + img_path + file_path)
#------------------------------------------------------------------------------
def openRuleFile(rule_path:str):
    '''`rule_path` is relative to the user input `rules_path`'''
    global __rule_name, __rulefile_path, open_files
    __rulefile_path, __rule_name = rule_path.rsplit(seperator, 1)
    __rule_name, extension = __rule_name.rsplit('.', 1)
    open_files.append(open(rule_path,'r'))
    return open_files[-1], extractRuleSections(open_files[-1])
#------------------------------------------------------------------------------
def openTemplateFile(file_path:str):
    '''`file_path` is relative to the user input `templ_path`'''
    global open_files
    open_files.append(open(templ_path+file_path,'r'))
    return open_files[-1], extractTemplateSections(open_files[-1])
#------------------------------------------------------------------------------
def openContentFile(cont_path:str):
    global __rulefile_path, open_files
    open_files.append(open(__rulefile_path+'/'+cont_path,'r'))
    return open_files[-1], extractContentSections(open_files[-1])
#------------------------------------------------------------------------------
def openResultFile(result_path:str):
    '''Creates and opens a Result file'''
    global __rule_name, __rulefile_path, open_files
    path_to_result = result_path + __rulefile_path[9:]
    os.makedirs(path_to_result, exist_ok=True)
    open_files.append(open((path_to_result+'/'+__rule_name+'.html'),'w'))
    return open_files[-1]
#------------------------------------------------------------------------------
def closeFile(file):
    '''wrapper around close(), but used slightly differently'''
    global open_files
    try:
        idx = open_files.index(file)
        open_files[idx].close()
        open_files.remove(file)
    except:
        print("File Closure : raised exception")
    return
#-------------------------------------------------------------------------------
def closeFiles(files:list):
    '''close multiple files'''
    for file in files:
        closeFile(file)
    return
#------------------------------------------------------------------------------
def close_open_files() -> None:
    '''closes all files opened using open_file()'''
    global open_files
    for file in open_files:
        file.close()
    open_files.clear()
    return
#------------------------------------------------------------------------------