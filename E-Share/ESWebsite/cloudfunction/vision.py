import json
import re
import os
from google.cloud import vision
from google.cloud import vision_v1
from google.cloud import storage
from google.protobuf import json_format

bucket_names = "processedjson"
blob_name = "processed.txt"


def async_detect_document(gcs_source_uri, gcs_destination_uri):
    gcs_source_uri = 'gs://forimagea06/Registration_form.pdf'
    gcs_destination_uri = 'gs://forresulta06/pdf_resulte'
    mime_type = 'application/pdf'

    batch_size = 2

    client = vision.ImageAnnotatorClient()

    feature = vision.Feature(
        type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    gcs_source = vision.GcsSource(uri=gcs_source_uri)
    input_config = vision.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size)

    async_request = vision.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config,
        output_config=output_config)

    operation = client.async_batch_annotate_files(
        requests=[async_request])

    print('Waiting for the operation to finish.')
    operation.result(timeout=180)

    storage_client = storage.Client()

    match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)

    blob_list = list(bucket.list_blobs(
        prefix=prefix))
    print('Output files:')
    for blob in blob_list:
        print(blob.name)

    output = blob_list[0]

    json_string = output.download_as_string()
    response = json_format.Parse(
        json_string, vision_v1.types.AnnotateFileResponse()._pb)

    first_page_response = response.responses[0]
    annotation = first_page_response.full_text_annotation
    x = annotation.text
    first = x.split("\n", 15)
    second = x.split("\n")
    del first[15]
    del first[13]
    del second[:15]
    jsonList = []
    for i in range(0,14):
        jsonList.append({first[i] : second[i]})
    print(json.dumps(jsonList, indent = 1))

    words = str(jsonList).replace("{", "")
    wordss = str(words).replace("}", "")
    wordsss = str(wordss).replace("[", "{")
    wordssss = str(wordsss).replace("]", "}")
    print(wordssss)

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_names)
    blob = bucket.blob(blob_name)

    with blob.open("w") as f:
        f.write(wordssss)

    with blob.open("r") as f:
        print(f.read())
