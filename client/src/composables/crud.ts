import {
    ICrudSubmit,
    ICrudBeforeOpen,
    IFormSubmit,
    StringObject,
    UnknownObject,
    MaybeRef, defineCrudBeforeOpen, defineCrudSearch, defineCrudSubmit,
} from 'element-pro-components'
import {reactive, ref, unref} from "vue";
import {useDelete, useGet, usePost, usePut} from "./request";
import {Api} from "../utils";
import {PagesData} from "../utils/pubilc";
import {isObject} from "@vueuse/core";


export function useAll(urlSerach: string, immediate: boolean = false){

    const list = ref<any[]>([])

    const {isFetching, data, execute: exeList} = useGet(urlSerach)

    const loadAll = async () => {
        if (isFetching.value) return
        await exeList()
        if (data.value) {
            list.value = data.value as any[]
        }

    }

    unref(immediate) && loadAll()
    return {

        list,
        loadAll,
        isFetching,
    }
}

export function useList(urlSerach: string, immediate: boolean = false){
    const currentPage = ref(1)
    const pageSize = ref(10)
    const list = ref<any[]>([])
    const total = ref(0)
    const serachForm = ref({
        current_page: currentPage.value,
        page_size: pageSize.value,
    })
    const {isFetching, data, execute: exeList} = useGet<PagesData<any>>(urlSerach, serachForm)

    const loadList = async () => {
        if (isFetching.value) return
        serachForm.value.current_page = currentPage.value
        serachForm.value.page_size = pageSize.value
        await exeList()
        if (data.value) {
            list.value = data.value.data
            total.value = data.value.total
        }

    }

    unref(immediate) && loadList()
    return {
        currentPage,
        pageSize,
        list,
        total,
        serachForm,
        loadList,
        isFetching,
    }
}

/**
 * 封装 CRUD操作
 * @param urlSerach Search 请求地址
 * @param urlAdd Add 请求地址
 * @param urlEdit URL 请求地址
 * @param urlDelete URL 请求地址
 * @param immediate 是否立即获取数据列表
 */
export function useCrud(urlSerach: string, urlAdd: string, urlEdit: string, urlDelete: string, immediate: boolean = false) {

    const detail = ref({})
    const currentRowID = reactive({
        id: '',
    })
    const currentPage = ref(1)
    const pageSize = ref(10)
    const list = ref<any[]>([])
    const total = ref(0)
    const form = ref({})
    const serachForm = ref({
        current_page: currentPage.value,
        page_size: pageSize.value,
    })

    const {isFetching, data, execute: exeList} = useGet<PagesData<any>>(urlSerach, serachForm)
    const {execute: exeAdd} = usePost(urlAdd, form)
    const {execute: exeEdit} = usePut(urlEdit, form)
    const {execute: exeDel} = useDelete(urlDelete, currentRowID)

    const loadList = async () => {
        if (isFetching.value) return
        serachForm.value.current_page = currentPage.value
        serachForm.value.page_size = pageSize.value

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
        currentRowID.id = row.id
        await exeDel()
        await loadList()
    }
    return {
        form,
        serachForm,
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