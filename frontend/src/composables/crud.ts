import type { PagesData } from '@/services'
import { useDelete, useGet, usePost, usePut } from '@/composables/request'
import {
  defineCrudBeforeOpen, defineCrudSearch, defineCrudSubmit,
} from 'element-pro-components'
import {ref, unref, computed} from "vue";

/**
 * 封装 CRUD操作
 * @param url 请求地址

 * @param immediate 是否立即获取数据列表
 */
export function useCrud(url: string, immediate: boolean = false) {

  const detail = ref({})
  const currentRowID = ref('')
  const currentPage = ref(1)
  const pageSize = ref(10)
  const list = ref<any[]>([])
  const total = ref(0)
  const form = ref({})
  const searchForm = ref({
    current_page: currentPage.value,
    page_size: pageSize.value,
  })



  const _url = computed(() => `${url}/${currentRowID.value}?id=${currentRowID.value}`);

  const {isFetching, data, execute: exeList} = useGet<PagesData<any>>(url, searchForm)
  const {execute: exeAdd} = usePost(url, form)
  const {execute: exeEdit} = usePut(_url, form);
  const {execute: exeDel} = useDelete(_url);

  const loadList = async () => {
    if (isFetching.value) return
    searchForm.value.current_page = currentPage.value
    searchForm.value.page_size = pageSize.value

    await exeList()
    if (data.value) {
      list.value = data.value.data
      total.value = data.value.total
    }

  }

  unref(immediate) && loadList()

  const beforeOpen = defineCrudBeforeOpen((done, type, row) => {
    if (type === 'edit') {
      form.value = row || {}
      currentRowID.value = row.id || ''

    } else if (type === 'detail') {
      detail.value = row || {}
    }
    done()
  })

  const search = defineCrudSearch(async (done, isValid, invalidFields) => {
    if (isValid) {
      await loadList()
    }
    done()
  })

  const submit = defineCrudSubmit(
    async (close, done, type, isValid, invalidFields) => {
      if (type === 'add') {
        await exeAdd()
        close()
        done()
      } else if (type === 'edit') {
        await exeEdit()
        close()
        done()
      }
      await loadList()

    }
  )
  const deleteRow = async (row: any) => {
    currentRowID.value = row.id
    await exeDel()
    await loadList()
  }
  return {
    form,
    searchForm,
    detail,
    loadList,
    currentPage,
    pageSize,
    list,
    total,
    isFetching,
    currentRowID,
    beforeOpen,
    submit,
    search,
    deleteRow,
  }
}