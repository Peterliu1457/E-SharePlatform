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

resource "google_cloudfunctions_function" "gcs2bq" {
  name = "gcs2bq"
  runtime = "python310"
  description = "gcs2bq"

  available_memory_mb = 256
  source_archive_bucket = google_storage_bucket.upload.name
  source_archive_object = google_storage_bucket_object.gcs2bq.name
  event_trigger {
    event_type = "google.storage.object.finalize"
    resource     = google_storage_bucket.processed_bucket.name
  }

  entry_point = "gcs2bq"
}

resource "google_cloudfunctions_function" "vision" {
  name = "vision"
  runtime = "python310"
  description = "visionning"

  available_memory_mb = 256
  source_archive_bucket = google_storage_bucket.upload.name
  source_archive_object = google_storage_bucket_object.vision.name

  event_trigger {
    event_type = "google.storage.object.finalize"
    resource     = google_storage_bucket.image_bucket.name
  }
  entry_point = "async_detect_document"
}