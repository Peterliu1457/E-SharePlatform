from google.api_core.client_options import ClientOptions
from google.cloud import documentai
from typing import Sequence

project_id = 'peterproject-364114'
location = 'us'
processor_id = 'dbe1f8720871be2a'
file_path = 'Registration_form.pdf'
mime_type = 'application/pdf'


def quickstart1(data, context):
    data = '1'
    context = '1'


def quickstart(
        project_id: str, location: str, processor_id: str, file_path: str, mime_type: str
):
    opts = ClientOptions(api_endpoint=f"us-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)

    document = result.document

    print("The document contains the following text:")
    print(document.text)


def process_document_form_sample(
        project_id: str, location: str, processor_id: str, file_path: str, mime_type: str
):
    document = process_document(
        project_id, location, processor_id, file_path, mime_type
    )

    text = document.text
    print(f"Full document text: {repr(text)}\n")
    print(f"There are {len(document.pages)} page(s) in this document.")

    for page in document.pages:
        print(f"\n\n**** Page {page.page_number} ****")

        print(f"\nFound {len(page.tables)} table(s):")
        for table in page.tables:
            num_collumns = len(table.header_rows[0].cells)
            num_rows = len(table.body_rows)
            print(f"Table with {num_collumns} columns and {num_rows} rows:")

            print("Columns:")
            print_table_rows(table.header_rows, text)

            print("Table body data:")
            print_table_rows(table.body_rows, text)

        print(f"\nFound {len(page.form_fields)} form field(s):")
        for field in page.form_fields:
            name = layout_to_text(field.field_name, text)
            value = layout_to_text(field.field_value, text)
            print(f"    * {repr(name.strip())}: {repr(value.strip())}")


def process_document(
        project_id: str, location: str, processor_id: str, file_path: str, mime_type: str
) -> documentai.Document:
    opts = ClientOptions(api_endpoint=f"us-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)

    return result.document


def print_table_rows(
        table_rows: Sequence[documentai.Document.Page.Table.TableRow], text: str
) -> None:
    for table_row in table_rows:
        row_text = ""
        for cell in table_row.cells:
            cell_text = layout_to_text(cell.layout, text)
            row_text += f"{repr(cell_text.strip())} | "
        print(row_text)


def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
    """
    Document AI identifies text in different parts of the document by their
    offsets in the entirety of the document's text. This function converts
    offsets to a string.
    """
    response = ""
    for segment in layout.text_anchor.text_segments:
        start_index = int(segment.start_index)
        end_index = int(segment.end_index)
        response += text[start_index:end_index]
    return response
