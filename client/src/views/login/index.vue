<template>
  <div class=" h-screen" :style="{'background': 'url('+ background +')'}">
    <div class="flex flex-row justify-center pt-16">
      <a-image :width="40" src="https://aliyuncdn.antdv.com/vue.png"/>
      <span class="text-3xl">AdminTemplate</span>
    </div>

    <div class="flex justify-center mt-4">AdminTemplate 是武林中最具有影响力的葵花宝典</div>
    <div id="main">
      <a-form
          class="flex flex-col"
          layout="inline"
          :model="formState"
          @finish="handleFinish"
          @finishFailed="handleFinishFailed"
      >
        <a-form-item>

          <a-input v-model:value="formState.username" placeholder="Username" size="large" class="mt-12 ">
            <template #prefix>
              <UserOutlined class="text-slate-400"/>
            </template>
          </a-input>
          <a-input v-model:value="formState.password" type="password" placeholder="Password" size="large" class="mt-4">
            <template #prefix>
              <LockOutlined class="text-slate-400"/>
            </template>
          </a-input>
          <a-button
              class="mt-4"
              size="large"
              type="primary" block
              html-type="submit"
          >
            登录
          </a-button>
        </a-form-item>
      </a-form>
    </div>
    >
  </div>

</template>

<script setup lang="ts">
import {UserOutlined, LockOutlined} from '@ant-design/icons-vue';
import {message} from 'ant-design-vue'
import {ValidateErrorEntity} from 'ant-design-vue/es/form/interface';
import {reactive, UnwrapRef, computed, getCurrentInstance, inject} from 'vue';
import background from '../../assets/background.svg';
import {useStore} from "vuex";
import {useRouter} from 'vue-router'


const axios: any = inject('axios')  // inject axios
interface FormState {
  username: string;
  password: string;
}

const store = useStore();
const router = useRouter()
const key = 'updatable';

const formState: UnwrapRef<FormState> = reactive({
  username: '',
  password: '',
});

const handleFinish = () => {
  message.loading({ content: 'Loading...', key, duration: 8 });
  axios
      .post('/api/login', formState)
      .then((res: any) => {
        console.log(res.data.data.token)
        if (res.data.status === 'success') {
          message.success({ content: 'success!', key, duration: 2 });
          let token = res.data.data.token;
          store.commit("setToken", token);
          router.push({path: "/home"});
        }else{
          message.info({ content: '请输入有效的用户或者密码!', key, duration: 2 });
        }

      })
      .catch((error: any) => {
        message.error(error.message)
      });
};
const handleFinishFailed = (errors: ValidateErrorEntity<FormState>) => {
  console.log(errors);
};
</script>
<style>
#main {
  min-width: 260px;
  width: 368px;
  margin: 0 auto;
}
</style>
