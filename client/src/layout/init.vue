<template>
  <div class="login">
    <el-card class="w-3/12 max-w[90%] login-button">
      <h1 class="mb-2 text-center text-3xl">
        初始化
      </h1>
      <pro-form
          ref="login"
          v-model="form"
          :columns="columns"
          :menu="menu"
          label-position="top"
          @submit="submit"
      >
        <template #menu-left>
          <div class="w-full">
            <el-collapse v-model="activeNames" @change="handleChange">
              <el-collapse-item title="其他系统参数" name="1">
                <el-scrollbar class="w-full" style="height: 300px">
                  <el-divider content-position="left">共用</el-divider>
                  <el-space class="w-full" :fill="true" direction="vertical">
                    <el-input v-model="form.tz_info" placeholder="Please input">
                      <template #prepend>时区</template>
                    </el-input>
                  </el-space>
                  <el-divider content-position="left">数据库</el-divider>
                  <el-space class="w-full" :fill="true" direction="vertical">
                    <el-input v-model="form.db_host" placeholder="Please input">
                      <template #prepend>IP/域名</template>
                    </el-input>
                    <el-input v-model="form.db_username" placeholder="Please input">
                      <template #prepend>帐号</template>
                    </el-input>
                    <el-input v-model="form.db_password" placeholder="Please input">
                      <template #prepend>密码</template>
                    </el-input>
                  </el-space>
                  <el-divider content-position="left">令牌配置</el-divider>
                  <el-space class="w-full" :fill="true" direction="vertical">
                    <el-input v-model="form.secret_key" placeholder="Please input">
                      <template #prepend>密钥</template>
                    </el-input>
                    <el-input v-model="form.algorithm" placeholder="Please input">
                      <template #prepend>算法</template>
                    </el-input>
                    <el-input v-model="form.access_token_expire_minutes" placeholder="Please input">
                      <template #prepend>令牌有效时间/分钟</template>
                    </el-input>
                  </el-space>
                  <el-divider content-position="left">Exchange 邮箱配置</el-divider>
                  <el-space class="w-full" :fill="true" direction="vertical">
                    <el-input v-model="form.email_server" placeholder="Please input">
                      <template #prepend>服务器</template>
                    </el-input>
                    <el-input v-model="form.email_domain" placeholder="Please input">
                      <template #prepend>域名</template>
                    </el-input>
                    <el-input v-model="form.email" placeholder="Please input">
                      <template #prepend>邮箱</template>
                    </el-input>
                    <el-input v-model="form.email_user" placeholder="Please input">
                      <template #prepend>用户</template>
                    </el-input>
                    <el-input v-model="form.email_pwd" placeholder="Please input">
                      <template #prepend>密码</template>
                    </el-input>
                    <el-input v-model="form.email_attachment_file_name" placeholder="Please input">
                      <template #prepend>附件文件名</template>
                    </el-input>
                    <el-divider content-position="left">定时推送任务</el-divider>
                    <el-space class="w-full" :fill="true" direction="vertical">
                      <el-input v-model="form.push_email_task_hour" placeholder="Please input">
                        <template #prepend>时</template>
                      </el-input>
                      <el-input v-model="form.push_email_task_minute" placeholder="Please input">
                        <template #prepend>分</template>
                      </el-input>
                      <el-input v-model="form.push_email_task_second" placeholder="Please input">
                        <template #prepend>秒</template>
                      </el-input>
                    </el-space>
                  </el-space>
                </el-scrollbar>

              </el-collapse-item>
            </el-collapse>
          </div>
        </template>
      </pro-form>
    </el-card>

  </div>
</template>

<script setup lang="ts">
import {markRaw, reactive, ref, watch} from 'vue'
import {useRouter} from 'vue-router'
import {useDark, useMagicKeys, useTitle} from '@vueuse/core'
import {Lock, User} from '@element-plus/icons-vue'
import {
  defineFormColumns,
  defineFormMenuColumns,
  defineFormSubmit,
  IFormExpose,
} from 'element-pro-components'
import {useGlobalState, usePost} from '../composables'
import {Api} from '../utils'
import type {LoginForm, ResLogin} from '../types'
import {InitSystemForm} from "../types";

const router = useRouter()
const state = useGlobalState()
const {enter} = useMagicKeys()
const login = ref({} as IFormExpose)
const columns = defineFormColumns<InitSystemForm>([
  {
    label: '用户',
    prop: 'username',
    component: 'el-input',
    rules: {required: true, message: '请输入用户名', trigger: 'blur'},
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
      {required: true, message: '请输入密码', trigger: 'blur'},
      {min: 5, max: 16, message: '长度 5 到 16 个字符', trigger: 'blur'},
    ],
    props: {
      type: 'password',
      clearable: true,
      showPassword: true,
      prefixIcon: markRaw(Lock),
      placeholder: '请输入密码',
    },
  }, {
    label: '确认密码',
    prop: 'verify_password',
    component: 'el-input',
    rules: [
      {required: true, message: '请输入密码', trigger: 'blur'},
      {min: 5, max: 16, message: '长度 5 到 16 个字符', trigger: 'blur'},
      {
        validator: (rule, value, callback) => {
          if (value === '') {
            callback(new Error('请再次输入密码'))
            // password 是表单上绑定的字段
          } else if (value !== form.password) {
            callback(new Error('两次输入密码不一致!'))
          } else {
            callback()
          }
        },
        trigger: 'change'
      },
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
  submitText: '创建管理员',
  reset: false,
})
const form = reactive<InitSystemForm>({
  username: '',
  password: '',
  verify_password: '',
  tz_info: 'Asia/Shanghai',
  db_host: '127.0.0.1',
  db_username: 'universal',
  db_password: '123456',
  secret_key: '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7',
  algorithm: 'HS256',
  access_token_expire_minutes: 30,
  email_server: 'mail.x.com',
  email_domain: 'v01',
  email: 'x.x@x.com',
  email_user: 'uidp821321321',
  email_pwd: '12456',
  email_attachment_file_name: 'vul.csv',
  push_email_task_hour: '16',
  push_email_task_minute: '0',
  push_email_task_second: '0'
})


const submit = defineFormSubmit(async (done, isValid) => {
  const valid = await login.value.validate()
  console.log(valid)
  if (valid) {
    const {data, execute} = usePost(Api.login, form)
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
  @apply flex justify-center items-center flex-col;
  @apply w-full h-screen;
  @apply bg-[url('https://api.ixiaowai.cn/gqapi/gqapi.php')];
}

.login-button .el-button {
  @apply w-full
}

.collapse {
  overflow-y: auto /* 开启滚动显示溢出内容 */
}
</style>