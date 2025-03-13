def visualize_graph(final_df, title="Product Relationship Graph"):
    """
    使用pytorch_geometric可视化关系图
    - 红色边：relationship=1（上游）
    - 蓝色边：relationship=-1（下游）
    """
    # 构建节点索引映射
    all_nodes = set(final_df['primary_code'].tolist() + final_df['related_code'].tolist())
    node_idx = {node: i for i, node in enumerate(all_nodes)}
    
    # 提取边信息
    edges = []
    edge_labels = []
    for _, row in final_df.iterrows():
        src = node_idx[row['primary_code']]
        dst = node_idx[row['related_code']]
        edges.append((src, dst))
        edge_labels.append(row['relationship'])
    
    # 创建PyG数据对象
    edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
    edge_attr = torch.tensor(edge_labels, dtype=torch.float)
    data = Data(edge_index=edge_index, edge_attr=edge_attr, num_nodes=len(node_idx))
    
    # 转换为NetworkX图
    G = to_networkx(data, node_attrs=['x'], edge_attrs=['edge_attr'])
    
    # 可视化设置
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)  # 固定布局种子
    
    # 绘制边
    for i, (u, v, d) in enumerate(G.edges(data=True)):
        color = 'red' if d['edge_attr'] == 1 else 'blue'
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], 
                             edge_color=color, width=2, alpha=0.7,
                             arrowsize=20, arrowstyle='->')
    
    # 绘制节点和标签
    nx.draw_networkx_nodes(G, pos, node_size=800, node_color='lightblue')
    nx.draw_networkx_labels(G, pos, font_family='sans-serif', font_size=12)
    
    # 添加图例
    plt.legend([plt.Line2D([0], [0], color='red', lw=2, label='Upstream (1)'),
                plt.Line2D([0], [0], color='blue', lw=2, label='Downstream (-1)')],
               loc='upper right')
    
    plt.title(title, fontsize=14)
    plt.axis('off')
    plt.show()

# 使用示例
if __name__ == "__main__":
    # 假设原始数据
    raw_data = {
        'primary_code': ['A', 'A', 'B', 'C'],
        'related_code': ['B', 'C', 'A', 'D'],
        'relationship': [1, 1, -1, 1],
        'primary_ancestors': ['', 'B', '', 'A, B'],
        'related_ancestors': ['', '', '', '']
    }
    df = pd.DataFrame(raw_data)
    
    # 修剪关系并可视化
    final_df = trim_relations(df)
    print("Trimmed DataFrame:")
    print(final_df)
    
    # 可视化图（需要安装torch, torch_geometric, networkx, matplotlib）
    visualize_graph(final_df)
