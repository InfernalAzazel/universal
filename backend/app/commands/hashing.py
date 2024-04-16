from app.utils.hashing import hash_password, verify_password
import typer

app = typer.Typer(help="密码加密处理")


@app.command('h')
def h(password: str = typer.Argument(..., help="用户的明文密码")):
    """
    对用于存储的密码进行哈希处理
    """
    typer.echo("[+] 对密码进行哈希处理 ..")
    r = hash_password(password)
    typer.echo(f"[+] 加密前: {password} 加密后: {r}")
    typer.echo(f"[+] 操作完成")


@app.command('v')
def v(
        plain_password: str = typer.Argument(..., help="用户的明文密码"),
        hashed_password: str = typer.Argument(..., help="存储的哈希密码，用于验证")
):
    """
    根据用户提供的密码验证存储的密码
    """
    typer.echo("[+] 对用于存储的密码进行哈希处理 ..")
    b = verify_password(plain_password, hashed_password)
    n = '是' if b else '否'
    typer.echo(f"[+] 验证是否通过:  {n}")
    typer.echo(f"[+] 操作完成")
