import requests
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import CommandArg

# Flask API的地址
FLASK_API_URL = 'http://frp.aharry.top:7529'  # 请替换为实际的NAS IP地址

def search_files_via_api(pat):
    """通过Flask API搜索文件"""
    if pat == "list":
        # 请求列出所有文件
        try:
            response = requests.get(f"{FLASK_API_URL}/list", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    return "\n".join(data['files'])
                else:
                    return f"API错误: {data.get('message', '未知错误')}"
            else:
                return f"HTTP错误: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return f"连接API失败: {str(e)}"
    else:
        # 请求搜索文件
        try:
            response = requests.get(f"{FLASK_API_URL}/search", params={'pattern': pat}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    if data['file'] is None:
                        return "没有找到匹配的文件"
                    else:
                        return data['file']
                else:
                    return f"API错误: {data.get('message', '未知错误')}"
            else:
                return f"HTTP错误: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return f"连接API失败: {str(e)}"

play_voice = on_command("play", aliases={"mp3"})
@play_voice.handle()
async def voicelay(matcher: Matcher, args: Message = CommandArg()):
    amount = args.extract_plain_text()
    if not amount:
        return

    if "http" in amount:
        await matcher.send(MessageSegment.record(amount))
    else:
        result = search_files_via_api(amount)
    
        if result == "没有找到匹配的文件":
            await matcher.send("没有这种play")
        elif result.startswith(("API错误:", "HTTP错误:", "连接API失败:")):
            await matcher.send(f"搜索失败: {result}")
        elif result == "upload.php":
            await matcher.send("http://frp.aharry.top:666/upload.php")
        else:
            if "\n" in result:
                await matcher.send(f"{result}")
            else:
                url = f"http://frp.aharry.top:666/{result}"
                await matcher.send(MessageSegment.record(url))