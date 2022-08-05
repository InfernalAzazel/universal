<template>

    <div class="login">
    <el-card class="w-3/12 max-w[90%] login-button bg-white/0">
      <div class="flex flex-row-reverse">
        <lang-btu></lang-btu>
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
          ref="login"
          v-model="form"
          :columns="columns"
          :menu="menu"
          label-position="top"
          @submit="submit"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import {markRaw, onMounted, reactive, ref, watch} from 'vue'
import { useRouter } from 'vue-router'
import { useDark, useMagicKeys, useTitle } from '@vueuse/core'
import { Lock, User } from '@element-plus/icons-vue'
import {
  defineFormColumns,
  defineFormMenuColumns,
  defineFormSubmit,
  IFormExpose,
} from 'element-pro-components'
import {useGet, useGlobalState, usePost} from '../composables'
import { Api} from '../utils'
import type {InitState, LoginForm, ResLogin} from '../types'
import LangBtu from './components/LangBtu/index.vue'
import {useI18n} from "vue-i18n";
const router = useRouter()
const state = useGlobalState()
const { enter } = useMagicKeys()
const login = ref({} as IFormExpose)
const {t} = useI18n()

const columns = defineFormColumns<LoginForm>([
  {
    label: t('layout.login.username'),
    prop: 'username',
    component: 'el-input',
    rules: { required: true, message: '请输入用户名', trigger: 'blur' },
    props: {
      clearable: true,
      prefixIcon: markRaw(User),
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
      prefixIcon: markRaw(Lock),
      placeholder: t('layout.login.placeholder.password'),
    },
  },
])
const menu = defineFormMenuColumns({
  submitText: t('layout.login.submit'),
  reset: false,
})
const form = reactive<LoginForm>({
  username:'',
  password:''
})
const submit = defineFormSubmit(async (done, isValid) => {
  const valid = await login.value.validate()
  console.log(valid)
  if(valid){
    let sp = new URLSearchParams(form)
    const {data, execute} = usePost<ResLogin>(Api.login, sp)
    await execute()
    if (data.value) {
      state.value.access_token = data.value.access_token
      state.value.token_type = data.value?.token_type
      await router.push('/')
    }
  }

  done()
})
const {data: initStateData, execute: exeInitState} = useGet<InitState>(Api.initState)

onMounted(async () => {
  await exeInitState()
  if (initStateData.value?.switch) {
    await router.push('/init')
  }
})
</script>

<style>
.login {
  @apply flex justify-center items-center;
  @apply w-full h-screen;
  @apply bg-[url('../src/assets/background.svg')];
}


.login-button .el-button{
  @apply w-full
}
</style>
