# Terraform Configuration for Enterprise ADK Infrastructure
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {
  type        = string
  description = "Google Cloud Platform Project ID"
}

variable "region" {
  type        = string
  default     = "us-east1"
  description = "Primary GCP Region for Deployment"
}

# GCS Bucket for Agent Traces, Logs, and File Artifacts
resource "google_storage_bucket" "agent_logs_bucket" {
  name                        = "${var.project_id}-agent-artifacts"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  # Purge trace files older than 30 days
    }
  }
}

output "logs_bucket_name" {
  value       = google_storage_bucket.agent_logs_bucket.name
  description = "Name of the created GCS bucket for log storage"
}
