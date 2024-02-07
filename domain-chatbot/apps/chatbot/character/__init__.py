import os

from .role_package_manage import RolePackageManage, RoleDialogueExample

root_path = os.getcwd()
args = {
    "embed_model_path": root_path + "/models/baai/bge-large-zh-v1.5",
    "reranker_model_path": root_path + "/models/baai/bge-reranker-large",
}

role_package_manage = RolePackageManage()
role_dialogue_example = RoleDialogueExample(args)
