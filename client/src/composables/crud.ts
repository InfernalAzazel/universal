/**
 * 封装表单提交
 * @param config.url 请求地址
 * @param config.showTip 显示提示，默认: `true`
 * @param config.type 提交请求方式 post | put，默认: `post`
 * @param config.transform 转换表单
 */
// import {IFormSubmit, StringObject} from "element-pro-components";
// import {computed, Ref, ref, unref} from "vue";
// import {usePost, usePut} from "./request";
//
//
// export function useForm<Form = StringObject, Data = unknown>({
//                                                                  url,
//                                                                  transform,
//                                                                  showTip = true,
//                                                                  type = 'post',
//                                                              }: UseFormConfig<Form>): UseFormReturn<Form, Data> {
//     const isFetching = ref(false)
//     const form = ref({}) as Ref<Form>
//     const payload = computed(() => {
//         return transform ? transform(unref(form)) : form.value
//     })
//     const _url = computed(() => {
//         return replaceId(unref(url), (payload.value as { id?: string }).id)
//     })
//     const postForm = usePost<Data>(url, payload)
//     const putForm = usePut<Data>(_url, payload)
//     const submit: IFormSubmit = async (done, isValid) => {
//         if (isValid) {
//             const res = await submitForm()
//
//             if (res.value) {
//                 unref(showTip) && appMessage('success', '提交成功！')
//             } else if (res.value !== null) {
//                 unref(showTip) && appMessage('warning', '提交失败！')
//             }
//         }
//         done()
//     }