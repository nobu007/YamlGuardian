import os
import json
from glob import glob
from ruamel.yaml import YAML

yaml = YAML()

def yaml_to_json_schema(yaml_data, schema_name):
    """YAML データを JSON Schema に変換"""
    json_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": schema_name,
        "type": "object",
        "properties": {},
        "required": []
    }

    for key, value in yaml_data.items():
        field_schema = {}

        # 型を判定
        if isinstance(value, dict):
            field_schema["type"] = "object"
            field_schema["properties"] = yaml_to_json_schema(value, key)["properties"]
        elif isinstance(value, list):
            field_schema["type"] = "array"
            if value and isinstance(value[0], dict):  # オブジェクトの配列
                field_schema["items"] = yaml_to_json_schema(value[0], key)
            else:
                field_schema["items"] = {"type": "string"}  # デフォルトで文字列
        elif isinstance(value, int):
            field_schema["type"] = "integer"
        elif isinstance(value, float):
            field_schema["type"] = "number"
        elif isinstance(value, bool):
            field_schema["type"] = "boolean"
        else:
            field_schema["type"] = "string"

        json_schema["properties"][key] = field_schema
        json_schema["required"].append(key)

    return json_schema

def merge_schemas(schema_dict):
    """複数の JSON Schema を統合 ($defs に登録)"""
    merged_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {},
        "$defs": {}
    }

    for schema_name, schema in schema_dict.items():
        merged_schema["$defs"][schema_name] = schema
        merged_schema["properties"][schema_name] = {"$ref": f"#/$defs/{schema_name}"}

    return merged_schema

def load_yaml_files(directory):
    """ディレクトリ内の YAML ファイルを読み込んで JSON Schema に変換"""
    schema_dict = {}
    
    for file_path in glob(os.path.join(directory, "*.yaml")):
        schema_name = os.path.splitext(os.path.basename(file_path))[0]
        
        with open(file_path, "r", encoding="utf-8") as f:
            yaml_data = yaml.load(f)
            schema_dict[schema_name] = yaml_to_json_schema(yaml_data, schema_name)
    
    return schema_dict

def yaml_to_json(yaml_input, output_file=None):
    """YAMLをJSONに変換
    
    Args:
        yaml_input: YAML文字列またはファイルパス
        output_file: 出力JSONファイルパス（オプション）
    
    Returns:
        JSON文字列または辞書オブジェクト
    """
    # 入力処理
    if isinstance(yaml_input, (str, Path)) and Path(yaml_input).is_file():
        with open(yaml_input, 'r', encoding='utf-8') as f:
            data = yaml.load(f)
    else:
        data = yaml.load(yaml_input)
        
    # 出力処理
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return data
    else:
        return json.dumps(data, ensure_ascii=False, indent=2)

def json_to_yaml(json_input, output_file=None):
    """JSONをYAMLに変換
    
    Args:
        json_input: JSON文字列、ファイルパス、または辞書オブジェクト
        output_file: 出力YAMLファイルパス（オプション）
        
    Returns:
        YAML文字列または辞書オブジェクト
    """
    # 入力処理
    if isinstance(json_input, dict):
        data = json_input
    elif isinstance(json_input, (str, Path)) and Path(json_input).is_file():
        with open(json_input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = json.loads(json_input)
        
    # 出力処理
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f)
        return data
    else:
        from io import StringIO
        stream = StringIO()
        yaml.dump(data, stream)
        return stream.getvalue()

if __name__ == "__main__":
    yaml_directory = "./schemas"  # YAML ファイルの格納ディレクトリ
    schema_dict = load_yaml_files(yaml_directory)
    merged_schema = merge_schemas(schema_dict)

    with open("merged_schema.json", "w", encoding="utf-8") as f:
        json.dump(merged_schema, f, indent=2, ensure_ascii=False)

    print("✅ JSON Schema の統合が完了しました: merged_schema.json")
