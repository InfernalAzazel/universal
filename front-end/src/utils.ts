

export function splitString(value: any) {
  const newValue = typeof value === 'string' ? value : '';
  return newValue.includes(' ') ? newValue.split(' ') : [newValue];
}

export function getTagType  (method: string) {
  switch (method) {
    case 'GET':
      return 'primary';
    case 'POST':
      return 'success';
    case 'PUT':
      return 'warning';
    case 'DELETE':
      return 'danger';
    default:
      return 'secondary';
  }
}

/**
 * 递归获取树形数据和半选中的键
 *
 * @param data 源数据列表
 * @param parentId 当前父节点的ID
 * @param childrenKey 子节点在对象中的键名
 * @param depth 当前节点深度
 * @returns {treeData, halfCheckedKeys} 树形数据和半选中的键
 */
export function getTreeDataAndHalfCheckedKeys(
  data: any[],
  parentId: number = 0,
  childrenKey: string = "children",
  depth: number = 0
): { treeData: any[]; halfCheckedKeys: string[] } {
  const treeData: any[] = []; // 存储树形数据的数组
  const halfCheckedKeys: Set<string> = new Set(); // 存储半选中的键的唯一 uid

  // 遍历数据
  data
    .filter((item) => item.father === parentId) // 筛选出具有指定父节点的元素
    .forEach((item) => {
      const { treeData: itemChildren, halfCheckedKeys: childHalfCheckedKeys } = getTreeDataAndHalfCheckedKeys(
        data,
        item.key,
        childrenKey,
        depth + 1
      );

      if (itemChildren.length > 0) {
        halfCheckedKeys.add(item.uid); // 添加当前父节点的 uid
        item[childrenKey] = itemChildren; // 将子节点添加到父节点的 children 属性中
        childHalfCheckedKeys.forEach((node) => halfCheckedKeys.add(node)); // 将子节点的半选中键合并到当前父节点数组中
      }

      treeData.push({
        ...item,
        depth,
      });
    });

  return { treeData, halfCheckedKeys: Array.from(halfCheckedKeys) }; // 转换 Set 为数组并返回
}