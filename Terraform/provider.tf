terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}
provider "google" {
  project = "peterproject-364114"
  region  = "us-central1"
  zone    = "us-central1-c"
  #credentials = "keys.json"
}