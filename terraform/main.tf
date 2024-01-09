terraform {
  required_providers {
    kind = {
      source = "tehcyx/kind"
      version = "~> 0.2.1"
    }
  }
}

provider "kind" {}

resource "kind_cluster" "default" {
  name = var.cluster_name

  kind_config {
    kind = "Cluster"
    api_version = "kind.x-k8s.io/v1alpha4"

    node {
      role = var.master_role
    }
    node {
      role = var.worker_role
    }

    node {
      role = var.worker_role
    }
  }
}
