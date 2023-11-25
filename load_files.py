import os
import json

def load_data_to_json(data_dir):
    data_list = []  # 存储所有文档的信息
    for category in os.listdir(data_dir):  # 遍历每个分类
        category_path = os.path.join(data_dir, category)
        if os.path.isdir(category_path):  # 确保是文件夹
            for filename in os.listdir(category_path):  # 遍历该分类下的所有文件
                file_path = os.path.join(category_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()  # 读取文件内容
                    doc_id = filename.split('.')[0]  # 文件名作为ID
                    data_list.append({
                        'id': doc_id,
                        'content': content,
                        'category': category
                    })
    return data_list

def save_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

data_dir = 'data'  # 数据文件夹路径
data = load_data_to_json(data_dir)
save_json(data, 'documents.json')  # 将数据保存到output.json文件中
