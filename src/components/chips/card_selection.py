from typing import List, Tuple
from fasthtml.common import Div, Button, Style, Script
from src.lib.css import CHIPS_CSS


def get_chip_javascript(card_selector: str):
    return (
        """
document.addEventListener('DOMContentLoaded', () => {
    // Get all the chips and cards
    const chips = document.querySelectorAll('.chip');
    const cards = document.querySelectorAll('."""
        + card_selector
        + """');

    // Check URL for tag parameters and select chips accordingly
    function applyUrlFilters() {
        const urlParams = new URLSearchParams(window.location.search);
        const tagParam = urlParams.get('tag');

        if (tagParam) {
            // Find chips that match the tag parameter
            chips.forEach(chip => {
                if (chip.dataset.filter === tagParam) {
                    chip.classList.add('selected');
                }
            });

            // Apply filtering based on selected chips
            showHideCards();
        }
    }

    // Add click event listeners to all chips
    chips.forEach(chip => {
        chip.addEventListener('click', function() {
            // Toggle the selected state
            if (this.classList.contains('selected')) {
                this.classList.remove('selected');
            } else {
                this.classList.add('selected');
            }

            // Apply filters to cards
            showHideCards();
        });
    });

    // Function to filter cards based on selected chips
    function showHideCards() {
        // Get all selected filters
        const selectedFilters = Array.from(document.querySelectorAll('.chip.selected'))
            .map(chip => chip.dataset.filter);

        // Show all cards if no filters are selected
        const showAll = selectedFilters.length === 0;

        // Show/hide cards based on filters
        cards.forEach(card => {
            // Get all categories for this card (split by comma)
            const cardCategories = card.dataset.category.split(',');

            // Check if any of the card's categories match any selected filter
            const hasMatchingCategory = cardCategories.some(category =>
                selectedFilters.includes(category)
            );

            if (showAll || hasMatchingCategory) {
                card.classList.remove('hidden');
            } else {
                card.classList.add('hidden');
            }
        });
    }

    // Apply URL filters when the page loads
    applyUrlFilters();
});
"""
    )


def filter_chips(chips: List[Tuple[str, str, str, bool]]) -> Div:
    chip_list = [
        Button(
            name,
            cls=f"chip {color} selected" if selected else f"chip {color}",
            data_filter=data,
        )
        for name, color, data, selected in chips
    ]
    return Div(
        Style(CHIPS_CSS),
        Script(get_chip_javascript("masonry-card")),
        *chip_list,
        cls="chip-container",
    )
