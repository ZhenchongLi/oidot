import zipfile


def raw(docx_path: str) -> str:
    """
    从docx文件中提取原始xml内容
    将docx文件当做一个zip文件，解压之后，获取文件夹中的所有文件
    遍历目录中文件，将文件内容合并到content中
    格式为：
    file_name (relative path to folder)
    content
    
    file_name
    content
    ...
    
    """

    content = ""
    
    try:
        with zipfile.ZipFile(docx_path, 'r') as zip_file:
            # 获取zip文件中的所有文件列表
            file_list = zip_file.namelist()
            
            for file_name in file_list:
                # 跳过目录
                if file_name.endswith('/'):
                    continue
                    
                try:
                    # 读取文件内容
                    with zip_file.open(file_name, 'r') as file:
                        file_content = file.read().decode('utf-8', errors='ignore')
                        
                        # 按照指定格式添加到content中
                        content += f"{file_name}\n{file_content}\n\n"
                        
                except Exception as e:
                    # 如果某个文件读取失败，记录错误但继续处理其他文件
                    content += f"{file_name}\n[Error reading file: {str(e)}]\n\n"
                    
    except Exception as e:
        content = f"Error opening docx file: {str(e)}"
    
    return content


if __name__ == "__main__":
    d_file: str = "docs/1.docx"
    content = raw(d_file)
    with open("output/1.txt", "w", encoding="utf-8") as f:
        f.write(content)






