import fitz

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    title = ""
    headings = []
    font_sizes = []
    all_text = []  # Collect all text for summarization

    # Pass 1: Collect font sizes & text
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                text = "".join(span["text"] for span in line["spans"]).strip()
                if not text or len(text) < 3:  
                    continue
                size = max(span["size"] for span in line["spans"])
                font_sizes.append(size)
                all_text.append(text)

    max_size = max(font_sizes) if font_sizes else 12
    h1_size = max_size
    h2_size = max_size * 0.8
    h3_size = max_size * 0.7

    # Pass 2: Extract headings
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                text = "".join(span["text"] for span in line["spans"]).strip()
                if not text or len(text) < 3:
                    continue
                size = max(span["size"] for span in line["spans"])

                if not title and page_num == 1 and size >= h1_size:
                    title = text
                    continue

                if size >= h1_size * 0.95:
                    level = "H1"
                elif size >= h2_size:
                    level = "H2"
                elif size >= h3_size:
                    level = "H3"
                else:
                    continue
                headings.append({"level": level, "text": text, "page": page_num})

    # --- Simple summarization ---
    summary = " ".join(all_text[:10])  # Take first 10 lines as a basic summary
    if len(summary) > 800:  # Limit summary length
        summary = summary[:800] + "..."

    return {
        "title": title if title else "Untitled Document",
        "summary": summary if summary else "No summary available.",
        "outline": headings
    }
