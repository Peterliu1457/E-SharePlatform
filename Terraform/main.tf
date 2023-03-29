resource "google_storage_bucket" "upload" {
    name = "foruploada06"
    location = "us-central1"
}

resource "google_storage_bucket" "give_result" {
    name = "forresulta06"
    location = "us-central1"
}

resource "google_storage_bucket" "image_bucket" {
    name = "forimagea06"
    location = "us-central1"
}

resource "google_storage_bucket" "processed_bucket" {
    name = "processedjson"
    location = "us-central1"
}

resource "google_storage_bucket_object" "gcs2bq" {
    name = "gcs2bq"
    bucket = google_storage_bucket.upload.name
    source = "gcs2bq.zip"
}

resource "google_storage_bucket_object" "vision" {
    name = "vision"
    bucket = google_storage_bucket.upload.name
    source = "vision.zip"
}


  event_trigger {
    event_type = "google.storage.object.finalize"
    resource     = google_storage_bucket.image_bucket.name
  }
  entry_point = "async_detect_document"
}
