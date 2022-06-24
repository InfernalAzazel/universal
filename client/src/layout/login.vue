<template>
  <div class="login">
    <el-card class="w-3/12 max-w[90%] login-button">
      <h1 class="mb-2 text-center text-3xl">
        管理后台
      </h1>
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
import {markRaw, reactive, ref, watch} from 'vue'
import { useRouter } from 'vue-router'
import { useDark, useMagicKeys, useTitle } from '@vueuse/core'
import { Lock, User } from '@element-plus/icons-vue'
import {
  defineFormColumns,
  defineFormMenuColumns,
  defineFormSubmit,
  IFormExpose,
} from 'element-pro-components'
import { useGlobalState, usePost } from '../composables'
import { Api} from '../utils'
import type { LoginForm, ResLogin } from '../types'
const router = useRouter()
const state = useGlobalState()
const { enter } = useMagicKeys()
const login = ref({} as IFormExpose)
const columns = defineFormColumns<LoginForm>([
  {
    label: '用户',
    prop: 'username',
    component: 'el-input',
    rules: { required: true, message: '请输入用户名', trigger: 'blur' },
    props: {
      clearable: true,
      prefixIcon: markRaw(User),
      placeholder: '请输入用户名',
    },
  },
  {
    label: '密码',
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
      placeholder: '请输入密码',
    },
  },
])
const menu = defineFormMenuColumns({
  submitText: '登录',
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
    const {data, execute} = usePost(Api.login, sp)
    await execute()
    if (data.value) {
      state.value = data.value as ResLogin
      router.push('/')
    }
  }

  done()
})

</script>

<style>
.login {
  @apply flex justify-center items-center;
  @apply w-full h-screen;
  @apply bg-[url('https://api.ixiaowai.cn/gqapi/gqapi.php')];
}


.login-button .el-button{
  @apply w-full
}
</style>
