<script setup lang="ts">
import {markRaw, onMounted, reactive, ref} from 'vue'
import { useRouter } from 'vue-router'
import { useMagicKeys } from '@vueuse/core'
import { type API, useAutoInitRequest } from '@/services'
import  {useLoginRequest} from '@/services'
import { useI18n } from 'vue-i18n'
import {
  defineFormColumns,
  defineFormMenuColumns,
  defineFormSubmit,
  IFormExpose,
} from 'element-pro-components'
import { useGlobalState } from '@/composables/store'
const router = useRouter()
const loginRef = ref<IFormExpose>({})
const {t} = useI18n()
const state = useGlobalState()

const columns = defineFormColumns<API.LoginForm>([
  {
    label: t('layout.login.username'),
    prop: 'username',
    component: 'el-input',
    rules: { required: true, message: '请输入用户名', trigger: 'blur' },
    props: {
      clearable: true,
      // prefixIcon: markRaw(User),
      placeholder: t('layout.login.placeholder.username'),
      class: 'bg-blue-100',
    },
  },
  {
    label: t('layout.login.password'),
    prop: 'password',
    component: 'el-input',
    rules: [
      { required: true, message: '请输入密码', trigger: 'blur' },
      { min: 5, max: 16, message: '长度 5 到 16 个字符', trigger: 'blur' },
    ],
    props: {
      type: 'password',
      clearable: true,
      showPassword: true,
      // prefixIcon: markRaw(Lock),
      placeholder: t('layout.login.placeholder.password'),
    },
  },
])
const menu = defineFormMenuColumns({
  submitText: t('layout.login.submit'),
  reset: false,
})
const form = reactive<API.LoginForm>({
  username:'',
  password:''
})
const submit = defineFormSubmit(async (done, isValid) => {
  const valid = await loginRef.value.validate();
  if(valid){
    const {data, execute} = useLoginRequest(form);
    await execute();
    if (data.value) {
      state.value.access_token = data.value?.access_token;
      state.value.token_type = data.value?.token_type;
      await router.push('/')
      router.go(0)
    }
  }

  done()
})
// 自动判断初始化
const {execute: exeAutoInitRequest} = useAutoInitRequest()

onMounted(async () => {
  await exeAutoInitRequest()
})
</script>


<template>
  <div class="flex justify-center items-center w-full h-screen">
    <el-card class="w-3/12 max-w[90%] login-button bg-white/0">
      <div class="flex flex-row-reverse">

      </div>

      <div class="flex flex-row justify-center space-x-1 items-center">
        <el-image
          style="width: 32px;
            height: 32px"
          src="https://gw.alipayobjects.com/zos/antfincdn/PmY%24TNNDBI/logo.svg"
          fit="cover"
        />
        <h2 class="text-center">
          {{ $t('layout.login.title') }}
        </h2>
      </div>
      <h5 class="text-center">
        {{ $t('layout.login.describe') }}
      </h5>
      <pro-form
        ref="loginRef"
        v-model="form"
        :columns="columns"
        :menu="menu"
        label-position="top"
        @submit="submit"
      />
    </el-card>
  </div>
</template>
<style>
.login-button .el-button{
  width: 100%;
}
</style>