def list_to_tree(data, parent_id, is_add_redirect=False, children="children", depth=0):
    """
    将列表转换为树结构

    :param data: 源数据列表
    :param parent_id: 父ID
    :param is_add_redirect: 是添加重定向
    :param children: children key
    :param depth: 深度
    :return: 树的列表
    """
    res = []
    for item in data:
        # 判断是否是父节点
        if item['father'] == parent_id:
            item_children = list_to_tree(data, int(item['key']), is_add_redirect, children, depth + 1)
            # 如果有子节点
            if item_children:
                if is_add_redirect:
                    # 父节点的 redirect 添加子节点 第一个数组的 path
                    item['redirect'] = item_children[0]['path']
                # 父节点的 children 添加子节点
                item[children] = item_children
            res.append({
                **item,
                **{'depth': depth}
            })
    return res
