#!/usr/bin/env python3
"""
Nexent 模型自动化管理脚本

功能：
- 从配置文件批量添加模型
- 删除所有模型
- 验证模型连通性

使用方法：
    python nexent_model_manager.py --config models_config.json
    python nexent_model_manager.py --delete-all
    python nexent_model_manager.py --verify-all
"""

import requests
import json
import argparse
import sys
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import time
import re


@dataclass
class ModelConfig:
    """模型配置数据类"""
    model_name: str
    model_type: str
    base_url: str
    api_key: str = ""
    max_tokens: int = 0
    display_name: str = ""
    model_factory: str = "OpenAI-API-Compatible"


class NexentModelManager:
    """Nexent模型管理器"""
    
    def __init__(self, base_url: str = "http://localhost:5010", token: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
        # 设置认证头
        if token:
            self.session.headers.update({
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            })
        else:
            self.session.headers.update({
                "Content-Type": "application/json"
            })
    
    def add_model(self, model_config: ModelConfig) -> bool:
        """添加单个模型"""
        url = f"{self.base_url}/api/model/create"
        
        payload = {
            "model_factory": model_config.model_factory,
            "model_name": model_config.model_name,
            "model_type": model_config.model_type,
            "base_url": model_config.base_url,
            "api_key": model_config.api_key,
            "max_tokens": model_config.max_tokens,
            "display_name": model_config.display_name or model_config.model_name
        }
        
        try:
            response = self.session.post(url, json=payload)
            
            if response.status_code == 200:
                print(f"✅ 模型 '{model_config.display_name or model_config.model_name}' 添加成功")
                return True
            else:
                error_msg = response.json().get('detail', response.text) if response.text else '未知错误'
                print(f"❌ 模型 '{model_config.display_name or model_config.model_name}' 添加失败: {error_msg}")
                return False
                
        except Exception as e:
            print(f"❌ 添加模型时发生错误: {e}")
            return False
    
    def batch_add_models(self, models: List[ModelConfig]) -> Dict[str, int]:
        """批量添加模型"""
        results = {"success": 0, "failed": 0}
        
        print(f"🚀 开始批量添加 {len(models)} 个模型...")
        
        for i, model in enumerate(models, 1):
            print(f"\n[{i}/{len(models)}] 正在添加模型: {model.display_name or model.model_name}")
            
            if self.add_model(model):
                results["success"] += 1
            else:
                results["failed"] += 1
            
            # 添加延迟避免请求过快
            if i < len(models):
                time.sleep(0.5)
        
        print(f"\n📊 批量添加完成: 成功 {results['success']} 个，失败 {results['failed']} 个")
        return results
    
    def delete_model(self, display_name: str) -> bool:
        """删除单个模型"""
        url = f"{self.base_url}/api/model/delete"
        
        try:
            response = self.session.post(url, params={"display_name": display_name})
            
            if response.status_code == 200:
                return True
            else:
                error_msg = response.json().get('detail', response.text) if response.text else '未知错误'
                print(f"❌ 删除失败: {error_msg}")
                return False
                
        except Exception as e:
            print(f"❌ 删除模型时发生错误: {e}")
            return False
    
    def delete_all_models(self) -> bool:
        """删除所有模型"""
        # 先获取所有模型
        models = self.list_models()
        if not models:
            print("📋 没有找到任何模型")
            return True
        
        print(f"🗑️  开始删除 {len(models)} 个模型...")
        
        success_count = 0
        failed_count = 0
        
        for i, model in enumerate(models, 1):
            display_name = model.get('display_name', model.get('model_name', 'Unknown'))
            
            print(f"\n[{i}/{len(models)}] 正在删除模型: {display_name}")
            
            if self.delete_model(display_name):
                success_count += 1
            else:
                failed_count += 1
            
            # 添加延迟避免请求过快
            if i < len(models):
                time.sleep(0.3)
        
        print(f"\n📊 删除完成: 成功 {success_count} 个，失败 {failed_count} 个")
        return failed_count == 0
    
    def verify_model(self, model_name: str) -> bool:
        """验证模型连通性"""
        url = f"{self.base_url}/api/model/healthcheck"
        
        try:
            response = self.session.post(url, params={"display_name": model_name})
            
            if response.status_code == 200:
                result = response.json()
                connectivity = result.get('data', {}).get('connectivity', False)
                
                if connectivity:
                    print(f"✅ 模型 '{model_name}' 连通性验证成功")
                else:
                    print(f"❌ 模型 '{model_name}' 连通性验证失败")
                    
                return connectivity
            else:
                error_detail = response.json().get('detail', response.text) if response.text else '未知错误'
                print(f"❌ 验证模型 '{model_name}' 失败: {error_detail}")
                return False
                
        except Exception as e:
            print(f"❌ 验证模型时发生错误: {e}")
            return False
    
    def list_models(self) -> List[Dict[str, Any]]:
        """获取模型列表"""
        url = f"{self.base_url}/api/model/list"
        
        try:
            response = self.session.get(url)
            
            if response.status_code == 200:
                result = response.json()
                models = result.get('data', [])
                return models
            else:
                print(f"❌ 获取模型列表失败: {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ 获取模型列表时发生错误: {e}")
            return []
    
    def verify_all_models(self) -> Dict[str, bool]:
        """验证所有模型的连通性"""
        models = self.list_models()
        results = {}
        
        if not models:
            print("📋 没有找到任何模型")
            return results
        
        print(f"🔍 开始验证 {len(models)} 个模型的连通性...")
        
        for i, model in enumerate(models, 1):
            display_name = model.get('display_name', model.get('model_name', ''))
            
            print(f"\n[{i}/{len(models)}] 验证模型: {display_name}")
            
            try:
                is_connected = self.verify_model(display_name)
                results[display_name] = is_connected
            except Exception as e:
                print(f"❌ 验证失败: {e}")
                results[display_name] = False
        
        # 统计结果
        success_count = sum(1 for v in results.values() if v)
        total_count = len(results)
        
        print(f"\n📊 验证完成: {success_count}/{total_count} 个模型连通性正常")
        return results


def resolve_env_variables(value: str) -> str:
    """解析环境变量引用"""
    if not isinstance(value, str):
        return value
    
    # 匹配 ${VAR_NAME} 格式的环境变量
    pattern = r'\$\{([^}]+)\}'
    
    def replace_env_var(match):
        env_var_name = match.group(1)
        env_value = os.getenv(env_var_name)
        
        if env_value is None:
            print(f"⚠️  警告: 环境变量 '{env_var_name}' 未设置")
            return match.group(0)  # 返回原始字符串
        
        return env_value
    
    return re.sub(pattern, replace_env_var, value)

def load_config_from_file(config_file: str) -> List[ModelConfig]:
    """从配置文件加载模型配置"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        models = []
        for model_data in data.get('models', []):
            # 解析环境变量
            api_key = resolve_env_variables(model_data.get('api_key', ''))
            base_url = resolve_env_variables(model_data['base_url'])
            
            models.append(ModelConfig(
                model_name=model_data['model_name'],
                model_type=model_data['model_type'],
                base_url=base_url,
                api_key=api_key,
                max_tokens=model_data.get('max_tokens', 0),
                display_name=model_data.get('display_name', ''),
                model_factory=model_data.get('model_factory', 'OpenAI-API-Compatible')
            ))
        
        return models
        
    except FileNotFoundError:
        print(f"❌ 配置文件 '{config_file}' 不存在")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ 配置文件格式错误: {e}")
        return []
    except Exception as e:
        print(f"❌ 读取配置文件时发生错误: {e}")
        return []


def main():
    parser = argparse.ArgumentParser(description='Nexent 模型自动化管理工具')
    parser.add_argument('--base-url', default='http://localhost:5010', help='Nexent API 基础URL')
    parser.add_argument('--token', help='认证令牌')
    
    # 主要功能
    parser.add_argument('--config', help='从配置文件批量添加模型')
    parser.add_argument('--delete-all', action='store_true', help='删除所有模型')
    parser.add_argument('--verify', help='验证指定模型的连通性')
    parser.add_argument('--verify-all', action='store_true', help='验证所有模型的连通性')
    
    args = parser.parse_args()
    
    # 创建管理器实例
    manager = NexentModelManager(base_url=args.base_url, token=args.token)
    
    try:
        if args.config:
            # 从配置文件批量添加
            models = load_config_from_file(args.config)
            if models:
                manager.batch_add_models(models)
            else:
                sys.exit(1)
                
        elif args.delete_all:
            # 删除所有模型
            if manager.delete_all_models():
                print("\n✅ 所有模型删除成功")
                sys.exit(0)
            else:
                print("\n❌ 部分模型删除失败")
                sys.exit(1)
                
        elif args.verify:
            # 验证模型连通性
            if manager.verify_model(args.verify):
                sys.exit(0)
            else:
                sys.exit(1)
                
        elif args.verify_all:
            # 验证所有模型连通性
            results = manager.verify_all_models()
            failed_models = [name for name, status in results.items() if not status]
            
            if failed_models:
                print(f"\n❌ 以下模型连通性异常: {', '.join(failed_models)}")
                sys.exit(1)
            else:
                print("\n✅ 所有模型连通性正常")
                sys.exit(0)
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        print("\n⚠️ 操作被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 程序执行时发生错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()