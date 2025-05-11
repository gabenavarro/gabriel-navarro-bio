'''
Insertion of Javscript library Prism.js into FastHTML
https://prismjs.com/
'''
from fasthtml.common import Script

def PrismJS(sel: str = ".prism"):
    """Implements browser-based Prism.js library for syntax highlighting."""
    src = """
import { Prism } from "https://cdn.jsdelivr.net/npm/prismjs@1.30.0/prism.min.js";
proc_htmx('%s', e => Prism.highlightElement(e));
    """ % sel
    return Script(src, type='module')