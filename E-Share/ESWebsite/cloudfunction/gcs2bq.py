def gcs2bq(event, context):
    event = "1"
    context = "2"
    from google.cloud import bigquery
    client = bigquery.Client()
    table_id = "peterproject-364114.regdata.regdata"

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("StudentName", "STRING"),
            bigquery.SchemaField("DateOfBirth", "STRING"),
            bigquery.SchemaField("Age", "INTEGER"),
            bigquery.SchemaField("StudentID", "INTEGER"),
            bigquery.SchemaField("EmailAddress", "STRING"),
            bigquery.SchemaField("PhoneNumber", "INTEGER"),
            bigquery.SchemaField("HomeAddress", "STRING"),
            bigquery.SchemaField("NameOSchool", "STRING"),
            bigquery.SchemaField("SchoolAddress", "STRING"),
            bigquery.SchemaField("NameOTeacher", "STRING"),
            bigquery.SchemaField("PhoneOfTeacher", "INTEGER"),
            bigquery.SchemaField("EmailOfTeacher", "STRING"),
            bigquery.SchemaField("NameOfParent", "STRING"),
            bigquery.SchemaField("ParentPhoneNumber", "INTEGER")
        ],
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    )
    uri = "gs://processedjson/processed.txt"

    load_job = client.load_table_from_uri(
        uri,
        table_id,
        location="US",
        job_config=job_config,
    )

    load_job.result()

    destination_table = client.get_table(table_id)
    print("Loaded {} rows.".format(destination_table.num_rows))
