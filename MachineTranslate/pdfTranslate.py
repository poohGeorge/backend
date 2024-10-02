import fitz
from . import textTranslate

def normalize_color(color):
    """Normalize the color components from 0-255 range to 0-1 range."""
    if isinstance(color, (tuple, list)):  # Check if color is a list or tuple
        if len(color) == 3:  # RGB
            return [c / 255 for c in color]
        elif len(color) == 4:  # RGBA
            return [c / 255 for c in color[:3]]  # Ignore alpha for text
        else:
            raise ValueError("Unsupported color format: must be RGB or RGBA")
    elif isinstance(color, int):  # Handle integer color value
        return [color / 255]  # Normalize the integer color to a single component
    else:
        raise ValueError("Unsupported color format")

def translate_pdf(input_pdf_path, source_lang, target_lang):
    # Open the original PDF
    pdf_document = fitz.open(input_pdf_path)
    output_pdf_path = "translated_pdf.pdf"
    # Set to track already translated texts
    translated_texts = set()

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)

        # Get all text boxes (regions of text)
        text_instances = page.get_text("dict")  # Extract text as a dictionary

        # Iterate through the text instances to get text and their coordinates
        for block in text_instances["blocks"]:
            if "lines" in block:  # Check if it's a text block
                for line in block["lines"]:
                    # Join the spans in the line to form the complete text
                    original_text = "".join(span["text"] for span in line["spans"]).strip()

                    if original_text and original_text not in translated_texts:  # Check if there's text to translate and not already translated
                        # Translate the text
                        translated_text = textTranslate.translate_text(original_text, source_lang, target_lang)

                        # Store the translated text to avoid re-translation
                        translated_texts.add(original_text)

                        # Get the bounding box (coordinates) of the text to be replaced
                        rects = page.search_for(original_text)

                        # Overwrite original text with the translated text
                        for rect in rects:
                            # Get font size and color from the original text
                            font_size =  12
                            font_color = (0, 0, 0)  # Default to black
                            print("normalized_color", font_color)
                            # Normalize the font color
                            normalized_color = normalize_color(font_color)

                            # Ensure we have 1 or 3 components after normalization
                            if len(normalized_color) == 1:
                                normalized_color = [normalized_color[0]]  # Grayscale
                            elif len(normalized_color) == 3:
                                normalized_color = normalized_color  # RGB
                            elif len(normalized_color) == 4:
                                normalized_color = normalized_color  # RGB

                            # First, redact the original text by placing a white box over it
                            page.add_redact_annot(rect, fill=[1.0, 1.0, 1.0])  # White color
                            page.apply_redactions()
                            
                            # Insert the translated text at the same position
                            page.insert_text((rect.x0, rect.y0), translated_text, fontsize=font_size, color=normalized_color)

    # Save the modified PDF with translated text
    pdf_document.save(output_pdf_path)
    pdf_document.close()
