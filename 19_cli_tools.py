"""
Python CLI 工具详解
包含：uv、pip、pipenv、poetry、pyenv、虚拟环境等
"""

import subprocess
import sys
import os


# ============================================
# 1. uv - 现代 Python 包管理器
# ============================================

def uv_introduction():
    """uv 介绍"""
    print("\n=== uv - 现代 Python 包管理器 ===")
    
    print("""
    uv 是什么?
    - Rust 编写的超快 Python 包管理器
    - pip 和 pip-tools 的替代品
    - 速度快 10-100 倍
    - 兼容 pip 接口
    
    特点:
    ✓ 极快的速度
    ✓ 全局缓存
    ✓ 并行下载
    ✓ 依赖解析
    ✓ 跨平台
    
    安装 uv:
    
    # macOS/Linux
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Windows (PowerShell)
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    
    # 使用 pip
    pip install uv
    
    # 使用 cargo
    cargo install --git https://github.com/astral-sh/uv uv
    """)


def uv_basic_usage():
    """uv 基本使用"""
    print("\n=== uv 基本使用 ===")
    
    print("""
    1. 创建虚拟环境:
    
    # 创建 .venv
    uv venv
    
    # 指定 Python 版本
    uv venv --python 3.11
    
    # 指定名称
    uv venv myenv
    
    # 激活虚拟环境
    source .venv/bin/activate  # Linux/macOS
    .venv\\Scripts\\activate     # Windows
    
    
    2. 安装包:
    
    # 安装单个包
    uv pip install requests
    
    # 安装多个包
    uv pip install requests numpy pandas
    
    # 安装特定版本
    uv pip install "requests==2.31.0"
    uv pip install "numpy>=1.24.0,<2.0.0"
    
    # 从 requirements.txt
    uv pip install -r requirements.txt
    
    # 安装开发依赖
    uv pip install -r requirements-dev.txt
    
    
    3. 同步依赖:
    
    # 确保环境与 requirements.txt 完全一致
    uv pip sync requirements.txt
    
    # 这会删除不在 requirements.txt 中的包
    
    
    4. 编译依赖:
    
    # 生成锁定的依赖文件
    uv pip compile requirements.in -o requirements.txt
    
    # 更新依赖
    uv pip compile --upgrade requirements.in
    
    
    5. 列出已安装的包:
    
    uv pip list
    uv pip list --format json
    
    
    6. 卸载包:
    
    uv pip uninstall requests
    uv pip uninstall -r requirements.txt
    """)


def uv_advanced_features():
    """uv 高级特性"""
    print("\n=== uv 高级特性 ===")
    
    print("""
    1. 依赖解析:
    
    # requirements.in
    flask
    requests
    
    # 生成 requirements.txt (包含所有依赖)
    uv pip compile requirements.in -o requirements.txt
    
    # 输出示例:
    # flask==3.0.0
    # requests==2.31.0
    # click==8.1.7
    # werkzeug==3.0.1
    # ...
    
    
    2. 多平台锁定:
    
    # 为不同平台生成依赖
    uv pip compile --universal requirements.in
    
    
    3. 缓存管理:
    
    # 查看缓存大小
    uv cache dir
    
    # 清理缓存
    uv cache clean
    
    
    4. 替代源:
    
    # 使用国内镜像
    uv pip install requests --index-url https://pypi.tuna.tsinghua.edu.cn/simple
    
    # 使用私有 PyPI
    uv pip install mypackage --index-url https://pypi.company.com/simple
    
    
    5. 工作区 (Workspace):
    
    # pyproject.toml
    [tool.uv]
    dev-dependencies = [
        "pytest",
        "black",
        "mypy",
    ]
    
    # 安装开发依赖
    uv pip install -e ".[dev]"
    
    
    6. 性能对比:
    
    命令                    pip      uv
    ----------------------------------------
    安装 numpy            5.2s     0.3s
    安装 pandas           8.1s     0.5s
    安装 100 个包         45s      2.1s
    重新安装 (缓存)       12s      0.1s
    """)


# ============================================
# 2. pip - 标准包管理器
# ============================================

