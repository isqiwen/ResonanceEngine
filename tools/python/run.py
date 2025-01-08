import sys
from pathlib import Path

# 动态添加 python 目录到 sys.path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# 运行模块
from build.build_config import main

if __name__ == "__main__":
    main()
