import PyPDF2

def add_metadata(file, output_path, metadata):
    """Creates a new pdf by copying the contents of the supplied pdf and adding the supplied PDF standard metadata.

    Args:
        file (str): A file path representing the inputpdf file for which to add metadata
        output_path (str): A file path representing the location to output the new pdf with metadata
        metadata (dict[str, str]): A dictionary of key/value pairs representing the metadata to add to the pdf. Keys must follow the PDF standard.
    """
    try:
        with open(file, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_writer = PyPDF2.PdfWriter()

            # Update metadata in the new PDF writer
            pdf_writer.add_metadata(metadata)

            # Copy all pages from the original PDF to the new PDF writer
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

            # Create complete set with the new metadata
            with open(output_path, "wb") as output_pdf:
                pdf_writer.write(output_pdf)

        print("Complete set with metadata created.")

    except FileNotFoundError:
        print(f"File not found: {file}")


def split_score_by_bookmarks(score_pdf, part_names, metadata, output_directory):
    """Splits the given pdf score by its bookmarks that correlate to the given part names. The generated parts will include the given metadata and be stored at the given output location.

    Args:
        score_pdf (str): A file path representing the pdf of the score to be split into parts. Must contain bookmarks (outlines).
        part_names (list[str]): A list of part names that correlate with the given bookmarks. The number of bookmarks and parts must match.
        metadata (dict[str,str]): A dictionary of key/value pairs representing the metadata to add to the pdf. Keys must follow the PDF standard.
        output_directory (str): A file path representing the output directory location to store the newly created files.
    """
    try:
        with open(score_pdf, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            # metadata = pdf_reader.metadata
            bookmarks = pdf_reader.outline[1]
            if len(bookmarks) < len(part_names):
                print(
                    f"Not enough bookmarks ({len(bookmarks)}) found in the document for the supplied part names ({len(part_names)})"
                )
                return

            # Loop through each bookmarked section
            for i in range(len(bookmarks)):
                # for i in range(len(pdf_reader.pages)):
                print(f"Creating part {part_names[i]}")
                page_num_current_bookmark = pdf_reader.get_destination_page_number(
                    bookmarks[i]
                )
                if i == len(bookmarks) - 1:  # Last bookmark
                    page_num_next_bookmark = len(pdf_reader.pages)  # To end of pdf
                else:
                    page_num_next_bookmark = pdf_reader.get_destination_page_number(
                        bookmarks[i + 1]
                    )

                # Create a new PDF with just the bookmarked section
                pdf_writer = PyPDF2.PdfWriter()
                for j in range(page_num_next_bookmark - page_num_current_bookmark):
                    pdf_writer.add_page(pdf_reader.pages[page_num_current_bookmark + j])

                new_metadata = metadata.copy()

                new_metadata["/Tags"] = f"{part_names[i]}"
                pdf_writer.add_metadata(new_metadata)
                output_file_path = (
                    f"{output_directory}/{metadata['/Title']} - {part_names[i]}.pdf"
                )

                with open(output_file_path, "wb") as output_pdf:
                    pdf_writer.write(output_pdf)

                print(f"Extracted part '{part_names[i]}' to '{output_file_path}'.")

    except FileNotFoundError:
        print(f"File not found: {score_pdf}")