def pip_basics():
    """pip 基础使用"""
    print("\n=== pip - Python 包管理器 ===")
    
    print("""
    1. 基本命令:
    
    # 安装包
    pip install package_name
    pip install package_name==1.0.0
    pip install package_name>=1.0.0
    
    # 升级包
    pip install --upgrade package_name
    pip install -U package_name
    
    # 卸载包
    pip uninstall package_name
    
    # 列出已安装的包
    pip list
    pip list --outdated
    
    # 显示包信息
    pip show package_name
    
    # 搜索包
    pip search keyword  # (已禁用)
    
    
    2. requirements.txt:
    
    # 导出依赖
    pip freeze > requirements.txt
    
    # 安装依赖
    pip install -r requirements.txt
    
    # requirements.txt 示例:
    requests==2.31.0
    numpy>=1.24.0,<2.0.0
    pandas
    flask[async]  # 包含额外依赖
    
    
    3. 配置:
    
    # pip.conf (Linux/macOS: ~/.pip/pip.conf)
    # pip.ini (Windows: %APPDATA%\\pip\\pip.ini)
    
    [global]
    index-url = https://pypi.tuna.tsinghua.edu.cn/simple
    trusted-host = pypi.tuna.tsinghua.edu.cn
    timeout = 120
    
    
    4. 高级用法:
    
    # 安装本地包
    pip install /path/to/package
    pip install ./my-package-1.0.0.tar.gz
    
    # 从 Git 安装
    pip install git+https://github.com/user/repo.git
    pip install git+https://github.com/user/repo.git@branch
    
    # 可编辑模式（开发）
    pip install -e .
    pip install -e /path/to/project
    
    # 指定 Python 版本
    python3.9 -m pip install package_name
    """)


# ============================================
# 3. 虚拟环境
# ============================================

def virtual_environments():
    """虚拟环境"""
    print("\n=== 虚拟环境 ===")
    
    print("""
    1. venv (内置):
    
    # 创建虚拟环境
    python -m venv myenv
    python -m venv .venv
    
    # 激活
    source myenv/bin/activate      # Linux/macOS
    myenv\\Scripts\\activate         # Windows
    
    # 停用
    deactivate
    
    # 删除
    rm -rf myenv
    
    
    2. virtualenv (第三方):
    
    # 安装
    pip install virtualenv
    
    # 创建
    virtualenv myenv
    virtualenv -p python3.9 myenv
    
    # 激活和停用同 venv
    
    
    3. virtualenvwrapper (便捷工具):
    
    # 安装
    pip install virtualenvwrapper
    
    # 配置 (~/.bashrc 或 ~/.zshrc)
    export WORKON_HOME=$HOME/.virtualenvs
    source /usr/local/bin/virtualenvwrapper.sh
    
    # 使用
    mkvirtualenv myproject
    workon myproject
    deactivate
    rmvirtualenv myproject
    
    # 列出所有环境
    lsvirtualenv
    
    
    4. conda (Anaconda):
    
    # 创建环境
    conda create -n myenv python=3.9
    
    # 激活
    conda activate myenv
    
    # 停用
    conda deactivate
    
    # 删除
    conda remove -n myenv --all
    
    # 导出环境
    conda env export > environment.yml
    
    # 从文件创建
    conda env create -f environment.yml
    """)


# ============================================
# 4. Poetry - 依赖管理
# ============================================

