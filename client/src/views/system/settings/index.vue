<template>
<pro-card
    shadow="never"
>
  <pro-form
      v-model="form"
      :columns="columns"
      :menu="menu"
      @submit="submit"
      @reset="reset"
  />
</pro-card>
</template>

<script lang="ts" setup>
import {markRaw, onMounted, ref} from 'vue'
import {ElMessage} from "element-plus";
import {defineFormSubmit, defineFormColumns, defineFormMenuColumns} from "element-pro-components";
import {useGet, usePut} from "../../../composables";
import EXDivider from "../../../components/EXDivider/index.vue";
import {Api} from "../../../utils";


const form = ref({})
const menu = defineFormMenuColumns({
  submit:true,
  reset:true,
  submitText:'保存',
  resetText:'重置',
})
const columns = defineFormColumns([
  {
    component: markRaw(EXDivider),
    prop: 'null',
    props: {
      title: '共用',
    }
  },
  {
    label: '时区',
    prop: 'shared.tz_info',
    component: 'el-input',
    props: {
      placeholder: 'Name'
    }
  },
  {
    component: markRaw(EXDivider),
    prop: 'null',
    props: {
      title: '数据库配置',
    }
  },
  {
    label: 'Host',
    prop: 'mongodb.host',
    component: 'el-input',
    props: {
      placeholder: 'Address'
    }
  },
  {
    label: '用户',
    prop: 'mongodb.username',
    component: 'el-input',
    props: {
      placeholder: 'Address'
    }
  },
  {
    label: '密码',
    prop: 'mongodb.password',
    component: 'el-input',
    props: {
      placeholder: 'Address'
    }
  },
  {
    component: markRaw(EXDivider),
    prop: 'null',
    props: {
      title: '令牌配置',
    }
  },
  {
    label: '密钥',
    prop: 'jwt.secret_key',
    component: 'el-input',
    props: {
      placeholder: 'Address'
    }
  },
  {
    label: '算法',
    prop: 'jwt.algorithm',
    component: 'el-input',
    props: {
      placeholder: 'Address'
    }
  },
  {
    label: '过期时间',
    prop: 'jwt.minutes',
    component: 'el-input',
    props: {
      placeholder: 'Address',
      type: 'number'
    }
  },
])


const {data, isFetching, execute} =useGet(Api.settingsData)
const {data: settingsDefaultData, execute: exeSettingsDefault} =useGet(Api.settingsDefault)
const {execute: exeSettingsEdit} = usePut(Api.settingsEdit, form)
const submit = defineFormSubmit(async (done, isValid, invalidFields) => {
  ElMessage(`submit: ${isValid}`)
  await exeSettingsEdit()
  done()
})

const reset = async () => {
  await exeSettingsDefault()
  form.value = settingsDefaultData.value as any
}

onMounted(async () => {
  if(!isFetching.value) {
    await execute()
    form.value = data.value as any
  }
})

</script>

<style scoped>
.pro-form > :deep(.form-title > .el-form-item__label) {
  font-size: 18px;
  color: var(--el-text-color-primary);
  font-weight: 500;
}
.pro-form :deep(.pro-form-menu) {
  @apply w-full sticky bottom-0 m-0;
  padding: 18px 0;
  background-color: var(--pro-card-bg-color);
}
</style>