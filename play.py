import paramiko

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import CommandArg


def search_and_print_files(pat):
    # 群晖NAS的IP地址、SSH端口、用户名和密码
    hostname = '127.0.0.1'
    port = 22
    username = 'username'
    password = 'password'

    # 共享文件夹路径
    shared_folder_path = '/volume2/play'

    # 创建 SSH 客户端
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)

    def list_files(path):
        # 执行 ls 命令列出文件
        stdin, stdout, stderr = ssh.exec_command(f'ls {path}')
        files = stdout.readlines()
        return [file.strip() for file in files]

    def search_files(pattern, path):
        files = list_files(path)
        matched_files = [file for file in files if pattern.lower() in file.lower()]
        return matched_files


    if pat == "list":
        # 返回目录中所有的文件名
        all_files = list_files(shared_folder_path)
        if all_files:
            ssh.close()
            return "\n".join(all_files)
        else:
            ssh.close()
            return "目录为空"
    else:
        # 搜索匹配的文件
        matched_files = search_files(pat, shared_folder_path)
        if matched_files:
            ssh.close()
            return matched_files[0]
        else:
            ssh.close()
            return "没有找到匹配的文件"

    # 关闭 SSH 连接
    ssh.close()

# 示例：调用函数
#print(search_and_print_files("1"))


play_voice = on_command("play", aliases={"mp3"})
@play_voice.handle()
async def voicelay(matcher: Matcher, args: Message = CommandArg()):
    amount = args.extract_plain_text()
    if not amount:
        return

    if "http" in amount:
        await matcher.send(MessageSegment.record(amount))
    else:
        result = search_and_print_files(amount)
    
        if result == "没有找到匹配的文件":
            await matcher.send("没有这种play")
        elif result == "目录为空":
            await matcher.send("目录为空")
        elif result == "upload.php":
            await matcher.send("http://127.0.0.1/upload.php")
        else:
            if "\n" in result:
                await matcher.send(f"{result}")
            else:
                url = f"http://127.0.0.1:666/{result}"
                await matcher.send(MessageSegment.record(url))