def poetry_introduction():
    """Poetry 介绍"""
    print("\n=== Poetry - 依赖管理与打包 ===")
    
    print("""
    Poetry 是什么?
    - 现代 Python 依赖管理工具
    - 类似于 npm、cargo
    - 依赖解析 + 虚拟环境 + 打包
    
    安装:
    curl -sSL https://install.python-poetry.org | python3 -
    
    
    1. 创建新项目:
    
    poetry new myproject
    cd myproject
    
    # 结构:
    myproject/
    ├── pyproject.toml
    ├── README.md
    ├── myproject/
    │   └── __init__.py
    └── tests/
        └── __init__.py
    
    
    2. 初始化现有项目:
    
    poetry init
    
    
    3. pyproject.toml:
    
    [tool.poetry]
    name = "myproject"
    version = "0.1.0"
    description = ""
    authors = ["Your Name <you@example.com>"]
    
    [tool.poetry.dependencies]
    python = "^3.9"
    requests = "^2.31.0"
    
    [tool.poetry.dev-dependencies]
    pytest = "^7.4.0"
    black = "^23.0.0"
    
    
    4. 管理依赖:
    
    # 添加依赖
    poetry add requests
    poetry add numpy@^1.24.0
    
    # 添加开发依赖
    poetry add --group dev pytest
    poetry add --group dev black mypy
    
    # 更新依赖
    poetry update
    poetry update requests
    
    # 删除依赖
    poetry remove requests
    
    
    5. 安装依赖:
    
    # 安装所有依赖
    poetry install
    
    # 不安装开发依赖
    poetry install --without dev
    
    # 仅安装开发依赖
    poetry install --only dev
    
    
    6. 运行命令:
    
    # 在虚拟环境中运行
    poetry run python script.py
    poetry run pytest
    
    # 进入虚拟环境
    poetry shell
    
    
    7. 构建和发布:
    
    # 构建包
    poetry build
    
    # 发布到 PyPI
    poetry publish
    
    # 发布到私有仓库
    poetry publish -r private-pypi
    
    
    8. 锁定文件:
    
    poetry.lock  # 自动生成，类似 package-lock.json
    
    # 更新锁定文件
    poetry lock --no-update
    """)


# ============================================
# 5. Pipenv
# ============================================

def pipenv_introduction():
    """Pipenv 介绍"""
    print("\n=== Pipenv ===")
    
    print("""
    Pipenv 是什么?
    - pip + virtualenv 的结合
    - 自动管理虚拟环境
    - Pipfile 和 Pipfile.lock
    
    安装:
    pip install pipenv
    
    
    1. 基本使用:
    
    # 初始化项目
    pipenv install
    
    # 安装包
    pipenv install requests
    pipenv install numpy==1.24.0
    
    # 安装开发依赖
    pipenv install --dev pytest
    
    # 从 requirements.txt 导入
    pipenv install -r requirements.txt
    
    
    2. Pipfile:
    
    [[source]]
    url = "https://pypi.org/simple"
    verify_ssl = true
    name = "pypi"
    
    [packages]
    requests = "*"
    numpy = "~=1.24.0"
    
    [dev-packages]
    pytest = "*"
    black = "*"
    
    [requires]
    python_version = "3.9"
    
    
    3. 运行命令:
    
    # 运行脚本
    pipenv run python script.py
    pipenv run pytest
    
    # 进入环境
    pipenv shell
    
    # 退出
    exit
    
    
    4. 环境管理:
    
    # 创建环境
    pipenv --python 3.9
    
    # 删除环境
    pipenv --rm
    
    # 查看环境位置
    pipenv --venv
    
    # 查看依赖图
    pipenv graph
    
    
    5. 锁定和同步:
    
    # 锁定依赖
    pipenv lock
    
    # 从锁定文件安装
    pipenv sync
    pipenv sync --dev
    """)


# ============================================
# 6. pyenv - Python 版本管理
# ============================================

