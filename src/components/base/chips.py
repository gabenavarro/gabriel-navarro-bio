from typing import List, Tuple
from fasthtml.common import Div, Button, Style, Script
from src.styles import CHIPS_CSS

def get_chip_javascript(card_selector: str):
    return (
        """
document.addEventListener('DOMContentLoaded', () => {
    const chips = document.querySelectorAll('.chip');
    const cards = document.querySelectorAll('."""
        + card_selector
        + """');

    function applyUrlFilters() {
        const urlParams = new URLSearchParams(window.location.search);
        const tagParam = urlParams.get('tag');

        if (tagParam) {
            chips.forEach(chip => {
                if (chip.dataset.filter === tagParam) {
                    chip.classList.add('selected');
                }
            });
            showHideCards();
        }
    }

    chips.forEach(chip => {
        chip.addEventListener('click', function() {
            if (this.classList.contains('selected')) {
                this.classList.remove('selected');
            } else {
                this.classList.add('selected');
            }
            showHideCards();
        });
    });

    function showHideCards() {
        const selectedFilters = Array.from(document.querySelectorAll('.chip.selected'))
            .map(chip => chip.dataset.filter);

        const showAll = selectedFilters.length === 0;

        cards.forEach(card => {
            const cardCategories = card.dataset.category.split(',');
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
        # Assuming masonry-card is the default selector for now, can be made parameterizable if needed
        Script(get_chip_javascript("masonry-card")),
        *chip_list,
        cls="chip-container",
    )
