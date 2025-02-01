import yaml
import jsonschema
import sys
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from yamlguardian.validate import validate_yaml_data

# スキーマのロード関数
def load_schema(schema_path: str):
    """YAMLスキーマファイルを読み込む"""
    with open(schema_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# スキーマを読み込む（本番環境用）
schema = load_schema('schema.yaml')

# FastAPI アプリケーションのセットアップ
app = FastAPI()

class YamlInput(BaseModel):
    yaml_content: str

@app.get("/schema", response_class=JSONResponse)
def get_schema():
    """スキーマを JSON 形式で公開するエンドポイント"""
    return schema

@app.post("/validate")
def validate_yaml_endpoint(input_data: YamlInput):
    """YAML データをバリデーションするエンドポイント"""
    try:
        return validate_yaml_data(input_data.yaml_content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# コマンドライン実行時
if __name__ == "__main__":
    if len(sys.argv) > 1:
        validate_yaml_local(sys.argv[1])
    else:
        uvicorn.run(app, host='0.0.0.0', port=8000)