def pyenv_introduction():
    """pyenv 介绍"""
    print("\n=== pyenv - Python 版本管理 ===")
    
    print("""
    pyenv 是什么?
    - 管理多个 Python 版本
    - 轻松切换版本
    - 不影响系统 Python
    
    安装:
    
    # macOS (Homebrew)
    brew install pyenv
    
    # Linux
    curl https://pyenv.run | bash
    
    # 配置 shell (~/.bashrc 或 ~/.zshrc)
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
    
    
    1. 基本使用:
    
    # 查看可安装的版本
    pyenv install --list
    
    # 安装 Python 版本
    pyenv install 3.11.0
    pyenv install 3.10.8
    pyenv install 3.9.16
    
    # 查看已安装的版本
    pyenv versions
    
    # 设置全局版本
    pyenv global 3.11.0
    
    # 设置局部版本（当前目录）
    pyenv local 3.10.8
    
    # 设置 shell 版本（当前会话）
    pyenv shell 3.9.16
    
    # 卸载版本
    pyenv uninstall 3.9.16
    
    
    2. 虚拟环境插件:
    
    # 安装 pyenv-virtualenv
    git clone https://github.com/pyenv/pyenv-virtualenv.git \\
        $(pyenv root)/plugins/pyenv-virtualenv
    
    # 创建虚拟环境
    pyenv virtualenv 3.11.0 myproject
    
    # 激活
    pyenv activate myproject
    
    # 停用
    pyenv deactivate
    
    # 删除
    pyenv virtualenv-delete myproject
    
    
    3. 自动激活:
    
    # 在项目目录
    pyenv local myproject
    
    # 进入目录时自动激活
    cd myproject  # 自动激活 myproject 环境
    """)


# ============================================
# 7. 其他 CLI 工具
# ============================================

def other_cli_tools():
    """其他 CLI 工具"""
    print("\n=== 其他 CLI 工具 ===")
    
    print("""
    1. ruff - 超快的 linter
    
    # 安装
    pip install ruff
    
    # 使用
    ruff check .
    ruff check --fix .
    ruff format .
    
    
    2. black - 代码格式化
    
    # 安装
    pip install black
    
    # 使用
    black script.py
    black .
    black --check .
    
    
    3. mypy - 类型检查
    
    # 安装
    pip install mypy
    
    # 使用
    mypy script.py
    mypy src/
    
    
    4. pytest - 测试框架
    
    # 安装
    pip install pytest
    
    # 使用
    pytest
    pytest tests/
    pytest -v
    pytest --cov
    
    
    5. ipython - 增强交互式 shell
    
    # 安装
    pip install ipython
    
    # 使用
    ipython
    
    
    6. jupyter - 笔记本
    
    # 安装
    pip install jupyter
    
    # 使用
    jupyter notebook
    jupyter lab
    
    
    7. pdm - 现代包管理器
    
    # 安装
    pip install pdm
    
    # 使用
    pdm init
    pdm add requests
    pdm install
    
    
    8. hatch - 项目管理
    
    # 安装
    pip install hatch
    
    # 使用
    hatch new myproject
    hatch env create
    hatch run python script.py
    """)


# ============================================
# 8. 工具对比
# ============================================

def tools_comparison():
    """工具对比"""
    print("\n=== 工具对比 ===")
    
    print("""
    功能对比:
    
    工具         速度   依赖解析  虚拟环境  打包发布  锁定文件
    --------------------------------------------------------
    pip         慢     基础      需配合    pip      无
    uv          极快   强大      是        pip      无
    poetry      中等   强大      是        是       是
    pipenv      慢     好        是        否       是
    conda       慢     强大      是        是       是
    
    
    选择建议:
    
    场景                    推荐工具
    --------------------------------------------------------
    个人项目/小项目         uv + pip
    团队项目               poetry
    数据科学               conda
    兼容性优先             pip + venv
    追求速度               uv
    需要打包发布           poetry
    
    
    工作流示例:
    
    # 方案 1: uv (最快)
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt
    
    # 方案 2: poetry (最现代)
    poetry install
    poetry run python script.py
    
    # 方案 3: pip + venv (最传统)
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    
    # 方案 4: conda (数据科学)
    conda create -n myenv python=3.9
    conda activate myenv
    conda install numpy pandas scikit-learn
    """)


# ============================================
# 9. 实战示例
# ============================================

