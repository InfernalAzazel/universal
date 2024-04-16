import sys
import typer
import importlib
import pkgutil
from app import commands

app = typer.Typer()


def load_commands():
    """
    从“commands”模块动态加载所有命令.
    """
    # 遍历 commands 模块中所有的子模块
    # 动态发现并加载所有子模块
    for finder, name, ispkg in pkgutil.iter_modules(commands.__path__, commands.__name__ + "."):
        module = importlib.import_module(name)
        # 我们假设每个模块都有一个名为 'app' 的 Typer 实例
        if hasattr(module, 'app'):
            # 从模块名中提取命令组名，例如 'commands.items' -> 'items'
            command_group_name = name.split('.')[-1]
            print(f"Loading {command_group_name} commands from {name}")
            app.add_typer(module.app, name=command_group_name)

    # 如果没有任何命令行参数（仅有脚本名称），显示帮助信息
    if len(sys.argv) == 1:
        print("No command provided, showing help.")
        # 这句调用 Typer 的帮助显示
        sys.argv.append("--help")


if __name__ == "__main__":
    load_commands()
    app()
