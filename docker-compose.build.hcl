variable "TAG" {
  default = "latest"
}

variable "DISTRO" {
  default = "okapi0129"
}

group "default" {
  targets = ["chatbot","chatvrm","gateway"]
}

target "chatbot" {
  args = {
    TAG = null
  }
  dockerfile = "infrastructure-packaging/Dockerfile.ChatBot"
  tags = ["${DISTRO}/virtualwife-chatbot:${TAG}"]
}

target "chatvrm" {
  args = {
    TAG = null
  }
  dockerfile = "infrastructure-packaging/Dockerfile.ChatVRM"
  tags = ["${DISTRO}/virtualwife-chatvrm:${TAG}"]
}

target "gateway" {
  args = {
    TAG = null
  }
  dockerfile = "infrastructure-packaging/Dockerfile.Gateway"
  tags = ["${DISTRO}/virtualwife-gateway:${TAG}"]
}

target "chatbot-release" {
  inherits = ["chatbot"]
  platforms = ["linux/amd64", "linux/arm64"]
}

target "chatvrm-release" {
  inherits = ["chatvrm"]
  platforms = ["linux/amd64", "linux/arm64"]
}

target "gateway-release" {
  inherits = ["gateway"]
  platforms = ["linux/amd64", "linux/arm64"]
}