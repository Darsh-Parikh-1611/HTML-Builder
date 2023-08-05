import platform
import re
###############################################################################
result_path = ''
rules_path  = ''
templ_path  = ''
img_path    = ''

if platform.system() == 'Windows':
    seperator = '\\'
else:
    seperator = '/'
###############################################################################
__tab_depth = 0

def append(html:str, html_line:str, tab_change:int=0, new_line:bool=True) -> str:
    '''
    Offsets `html_line` by a certain number of tabs.\n
    Returns the concatenation of `html_container` and the modified `html_line`
    
    `tab_change` indicates how many tab depths to add / remove
    '''
    global __tab_depth
    ret_str = html
    if html_line != "":
        ret_str += ('\t' * __tab_depth) + html_line
    if new_line == True:
        ret_str += '\n'
    __tab_depth += tab_change
    return ret_str
#------------------------------------------------------------------------------
def find(iteratable, string : str) -> bool :
    '''
    Iterates using the `iterable` (a file iterator), until `string` is found.
    Returns True if found. Otherwise it returns False. \n
    **Moves the iterator in the process**
    '''
    while True:
        try:
            if next(iteratable) == string:
                return True
        except StopIteration:
            return False    # reached end of iterator