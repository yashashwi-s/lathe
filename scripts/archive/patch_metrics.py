import sys

def filter_page_numbers(blocks, page_height):
    filtered = []
    for b in blocks:
        # Check if block is at the bottom 15% of the page
        if b["bbox"][1] > page_height * 0.85:
            text = ""
            for l in b.get("lines", []):
                for s in l.get("spans", []):
                    text += s.get("text", "").strip()
            if text.isdigit():
                continue # Skip page numbers
        filtered.append(b)
    return filtered
