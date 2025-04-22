'''
Insertion of Javscript library Marked.Js into FastHTML
https://marked.js.org/
'''
from fasthtml.common import Script

def MarkedJS(sel: str = ".marked"):
    """Implements browser-based Marked.js library for Markdown parsing."""
    src = """
import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";
proc_htmx('%s', e => e.innerHTML = marked.parse(e.textContent));
    """ % sel
    return Script(src, type='module')