def practical_examples():
    """实战示例"""
    print("\n=== 实战示例 ===")
    
    print("""
    1. 新项目快速开始 (uv):
    
    # 创建项目目录
    mkdir myproject && cd myproject
    
    # 创建虚拟环境
    uv venv
    source .venv/bin/activate
    
    # 创建 requirements.in
    cat > requirements.in << EOF
    fastapi
    uvicorn[standard]
    pydantic
    EOF
    
    # 编译依赖
    uv pip compile requirements.in -o requirements.txt
    
    # 安装
    uv pip sync requirements.txt
    
    # 开发
    # ... 编写代码 ...
    
    # 添加新依赖
    echo "requests" >> requirements.in
    uv pip compile requirements.in -o requirements.txt
    uv pip sync requirements.txt
    
    
    2. 团队项目 (poetry):
    
    # 初始化
    poetry new myproject
    cd myproject
    
    # 添加依赖
    poetry add fastapi uvicorn
    poetry add --group dev pytest black mypy
    
    # 安装
    poetry install
    
    # 运行
    poetry run uvicorn main:app
    
    # 测试
    poetry run pytest
    
    # 提交 pyproject.toml 和 poetry.lock
    git add pyproject.toml poetry.lock
    git commit -m "Add dependencies"
    
    
    3. CI/CD 配置:
    
    # .github/workflows/test.yml
    name: Test
    on: [push, pull_request]
    
    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v3
          
          - name: Set up Python
            uses: actions/setup-python@v4
            with:
              python-version: '3.11'
          
          - name: Install uv
            run: pip install uv
          
          - name: Install dependencies
            run: |
              uv venv
              source .venv/bin/activate
              uv pip sync requirements.txt
          
          - name: Run tests
            run: |
              source .venv/bin/activate
              pytest
    
    
    4. Docker 优化:
    
    # Dockerfile (使用 uv)
    FROM python:3.11-slim
    
    # 安装 uv
    RUN pip install uv
    
    WORKDIR /app
    
    # 复制依赖文件
    COPY requirements.txt .
    
    # 安装依赖 (利用缓存层)
    RUN uv pip install --system -r requirements.txt
    
    # 复制代码
    COPY . .
    
    CMD ["python", "main.py"]
    """)


# ============================================
# 10. 最佳实践
# ============================================

def best_practices():
    """最佳实践"""
    print("\n=== 最佳实践 ===")
    
    print("""
    依赖管理最佳实践:
    
    1. 总是使用虚拟环境
       ✓ 隔离项目依赖
       ✓ 避免版本冲突
       ✓ 易于清理
    
    2. 锁定依赖版本
       ✓ requirements.txt 锁定版本
       ✓ 或使用 poetry.lock / Pipfile.lock
       ✓ 确保可重现构建
    
    3. 分离生产和开发依赖
       requirements.txt      # 生产
       requirements-dev.txt  # 开发
    
    4. 使用约束文件
       pip install -c constraints.txt
    
    5. 定期更新依赖
       # 检查过期包
       pip list --outdated
       uv pip list --outdated
       
       # 更新
       pip install --upgrade package
    
    6. 安全扫描
       pip install safety
       safety check
       
       pip install pip-audit
       pip-audit
    
    7. 镜像配置
       # 使用国内镜像加速
       # ~/.pip/pip.conf
       [global]
       index-url = https://pypi.tuna.tsinghua.edu.cn/simple
    
    8. .gitignore
       .venv/
       venv/
       __pycache__/
       *.pyc
       .pytest_cache/
       .mypy_cache/
    
    9. 文档化依赖
       # README.md
       ## 安装
       ```bash
       uv venv
       source .venv/bin/activate
       uv pip install -r requirements.txt
       ```
    
    10. CI/CD 缓存
        - 缓存虚拟环境
        - 缓存包下载
        - 加速构建
    """)


# ============================================
# 主函数
# ============================================

def main():
    """运行所有示例"""
    print("=" * 60)
    print("Python CLI 工具详解")
    print("=" * 60)
    
    uv_introduction()
    uv_basic_usage()
    uv_advanced_features()
    
    pip_basics()
    virtual_environments()
    
    poetry_introduction()
    pipenv_introduction()
    pyenv_introduction()
    
    other_cli_tools()
    tools_comparison()
    practical_examples()
    best_practices()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)
    
    print("""
    快速参考:
    
    # uv (推荐)
    uv venv && source .venv/bin/activate
    uv pip install package
    
    # poetry
    poetry install
    poetry add package
    
    # pip + venv
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    """)


if __name__ == "__main__":
    main()
