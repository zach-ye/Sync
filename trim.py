import pandas as pd
from collections import defaultdict

def trim_relations(df):
    """
    输入：原始DataFrame，包含列：
        - head_product_code, tail_product_code: 产品代码
        - relation: 1（正向）或 -1（反向）
        - head_ancestors, tail_ancestors: 每个产品的祖先列表（含自身？需确保包含自身，函数内自动添加）
    
    输出：修剪后的DataFrame，保留无冗余的直接关系
    """
    # 1. 标准化为正向关系（relation=1），统一处理反向关系
    df_positive = df[df['relation'] == 1].copy()
    df_negative = df[df['relation'] == -1].copy().rename(columns={
        'head_product_code': 'tail_product_code',
        'tail_product_code': 'head_product_code',
        'head_ancestors': 'tail_ancestors',
        'tail_ancestors': 'head_ancestors'
    })
    df_negative['relation'] = 1
    df_combined = pd.concat([df_positive, df_negative], ignore_index=True)

    # 2. 预处理：为每行生成带自身的祖先集合（集合操作更高效）
    df_combined['ancestors_head'] = df_combined.apply(
        lambda x: {x['head_product_code']} | set(x['head_ancestors']), axis=1
    )
    df_combined['ancestors_tail'] = df_combined.apply(
        lambda x: {x['tail_product_code']} | set(x['tail_ancestors']), axis=1
    )

    # 3. 核心逻辑：使用字典快速查询祖先冲突
    kept_pairs = defaultdict(set)  # key: head, value: {kept_tails}
    result = []

    for _, row in df_combined.iterrows():
        h, t = row['head_product_code'], row['tail_product_code']
        h_ancestors, t_ancestors = row['ancestors_head'], row['ancestors_tail']
        
        # 检查是否存在祖先对 (a, b) 已被保留
        conflict = any(
            t_ancestors & kept_pairs[a]  # 交集非空即冲突
            for a in h_ancestors
        )
        
        if not conflict:
            result.append(row)
            kept_pairs[h].add(t)  # 仅记录当前头尾，无需记录所有祖先

    # 4. 还原原始关系格式（含反向关系）
    final_df = pd.DataFrame({
        'head_product_code': [],
        'tail_product_code': [],
        'relation': [],
        'head_ancestors': [],
        'tail_ancestors': []
    })

    for row in result:
        # 正向关系（1）
        final_df = pd.concat([final_df, pd.DataFrame({
            'head_product_code': [row['head_product_code']],
            'tail_product_code': [row['tail_product_code']],
            'relation': [1],
            'head_ancestors': [list(row['head_ancestors'] - {row['head_product_code']})],  # 移除自身
            'tail_ancestors': [list(row['tail_ancestors'] - {row['tail_product_code']})]
        })], ignore_index=True)
        
        # 反向关系（-1）
        final_df = pd.concat([final_df, pd.DataFrame({
            'head_product_code': [row['tail_product_code']],
            'tail_product_code': [row['head_product_code']],
            'relation': [-1],
            'head_ancestors': [list(row['tail_ancestors'] - {row['tail_product_code']})],
            'tail_ancestors': [list(row['head_ancestors'] - {row['head_product_code']})]
        })], ignore_index=True)

    return final_df
