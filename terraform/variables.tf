variable "cluster_name" {
  type = string
  default = "virginia-cluster"
}

variable "master_role" {
  type = string
  default = "control-plane"
}

variable "worker_role" {
  type = string
  default = "worker"
}
