import pandas as pd
from collections import defaultdict

def trim_relations(df):
    """
    输入：原始DataFrame，包含列：
        - primary_product_code, related_product_code: 产品代码
        - relationship: 1（正向）或 -1（反向）
        - primary_product_ancestors, related_product_ancestors: 每个产品的祖先列表（含自身？需确保包含自身，函数内自动添加）
    
    输出：修剪后的DataFrame，保留无冗余的直接关系
    """
    # 提取除了指定列之外的其他列名
    other_columns = [col for col in df.columns if col not in ['primary_product_code', 'related_product_code', 'relationship', 'primary_product_ancestors', 'related_product_ancestors']]

    # 1. 标准化为正向关系（relationship=1），统一处理反向关系
    df_positive = df[df['relationship'] == 1].copy()
    df_negative = df[df['relationship'] == -1].copy().rename(columns={
        'primary_product_code': 'related_product_code',
        'related_product_code': 'primary_product_code',
        'primary_product_ancestors': 'related_product_ancestors',
        'related_product_ancestors': 'primary_product_ancestors'
    })
    df_negative['relationship'] = 1
    df_combined = pd.concat([df_positive, df_negative], ignore_index=True)

    # 2. 预处理：为每行生成带自身的祖先集合（集合操作更高效）
    df_combined['ancestors_primary'] = df_combined.apply(
        lambda x: {x['primary_product_code']} | set(x['primary_product_ancestors']), axis=1
    )
    df_combined['ancestors_related'] = df_combined.apply(
        lambda x: {x['related_product_code']} | set(x['related_product_ancestors']), axis=1
    )

    # 3. 核心逻辑：使用字典快速查询祖先冲突
    kept_pairs = defaultdict(set)  # key: primary, value: {kept_related}
    result = []

    for _, row in df_combined.iterrows():
        p, r = row['primary_product_code'], row['related_product_code']
        p_ancestors, r_ancestors = row['ancestors_primary'], row['ancestors_related']

        # 检查是否存在祖先对 (a, b) 已被保留
        conflict = any(
            r_ancestors & kept_pairs[a]  # 交集非空即冲突
            for a in p_ancestors
        )

        if not conflict:
            result.append(row)
            kept_pairs[p].add(r)  # 仅记录当前头尾，无需记录所有祖先

    # 4. 还原原始关系格式（含反向关系）
    final_rows = []
    for row in result:
        # 正向关系（1）
        new_row_positive = row.copy()
        new_row_positive['relationship'] = 1
        new_row_positive['primary_product_ancestors'] = list(row['ancestors_primary'] - {row['primary_product_code']})
        new_row_positive['related_product_ancestors'] = list(row['ancestors_related'] - {row['related_product_code']})
        final_rows.append(new_row_positive)

        # 反向关系（-1）
        new_row_negative = row.copy()
        new_row_negative['primary_product_code'] = row['related_product_code']
        new_row_negative['related_product_code'] = row['primary_product_code']
        new_row_negative['relationship'] = -1
        new_row_negative['primary_product_ancestors'] = list(row['ancestors_related'] - {row['related_product_code']})
        new_row_negative['related_product_ancestors'] = list(row['ancestors_primary'] - {row['primary_product_code']})
        final_rows.append(new_row_negative)

    final_df = pd.DataFrame(final_rows)
    # 调整列顺序，让指定列在前，其他列在后
    final_columns = ['primary_product_code', 'related_product_code', 'relationship', 'primary_product_ancestors', 'related_product_ancestors'] + other_columns
    final_df = final_df[final_columns]

    return final_df
