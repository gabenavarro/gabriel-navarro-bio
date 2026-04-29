"""Reset horizontal scroll on BFCache restore.

Edge's BFCache (and Safari's) restores scroll position on
back-navigation. If the page was *briefly* horizontally scrolled at any
point — for instance during the trackpad swipe-back gesture itself — the
browser may restore the page with `scrollX > 0`, leaving the entire layout
shifted right and the navbar nav-links cut off the right edge.

`html { overflow-x: clip }` in `_base.py` already prevents NEW horizontal
scroll. This handler clears any scrollX value the browser tries to restore
on `pageshow` events with `event.persisted === true` (BFCache restore), as
a defense-in-depth belt-and-braces.
"""

from fasthtml.common import Script

BFCACHE_SCROLL_RESET_JS = Script("""
window.addEventListener('pageshow', function (event) {
    if (event.persisted && window.scrollX !== 0) {
        window.scrollTo(0, window.scrollY);
    }
});
""")
