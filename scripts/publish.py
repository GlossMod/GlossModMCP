#!/usr/bin/env python
"""
GlossModMCP 发布助手脚本

用法:
    python scripts/publish.py --help
    python scripts/publish.py --check          # 检查准备情况
    python scripts/publish.py --upload pypi    # 上传到 PyPI
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional

def run_command(cmd: list[str], description: str = "") -> bool:
    """运行命令并报告结果"""
    if description:
        print(f"\n📋 {description}...")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ 完成")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 失败")
        print(f"错误: {e.stderr}")
        return False

def check_tools() -> bool:
    """检查必要工具是否已安装"""
    print("🔍 检查必要工具...")
    
    tools_ok = True
    
    # 检查 twine
    try:
        subprocess.run(["twine", "--version"], capture_output=True, check=True)
        print("✅ twine 已安装")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ twine 未安装，运行: pip install twine")
        tools_ok = False
    
    # 检查 git
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        print("✅ git 已安装")
    except FileNotFoundError:
        print("❌ git 未安装")
        tools_ok = False
    
    return tools_ok

def check_build() -> bool:
    """检查构建文件"""
    print("\n📦 检查构建文件...")
    
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("❌ dist 目录不存在，请先运行: uv build")
        return False
    
    wheel_file = list(dist_dir.glob("*.whl"))
    tar_file = list(dist_dir.glob("*.tar.gz"))
    
    if not wheel_file:
        print("❌ 没有找到 .whl 文件")
        return False
    
    if not tar_file:
        print("❌ 没有找到 .tar.gz 文件")
        return False
    
    print(f"✅ 找到 wheel: {wheel_file[0].name}")
    print(f"✅ 找到 tar.gz: {tar_file[0].name}")
    
    return True

def validate_package() -> bool:
    """验证包完整性"""
    print("\n✔️ 验证包完整性...")
    return run_command(["twine", "check", "dist/*"], "检查包元数据")

def upload_to_pypi(use_testpypi: bool = False) -> bool:
    """上传到 PyPI"""
    if use_testpypi:
        print("\n🚀 上传到 TestPyPI...")
        return run_command(
            ["twine", "upload", "--repository", "testpypi", "dist/*"],
            "上传到 TestPyPI"
        )
    else:
        print("\n🚀 上传到 PyPI...")
        return run_command(
            ["twine", "upload", "dist/*"],
            "上传到 PyPI"
        )

def create_github_release(version: str) -> bool:
    """创建 GitHub Release"""
    print(f"\n📝 创建 GitHub Release v{version}...")
    
    # 检查是否在 git 仓库中
    try:
        subprocess.run(["git", "rev-parse", "--git-dir"], 
                      capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print("❌ 不在 git 仓库中")
        return False
    
    # 创建标签
    if not run_command(
        ["git", "tag", "-a", f"v{version}", "-m", f"Release v{version}"],
        f"创建 git 标签 v{version}"
    ):
        return False
    
    # 推送标签
    if not run_command(
        ["git", "push", "origin", f"v{version}"],
        "推送标签到 GitHub"
    ):
        return False
    
    print(f"\n💡 现在访问 GitHub 创建 Release: https://github.com/GlossMod/gloss-mod-mcp/releases/new?tag=v{version}")
    return True

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="GlossModMCP 发布助手")
    parser.add_argument("--check", action="store_true", help="检查发布准备情况")
    parser.add_argument("--upload", choices=["pypi", "testpypi"], help="上传到 PyPI 或 TestPyPI")
    parser.add_argument("--release", metavar="VERSION", help="创建 GitHub Release")
    parser.add_argument("--full", action="store_true", help="完整发布流程")
    
    args = parser.parse_args()
    
    if args.check:
        print("=" * 50)
        print("GlossModMCP 发布准备检查")
        print("=" * 50)
        
        all_ok = True
        all_ok = check_tools() and all_ok
        all_ok = check_build() and all_ok
        
        if all_ok:
            print("\n✅ 所有检查通过，可以开始发布了！")
            print("\n推荐的发布命令:")
            print("  python scripts/publish.py --upload pypi")
            return 0
        else:
            print("\n❌ 检查失败，请解决上述问题后重试")
            return 1
    
    elif args.upload:
        if not check_tools():
            return 1
        
        if not check_build():
            return 1
        
        if not validate_package():
            return 1
        
        if args.upload == "pypi":
            if upload_to_pypi(use_testpypi=False):
                print("\n✅ 上传成功！")
                print("访问 https://pypi.org/project/glossmod-mcp/ 查看")
                return 0
            else:
                return 1
        else:
            if upload_to_pypi(use_testpypi=True):
                print("\n✅ 上传到 TestPyPI 成功！")
                print("访问 https://test.pypi.org/project/glossmod-mcp/ 查看")
                return 0
            else:
                return 1
    
    elif args.release:
        if create_github_release(args.release):
            print("✅ GitHub Release 准备完成")
            return 0
        else:
            return 1
    
    elif args.full:
        print("=" * 50)
        print("GlossModMCP 完整发布流程")
        print("=" * 50)
        
        if not check_tools():
            return 1
        
        if not check_build():
            return 1
        
        if not validate_package():
            return 1
        
        if not upload_to_pypi(use_testpypi=False):
            return 1
        
        print("\n✅ PyPI 上传成功！")
        print("\n现在可以创建 GitHub Release...")
        
        version = "1.0.0"  # TODO: 从 pyproject.toml 读取
        if create_github_release(version):
            print("\n✅ 完整发布流程完成！")
            return 0
    
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
