

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
    return content