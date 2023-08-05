from writer_translater import *
import documentation
import sys
###############################################################################
class PageConstructionError(BaseException):
    def __init__(self, message="") -> None:
        super().__init__(message)
###############################################################################
def constructPage(rule_file:str) -> str:
    try:
        r, rules  = openRuleFile(rule_file)
        h, header = openTemplateFile(rules.get('Templates').get('header'))
        b, body   = openTemplateFile(rules.get('Templates').get('body'))
        f, footer = openTemplateFile(rules.get('Templates').get('footer'))
    except FileNotFoundError as e:
        close_open_files()
        raise PageConstructionError(str(e))
    except RuleExtractionError as e:
        close_open_files()
        raise PageConstructionError(str(e))
    except TemplateExtractionError as e:
        close_open_files()
        raise PageConstructionError(str(e))
    scripts = [header.get('Script'), body.get('Script'), footer.get('Script')]

    html = "<!DOCTYPE html>\n<html lang=\"en\">\n"
    html = addHead(html, rules.get('Head'), scripts)
    html = append(html, "<body>", 1)
    html = addHeader(html, header.get('Body'))
    html = append(html, "<div class=\"main\">")
    html = append(html, f"<h1> {rules.get('Title')} </h1>")
    html = append(html, "<hr width=\"100%\" align=\"center\" color=\"black\" size=\"1\">")
    
    for rule in rules.get('Data'):
        c = ''
        try:
            instruction = rule.split(' ')
            c, content = openContentFile(instruction[1])
        except FileNotFoundError as e:
            print(str(e))
        except ContentExtractionError as e:
            print(f"Problem with content file ({instruction[0]}) : {str(e)}")
        except:
            print(f"Something wrong with the following rule: '{rule}'")
        else:
            if (instruction[0] == "item"):
                html = addItem(html, content.get('Item'))
            elif (instruction[0] == "text"):
                if len(instruction) != 3:
                    print(f"Invalid Syntax in rule: '{rule}'")
                else:
                    try:
                        html = addContent(html, content.get('Text').get(instruction[2]))
                    except:
                        print(f"No label marked as '{instruction[2]}' in content file '{instruction[1]}'")
            else:
                print(f"Invalid content command '{instruction[0]}'")
        finally:
            closeFile(c)
    
    html = append(html, "</div>", -1)
    html = append(html, "</body>")
    html = addFooter(html, footer.get('Body'))
    html = append(html, "</html>")
    closeFiles([r, h, b, f])
    return html
#------------------------------------------------------------------------------
def constructFolder(dir_objs, output_folder:str):
    for obj in dir_objs:
        if obj.is_file() and obj.name[-4:] == "rule":
            try:
                html = constructPage(obj.path)
            except PageConstructionError as e:
                print(str(e))
            else:
                res = openResultFile(output_folder)
                res.write(html)
                closeFile(res)
        elif obj.is_dir():
            constructFolder(os.scandir(obj.path), output_folder=output_folder)
#------------------------------------------------------------------------------
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
if len(sys.argv) == 5:
    Config.result_path = sys.argv[1]
    Config.rules_path  = sys.argv[2]
    Config.templ_path  = sys.argv[3]
    Config.img_path    = sys.argv[4]
else:
    print("Error : Invalid Program Usage")
    documentation.showUsage()
    exit(-1)

try:
    rules = os.scandir(Config.rules_path)
    os.scandir(Config.templ_path)
    os.scandir(Config.img_path)
except OSError as e:
    print(str(e))
else:
    constructFolder(rules, Config.result_path)