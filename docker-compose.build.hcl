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
  dockerfile = "infrastructure-packaging/Dockerfile.ChatBot"
  tags = ["${DISTRO}/virtualwife-chatbot:${TAG}"]
  platforms = ["linux/amd64", "linux/arm64"]
}

target "chatvrm" {
  dockerfile = "infrastructure-packaging/Dockerfile.ChatVRM"
  tags = ["${DISTRO}/virtualwife-chatvrm:${TAG}"]
  platforms = ["linux/amd64", "linux/arm64"]
}

target "gateway" {
  dockerfile = "infrastructure-packaging/Dockerfile.Gateway"
  tags = ["${DISTRO}/virtualwife-gateway:${TAG}"]
  platforms = ["linux/amd64", "linux/arm64"]
}