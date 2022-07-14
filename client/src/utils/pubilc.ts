// NOTE: 如果你分页列表不是返回下面这种格式，需要根据情况修改。然后修改 `composables/crud.ts`
/** 分页数据公用组装 */
export interface PagesData<T> {
    data: T[]
    total: number
}