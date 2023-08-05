from sections_files import *
###############################################################################
class ContentTranslationError(BaseException):
    def __init__(self, message="") -> None:
        super().__init__(message)
###############################################################################
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# ...
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#------------------------------------------------------------------------------
def addHead(html:str, head:map, templates:list):
    html = append(html, "<head>", 1)
    html = append(html, f"<title> {head.get('title')} </title>", 0)
    html = append(html, "<meta charset=\"UTF-8\">", 0)
    html = append(html, f"<meta name=\"author\" content=\"{head.get('author')}\">", 0)
    html = append(html, "<style>", 1)
    for styles in templates:
        for style in styles:
            html = append(html, style, 0)
    html = append(html, "", -1)
    html = append(html, "</style>", -1)
    html = append(html, "</head>", 0)
    return html
#------------------------------------------------------------------------------
def addHeader(html:str, header:list):
    html = append(html, "<div class=\"header\">", 1)
    for line in header:
        html = append(html, line, 0)
    html = append(html, "", -1)
    html = append(html, "</div>", 0)
    return html
#------------------------------------------------------------------------------
def addFooter(html:str, footer:list):
    html = append(html, "<footer>", 1)
    html = append(html, "<div class=\"footer\">", 1)
    for line in footer:
        html = append(html, line, 0)
    html = append(html, "", -1)
    html = append(html, "</div>", -1)
    html = append(html, "</footer>", 0)
    return html
#------------------------------------------------------------------------------
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# ...
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#------------------------------------------------------------------------------
def addItem(html:str, data:map) -> str:
    html = append(html, "<hr width=\"70%\" align=\"center\" color=\"lightgrey\" size=\"1\">")
    html = append(html, "<div class=\"item\">", 1)
    html = append(html, (f"<a href=\"{data.get('redirect')}\">"), 1)
    html = append(html, "<span class=\"item_link\"></span>", -1)
    html = append(html, "</a>")
    html = append(html, (f"<img src=\"{imagePath(data.get('img_path'))}\"/>"))
    html = append(html, "<div class=\"item-text\">", 1)
    html = append(html, (f"<h3> {data.get('title')} </h3>"))
    html = append(html, "<p>", 1)
    for line in data.get('desc'):
        html = append(html, line)    
    html = append(html, "", -1)
    html = append(html, "</p>", -1)
    html = append(html, "</div>", -1)
    html = append(html, "</div>")
    return html
#------------------------------------------------------------------------------
def addContent(html:str, text:list) -> str:
    def imgFix(line:str) -> str:
        parts = re.split("IMG[(](.*)[)]", line, maxsplit=1)
        if len(parts) > 1:
            return (parts[0] + imagePath(parts[1]) + "\"" + parts[2])
        else:
            return parts[0]

    html = append(html, "<hr width=\"70%\" align=\"center\" color=\"lightgrey\" size=\"1\">")
    html = append(html, "<p>", 1)
    for line in text:
        line = imgFix(line)
        html = append(html, line)
    html = append(html, "", -1, new_line=False)
    html = append(html, "</p>")
    return html