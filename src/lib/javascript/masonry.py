from fasthtml.common import Script

def MasonryJS(
        sel: str = '.masonry-grid',
        item_selector: str = '.masonry-item',
        gutter: int = 10,
        column_width: str | int = '.masonry-sizer',
        percent_position: bool = True,
        horizontal_order: bool = False,
        origin_left: bool = True,
        origin_top: bool = True
    ):
    """
    Implements browser-based Masonry layout library.
    
    ### Args:
        - sel: CSS selector for masonry grid container
        - item_selector: CSS selector for grid items
        - gutter: Gutter between items (in pixels)
        - column_width: Width of columns (can be a selector string or number)
        - percent_position: Set item positions in percent values instead of pixels
        - horizontal_order: Lay out items to maintain horizontal order
        - origin_left: Set positioning from left to right (false for right to left)
        - origin_top: Set positioning from top to bottom (false for bottom to top)
    
    # Returns:
        Script element with Masonry initialization
    """
    options = {
        'itemSelector': f"'{item_selector}'",
        'gutter': gutter,
        'percentPosition': str(percent_position).lower(),
        'horizontalOrder': str(horizontal_order).lower(),
        'originLeft': str(origin_left).lower(),
        'originTop': str(origin_top).lower()

    }
    
    # Handle column_width which can be a selector string or a number
    if isinstance(column_width, str) and column_width.startswith('.'):
        options['columnWidth'] = f"'{column_width}'"
    else:
        options['columnWidth'] = column_width
        
    options_str = ', '.join([f'{k}: {v}' for k, v in options.items()])
    
    src = f"""
import Masonry from 'https://cdn.jsdelivr.net/npm/masonry-layout@4/+esm';

function initMasonry(element) {{
    // Create Masonry instance and store it
    const msnry = new Masonry(element, {{
        {options_str}
    }});

    // Set up a ResizeObserver to watch for size changes in items
    const resizeObserver = new ResizeObserver(entries => {{
        // When any observed element changes size, re-layout
        msnry.layout();
    }});
    
    // Observe all current masonry items
    const items = element.querySelectorAll('{item_selector}');
    items.forEach(item => resizeObserver.observe(item));
    
    // Set up a MutationObserver to watch for new masonry items
    const mutationObserver = new MutationObserver(mutations => {{
        let needsUpdate = false;
        
        mutations.forEach(mutation => {{
            if (mutation.type === 'childList') {{
                // New nodes added
                if (mutation.addedNodes.length) {{
                    mutation.addedNodes.forEach(node => {{
                        if (node.nodeType === 1) {{ // Element node
                            if (node.matches('{item_selector}')) {{
                                resizeObserver.observe(node);
                                needsUpdate = true;
                            }} else {{
                                // Check for masonry items inside the added node
                                const nestedItems = node.querySelectorAll('{item_selector}');
                                if (nestedItems.length) {{
                                    nestedItems.forEach(item => resizeObserver.observe(item));
                                    needsUpdate = true;
                                }}
                            }}
                        }}
                    }});
                }}
                
                // Nodes removed
                if (mutation.removedNodes.length) {{
                    needsUpdate = true;
                }}
            }}
        }});
        
        if (needsUpdate) {{
            // Delay layout to allow browser to render new content
            setTimeout(() => msnry.layout(), 10);
        }}
    }});
    
    // Start observing the container for added/removed items
    mutationObserver.observe(element, {{ childList: true, subtree: true }});
    
    // Store the observers on the element to prevent memory leaks
    element._masonryObservers = {{
        resize: resizeObserver,
        mutation: mutationObserver
    }};
}}

proc_htmx('{sel}', initMasonry);
"""    
    # print(src) <== Good for debugging
    return Script(src, type='module')
