from mpi4py import MPI
import numpy as np
from utils import *
import time

K = 3

def non_mp_main():
    K = 3  # 假设K已经给定
    data = read_json('documents.json')

    # 提取所有文档的K元组
    all_k_tuples = set()
    for doc in data:
        tokens = clean_and_tokenize(doc['content'])
        k_tuples = generate_k_tuples(tokens, K)
        all_k_tuples.update(k_tuples)

    # 为所有K元组创建索引
    global_index = {k_tuple: idx for idx, k_tuple in enumerate(all_k_tuples)}

    # 为每个文档创建特征向量
    for doc in data:
        tokens = clean_and_tokenize(doc['content'])
        k_tuples = generate_k_tuples(tokens, K)
        feature_vector = [1 if k_tuple in k_tuples else 0 for k_tuple in global_index]
        doc['feature'] = feature_vector

    # 将更新的数据保存回JSON文件
    with open('processed_data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        t0 = time.time()

    # 所有进程读取数据
    data = read_json('documents.json')

    # 分割任务
    chunk_size = len(data) // size
    start = rank * chunk_size
    end = start + chunk_size if rank != size - 1 else len(data)
    subset = data[start:end]

    # 处理每个进程的数据子集
    local_k_tuples = set()
    for doc in subset:
        tokens = clean_and_tokenize(doc['content'])
        k_tuples = generate_k_tuples(tokens, K)  # 假设K已经定义
        local_k_tuples.update(k_tuples)

    # 收集所有进程的K元组并创建全局索引
    all_k_tuples = comm.gather(local_k_tuples, root=0)
    if rank == 0:
        global_index = set.union(*all_k_tuples)
        global_index = {k_tuple: idx for idx, k_tuple in enumerate(global_index)}
        print("Len of feature:", len(global_index))

    # 广播全局索引
    global_index = comm.bcast(global_index if rank == 0 else None, root=0)

    # 创建特征向量
    local_features = []
    for doc in subset:
        tokens = clean_and_tokenize(doc['content'])
        k_tuples = generate_k_tuples(tokens, K)
        feature_vector = [1 if k_tuple in k_tuples else 0 for k_tuple in global_index]
        local_features.append({'id': doc['id'], 'feature': feature_vector})

    # 收集所有特征向量
    all_features = comm.gather(local_features, root=0)

    # 保存处理后的数据（仅在root进程）
    if rank == 0:
        for i, subset in enumerate(all_features):
            for feature in subset:
                data[i]['feature'] = feature
        with open('processed_data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("Finished. Time Elapsed: {}".format(time.time()-t0))
        

if __name__ == "__main__":
    
    main()
    
