'''
Insertion of Javascript library MiniMasonry into FastHTML
https://spope.github.io/MiniMasonry.js/
'''

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
    // Create Masonry instance and store it globally so we can access it from the filter function
    const msnry = new Masonry(element, {{
        {options_str}
    }});
    
    // Store the masonry instance on the element for easy access
    element.msnry = msnry;

    // Set up a ResizeObserver to watch for size changes in items
    const resizeObserver = new ResizeObserver(entries => {{
        // When any observed element changes size, re-layout
        msnry.layout();
    }});
    
    // Observe all current masonry items
    const items = element.querySelectorAll('{item_selector}');
    items.forEach(item => resizeObserver.observe(item));
    
   
    // Store the observers on the element to prevent memory leaks
    element._masonryObservers = {{
        resize: resizeObserver,
    }};

    msnry.layout();
}}

// Function to filter cards based on selected chips with Masonry integration
function filterCards() {{
    // Get all selected filters
    const selectedFilters = Array.from(document.querySelectorAll('.chip.selected'))
        .map(chip => chip.dataset.filter);
    
    // Show all cards if no filters are selected
    const showAll = selectedFilters.length === 0;
    
    // Get the container with Masonry
    const container = document.querySelector('.card-container');
    
    // Show/hide cards based on filters
    const cards = document.querySelectorAll('.card');
    let hasVisibilityChanges = false;
    
    cards.forEach(card => {{
        // Get all categories for this card (split by comma)
        const cardCategories = card.dataset.category.split(',');
        
        // Check if any of the card's categories match any selected filter
        const hasMatchingCategory = cardCategories.some(category => 
            selectedFilters.includes(category)
        );
        
        // Check if visibility would change
        const isCurrentlyHidden = card.classList.contains('hidden');
        const shouldBeHidden = !(showAll || hasMatchingCategory);
        
        if (isCurrentlyHidden !== shouldBeHidden) {{
            hasVisibilityChanges = true;
        }}
        
        if (showAll || hasMatchingCategory) {{
            card.classList.remove('hidden');
        }} else {{
            card.classList.add('hidden');
        }}
    }});
}}

document.addEventListener('DOMContentLoaded', () => {{
    proc_htmx('{sel}', initMasonry);
    proc_htmx(filterCards);
}});
"""
    # print(src) <== Good for debugging
    return Script(src, type='module')
