from flask import Flask, jsonify, request
import random
import os

app = Flask(__name__)

# 共享文件夹路径
SHARED_FOLDER_PATH = '/volume2/aaa/play'

# 需要忽略的文件列表
IGNORED_FILES = ['app.py', 'nohup.log']

def list_files():
    """列出共享文件夹中的所有文件，忽略特定文件"""
    try:
        files = os.listdir(SHARED_FOLDER_PATH)
        # 过滤掉隐藏文件、非文件项和需要忽略的文件
        return [f for f in files if (
            os.path.isfile(os.path.join(SHARED_FOLDER_PATH, f)) and 
            not f.startswith('.') and
            f not in IGNORED_FILES
        )]
    except Exception as e:
        return f"错误: {str(e)}"

def search_files(pattern):
    """搜索匹配模式的文件，忽略特定文件"""
    try:
        all_files = list_files()
        if isinstance(all_files, str):  # 如果返回的是错误信息
            return all_files
            
        matched_files = [file for file in all_files if pattern.lower() in file.lower()]
        return matched_files
    except Exception as e:
        return f"错误: {str(e)}"

@app.route('/list', methods=['GET'])
def handle_list():
    """处理列出所有文件的请求"""
    files = list_files()
    if isinstance(files, list):
        return jsonify({"status": "success", "files": files})
    else:
        return jsonify({"status": "error", "message": files}), 500

@app.route('/search', methods=['GET'])
def handle_search():
    """处理搜索文件的请求"""
    pattern = request.args.get('pattern', '')
    if not pattern:
        return jsonify({"status": "error", "message": "缺少pattern参数"}), 400
        
    matched_files = search_files(pattern)
    
    if isinstance(matched_files, list):
        if not matched_files:
            return jsonify({"status": "success", "file": None, "message": "没有找到匹配的文件"})
        else:
            # 随机选择一个匹配的文件
            selected_file = random.choice(matched_files)
            return jsonify({"status": "success", "file": selected_file})
    else:
        return jsonify({"status": "error", "message": matched_files}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7529)