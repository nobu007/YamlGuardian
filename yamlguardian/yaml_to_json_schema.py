import ast
import copy
import json
import os
import tempfile
from glob import glob
from pathlib import Path

import jsonref
from ruamel.yaml import YAML

from yamlguardian.save_load_json import to_json
from yamlguardian.save_load_yaml import save_yaml
from yamlguardian.yaml_json_converter import YamlJsonConverter

yaml = YAML()
converter = YamlJsonConverter()


def yaml_to_json_schema(yaml_directory, json_directory="") -> str:
    # YAML Schema を読み込んで JSON Schema に変換
    yaml_schema_dict = load_yaml_schemas(yaml_directory)
    resolved_json_schema = yaml_schema_to_json_schema(yaml_schema_dict)
    resolved_json_schema_dict = jsonref_to_dict(resolved_json_schema)
    resolved_json_schema_str = to_json(resolved_json_schema_dict)

    # JSON Schema を保存
    resolved_json_schema_path = ""
    if json_directory:
        resolved_json_schema_filename = os.path.basename(yaml_directory) + ".json"
        resolved_json_schema_path = os.path.join(json_directory, resolved_json_schema_filename)
        yaml_schema_dict_path = os.path.join(json_directory, "yaml_schema_dict.yaml")

        # 保存
        save_yaml(yaml_schema_dict, yaml_schema_dict_path)
        save_schema(resolved_json_schema_str, resolved_json_schema_path)

    print("✅ JSON Schema の統合が完了しました:", resolved_json_schema_path)
    return resolved_json_schema_str


def jsonref_to_dict(jsonref_obj: jsonref.JsonRef | list | dict | str):
    def ref_caster(o):
        """
        jsonref.JsonRef を適切な Python のデータ型 (dict, list, str, int, bool, float) に変換する。
        """
        if isinstance(o, jsonref.JsonRef):
            for json_type in [dict, list, str, int, float, bool]:
                if isinstance(o, json_type):
                    return copy.deepcopy(o)  # 安全に変換
        raise TypeError(f"Type not serializable: {type(o)}")  # 想定外の型ならエラー

    # JSON シリアライズ時に `$ref` を解決
    if isinstance(jsonref_obj, jsonref.JsonRef):
        jsonref_obj = jsonref.JsonRef.replace_refs(jsonref_obj)

    # さらにJSON シリアライズ失敗時のデフォルト動作で jsonref.JsonRef を解決
    json_str = json.dumps(jsonref_obj, default=ref_caster)
    return json.loads(json_str)  # dict に戻す


def dereference_schema(json_schema: jsonref.JsonRef):

    def custom_jsonref_jsonloader(uri, **kwargs):
        return {}

    json_ref_obj = jsonref.loads(json.dumps(json_schema), json_loader=custom_jsonref_jsonloader)
    deref_schema_str = str(json_ref_obj)
    deref_schema_dict = ast.literal_eval(deref_schema_str)
    return deref_schema_dict


def yaml_schema_to_json_schema(yaml_schema_dict):
    # YAML Schema を JSON Schema に変換
    merged_json_schema = merge_yaml_schemas(yaml_schema_dict)
    resolved_json_schema = resolve_merged_json_schema(merged_json_schema)
    return resolved_json_schema


def merge_yaml_schemas(yaml_schema_dict):
    """複数の JSON Schema を統合 ($defs に登録)"""
    merged_json_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {},
        "$defs": {},
    }

    # 参照を$defsに登録
    for schema_name, yaml_schema in yaml_schema_dict.items():
        merged_json_schema["$defs"][schema_name] = converter.yaml_to_json(yaml_schema)
        merged_json_schema["properties"][schema_name] = {"$ref": f"#/$defs/{schema_name}"}

    return merged_json_schema


def resolve_merged_json_schema(merged_json_schema) -> jsonref.JsonRef:
    """参照を解決 (JSON Schema に変換)"""

    # 保存
    merged_json_schema_path = save_schema(merged_json_schema)

    # 参照を解決
    resolved_json_schema = None

    with open(merged_json_schema_path, "r", encoding="utf-8") as f:
        resolved_json_schema = jsonref.load(f)

    return resolved_json_schema


def load_yaml_schemas(directory):
    """ディレクトリ内の YAML ファイルを読み込む"""
    yaml_schema_dict = {}

    for file_path in glob(os.path.join(directory, "**/*.yaml"), recursive=True):
        schema_name = os.path.splitext(os.path.basename(file_path))[0]

        with open(file_path, "r", encoding="utf-8") as f:
            yaml_schema = yaml.load(f)
            yaml_schema_dict[schema_name] = yaml_schema

    return yaml_schema_dict


def save_schema(schema_str: str, output_path="") -> str:
    if output_path:
        prepare_dir(output_path)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(schema_str, f, indent=2, ensure_ascii=False)
    else:
        # save to temporary file
        tmp_ext = os.path.splitext(output_path)[1]
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=tmp_ext) as f:
            json.dump(schema_str, f, indent=2, ensure_ascii=False)
            output_path = f.name
    return output_path


def prepare_dir(output_file_path):
    directory = os.path.dirname(output_file_path)
    os.makedirs(directory, exist_ok=True)


def to_str_schema(schema_dict):
    return json.dumps(schema_dict, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    yaml_directory_ = "./rule_config"  # YAML ファイルの格納ディレクトリ
    yaml_to_json_schema(yaml_directory_, "outputs")
