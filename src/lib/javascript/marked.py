'''
Insertion of Javscript library Marked.Js into FastHTML
https://marked.js.org/
'''
from fasthtml.common import Script, Link


highlight_css = "https://cdn.jsdelivr.net/gh/PrismJS/prism@1.30.0/themes/prism-tomorrow.min.css"
highlight_link = Link(rel="stylesheet", href=highlight_css)

def MarkedJS(sel: str = ".marked"):
    """Implements browser-based Marked.js library for Markdown parsing."""
    src = """
import * as marked from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";
import * as prismjs from "https://cdn.jsdelivr.net/npm/prismjs@1.30.0/prism.min.js";
import * as bash from "https://cdn.jsdelivr.net/npm/prismjs@1.30.0/components/prism-bash.min.js";
import * as python from "https://cdn.jsdelivr.net/npm/prismjs@1.30.0/components/prism-python.min.js";
import * as dockerfile from "https://cdn.jsdelivr.net/npm/prismjs@1.30.0/components/prism-docker.min.js";
import * as yaml from "https://cdn.jsdelivr.net/npm/prismjs@1.30.0/components/prism-yaml.min.js";
import * as json from "https://cdn.jsdelivr.net/npm/prismjs@1.30.0/components/prism-json.min.js";
import * as typescript from "https://cdn.jsdelivr.net/npm/prismjs@1.30.0/components/prism-typescript.min.js";

marked.setOptions({
  highlight: function(code, lang) {
    if (prism.languages[lang]) {
      return prism.highlight(code, prism.languages[lang], lang);
    } else {
      return code;
    }
  }
});

proc_htmx('%s', e => e.innerHTML = marked.parse(e.textContent));
    """ % sel
    return (Script(src, type='module'), highlight_link)


# marked.setOptions({
#   highlight: function(code, lang) {
#     if (prism.languages[lang]) {
#       return prism.highlight(code, prism.languages[lang], lang);
#     } else {
#       return code;
#     }
#   }
# });
# https://cdnjs.cloudflare.com/ajax/libs/prism/1.30.0/components/prism-bash.min.js