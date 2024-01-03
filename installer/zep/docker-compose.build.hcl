variable "TAG" {
  default = "v1.0.0"
}

variable "DISTRO" {
  default = "okapi0129"
}

group "default" {
  targets = ["postgres","zep","zep-nlp-server"]
}

target "postgres" {
  args = {
    TAG = null
  }
  dockerfile = "Dockerfile.postgres"
  tags = ["${DISTRO}/getzep-postgres:${TAG}"]
}

target "zep" {
  args = {
    TAG = null
  }
  dockerfile = "Dockerfile.zep"
  tags = ["${DISTRO}/getzep-zep:${TAG}"]
}

target "zep-nlp-server" {
  args = {
    TAG = null
  }
  dockerfile = "Dockerfile.zep-nlp-server"
  tags = ["${DISTRO}/getzep-zep-nlp-server:${TAG}"]
}

target "postgres-release" {
  inherits = ["postgres"]
  platforms = ["linux/amd64", "linux/arm64"]
}

target "zep-release" {
  inherits = ["zep"]
  platforms = ["linux/amd64", "linux/arm64"]
}

target "zep-nlp-server-release" {
  inherits = ["zep-nlp-server"]
  platforms = ["linux/amd64", "linux/arm64"]
}