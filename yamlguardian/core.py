import os

import yaml
from fastapi import HTTPException
from yamlguardian.directory_analyzer import DirectoryAnalyzer
from yamlguardian.hierarchy_merger import HierarchyMerger
from yamlguardian.hierarchy_reader import HierarchyReader
from yamlguardian.rules import RuleManager
from yamlguardian.validate import (format_errors, load_validation_rules,
                                   validate_data)


class YamlGuardian:
    def __init__(self, schema_file, relations_file=None, common_definitions_file=None):
        self.schema = self.load_yaml(schema_file)
        self.relations = self.load_yaml(relations_file) if relations_file else None
        self.common_definitions = self.load_yaml(common_definitions_file) if relations_file else None
        self.rule_manager = RuleManager(self.schema, self.relations, self.common_definitions)
        self.hierarchy_reader = HierarchyReader()
        self.hierarchy_merger = HierarchyMerger()

    def load_yaml(self, file_path):
        try:
            with open(file_path, encoding="utf-8") as file:
                return yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise ValueError(f"YAML読み込みエラー: {e}")
        except FileNotFoundError:
            raise ValueError(f"ファイルが見つかりません: {file_path}")
        except Exception as e:
            raise ValueError(f"予期しないエラーが発生しました: {e}")

    def validate(self, data):
        schema = load_validation_rules(self.schema)
        errors = validate_data(data, schema)
        if errors:
            return format_errors(errors)
        openapi_result = self.rule_manager.validate_openapi_schema(data)
        if openapi_result["message"] == "Validation failed":
            return openapi_result
        user_defined_result = self.rule_manager.validate_user_defined_yaml(data)
        if user_defined_result["message"] == "Validation failed":
            return user_defined_result
        user_provided_result = self.rule_manager.validate_user_provided_yaml(data)
        if user_provided_result["message"] == "Validation failed":
            return user_provided_result
        return {"message": "Validation successful"}

    def load_page_definitions(self, page_definitions_dir):
        page_definitions = {}
        for root, _, files in os.walk(page_definitions_dir):
            for file in files:
                if file.endswith(".yaml"):
                    file_path = os.path.join(root, file)
                    page_definitions[file_path] = self.load_yaml(file_path)
        return page_definitions

    def validate_page(self, page_data, page_definitions_dir):
        page_definitions = self.load_page_definitions(page_definitions_dir)
        for file_path, definition in page_definitions.items():
            schema = load_validation_rules(definition)
            errors = validate_data(page_data, schema)
            if errors:
                return format_errors(errors)
            openapi_result = self.rule_manager.validate_openapi_schema(page_data)
            if openapi_result["message"] == "Validation failed":
                return openapi_result
            user_defined_result = self.rule_manager.validate_user_defined_yaml(page_data)
            if user_defined_result["message"] == "Validation failed":
                return user_defined_result
            user_provided_result = self.rule_manager.validate_user_provided_yaml(page_data)
            if user_provided_result["message"] == "Validation failed":
                return user_provided_result
        return {"message": "Validation successful"}

    def analyze_and_save_directory_structure(self, root_dir, csv_file):
        analyzer = DirectoryAnalyzer()
        changes = analyzer.analyze_directory_structure(root_dir)
        analyzer.save_changes_to_csv(changes, csv_file)
        analyzer.save_cache()

    def read_hierarchy(self, file_path):
        return self.hierarchy_reader.read_hierarchy(file_path)

    def merge_hierarchies(self, hierarchies):
        return self.hierarchy_merger.merge_hierarchies(hierarchies)

    def validate_yaml(self, input_data):
        try:
            return self.validate_yaml_data(input_data.yaml_content)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
