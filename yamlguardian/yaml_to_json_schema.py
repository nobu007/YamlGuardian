from pathlib import Path
import os
import json
from glob import glob
from ruamel.yaml import YAML
from yamlguardian.yaml_json_converter import YamlJsonConverter
import jsonref
import tempfile

yaml = YAML()
converter = YamlJsonConverter()


def yaml_to_json_schema(yaml_directory, json_directory=""):
    # YAML Schema を読み込んで JSON Schema に変換
    yaml_schema_dict = load_yaml_schemas(yaml_directory)
    resolved_json_schema = merge_schemas_and_convert_json(yaml_schema_dict, json_directory)

    # JSON Schema を保存
    resolved_json_schema_path=""
    if json_directory:
        resolved_json_schema_filename = os.path.basename(yaml_directory) + ".json"
        resolved_json_schema_path = os.path.join(json_directory, resolved_json_schema_filename)

        # 保存
        save_schema(resolved_json_schema, resolved_json_schema_path)

    print("✅ JSON Schema の統合が完了しました:", resolved_json_schema_path)
    return resolved_json_schema


def merge_schemas_and_convert_json(yaml_schema_dict, output_path=""):
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

    # 保存
    merged_json_schema_path = save_schema(merged_json_schema, output_path=output_path)

    # 参照を解決
    resolved_json_schema = None
    with open(merged_json_schema_path, "r", encoding="utf-8") as f:
        resolved_json_schema = jsonref.load(f)

    return resolved_json_schema


def load_yaml_schemas(directory):
    """ディレクトリ内の YAML ファイルを読み込む"""
    yaml_schema_dict = {}

    for file_path in glob(os.path.join(directory, "*.yaml")):
        schema_name = os.path.splitext(os.path.basename(file_path))[0]

        with open(file_path, "r", encoding="utf-8") as f:
            yaml_schema = yaml.load(f)
            yaml_schema_dict[schema_name] = yaml_schema

    return yaml_schema_dict


def save_schema(schema_str: str, output_path="") -> str:
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(schema_str, f, indent=2, ensure_ascii=False)
    else:
        # save to temporary file
        tmp_ext = os.path.splitext(output_path)[1]
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=tmp_ext) as f:
            json.dump(schema_str, f, indent=2, ensure_ascii=False)
            output_path = f.name
    return output_path


def to_str_schema(schema_dict):
    return json.dumps(schema_dict, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    yaml_directory_ = "./rule_config"  # YAML ファイルの格納ディレクトリ
    yaml_to_json_schema(yaml_directory_)
