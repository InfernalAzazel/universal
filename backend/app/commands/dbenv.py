import asyncio

import typer

from app.models.admin import User, Role, Menu, Interface
from app.utils.db import async_db_engine
from app.utils.dbenv import DBenv

app = typer.Typer(help="管理数据库环境")


@app.command('i')
def init():
    """
    初始化数据库
    """

    async def db():
        db_engine = async_db_engine()
        settings_names = [
            User.Settings.name,
            Role.Settings.name,
            Menu.Settings.name,
            Interface.Settings.name
        ]
        # 检查所有列出的集合是否已初始化（即是否为空）
        is_init_needed = any([await db_engine[name].count_documents({}) == 0 for name in settings_names])
        if is_init_needed:
            ei = DBenv()
            await ei.import_mongodb()
            typer.echo("[+] 操作完成")
        else:
            typer.echo("[!] 数据库已存在数据，忽略初始化操作")

    typer.echo("初始化数据库...")
    asyncio.run(db())


@app.command("s")
def save():
    """
    数据库数据保存到本地
    """
    typer.echo("数据库数据保存到本地...")
    db_env = DBenv()
    asyncio.run(db_env.export_mongodb())
    typer.echo("[+] 操作完成")
