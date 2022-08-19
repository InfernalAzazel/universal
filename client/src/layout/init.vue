<template>
  <div class="bg-image">
    <el-card class="w-3/12 max-w[90%] bg-white/0">
      <div class="flex flex-row-reverse">
        <lang-btu/>
      </div>
      <h2 class="mb-2 text-center">
        {{ $t('layout.init.title') }}
      </h2>
      <el-scrollbar class="w-full" style="height: 600px">
      <pro-form
          ref="login"
          class="init_button pro-form"
          v-model="form"
          :columns="columns"
          :menu="menu"
          label-position="top"
          @submit="submit"
     >
      </pro-form>
      </el-scrollbar>

    </el-card>

  </div>
</template>

<script setup lang="ts">
import {markRaw, onMounted, ref} from 'vue'
import {useRouter} from 'vue-router'
import {
  defineFormMenuColumns,
  defineFormSubmit,
  IFormExpose,
} from 'element-pro-components'
import {useGet, useGlobalState, usePost, usePut} from '../composables'
import {Api} from '../utils'
import {InitState, Settings} from "../types";
import LangBtu from './components/LangBtu/index.vue'
import EXDivider from "../components/EXDivider/index.vue";
import {useI18n} from "vue-i18n";
const {t} = useI18n()
const router = useRouter()
const state = useGlobalState()
const login = ref({} as IFormExpose)
const columns = [
  {
    component: markRaw(EXDivider),
    prop: 'null',
    props: {
      title: t(`layout.init.form.shared`),
    }
  },
  {
    prop: 'shared.tz_info',
    component: 'el-input',
    props: {
      placeholder: t(`layout.init.form.placeholder`),
      slots: {
        prepend: t(`layout.init.form.shared.tz_info`),
      }
    }
  },
  {
    component: markRaw(EXDivider),
    prop: 'null',
    props: {
      title: t(`layout.init.form.mongodb`),
    }
  },
  {
    prop: 'mongodb.host',
    component: 'el-input',
    props: {
      placeholder: t(`layout.init.form.placeholder`),
      slots: {
        prepend: t(`layout.init.form.mongodb.host`),
      }
    }
  },
  {
    prop: 'mongodb.username',
    component: 'el-input',
    props: {
      placeholder: t(`layout.init.form.placeholder`),
      slots: {
        prepend: t(`layout.init.form.mongodb.username`),
      }
    }
  },
  {
    prop: 'mongodb.password',
    component: 'el-input',
    props: {
      placeholder: t(`layout.init.form.placeholder`),
      slots: {
        prepend: t(`layout.init.form.mongodb.password`),
      }
    }
  },
  {
    component: markRaw(EXDivider),
    prop: 'null',
    props: {
      title: t(`layout.init.form.jwt`),
    }
  },
  {
    prop: 'jwt.secret_key',
    component: 'el-input',
    props: {
      placeholder: t(`layout.init.form.placeholder`),
      slots: {
        prepend: t(`layout.init.form.jwt.secret_key`),
      }
    }
  },
  {
    prop: 'jwt.algorithm',
    component: 'el-input',
    props: {
      placeholder: t(`layout.init.form.placeholder`),
      slots: {
        prepend: t(`layout.init.form.jwt.algorithm`),
      }
    }
  },
  {
    prop: 'jwt.minutes',
    component: 'el-input',
    props: {
      placeholder: t(`layout.init.form.placeholder`),
      type: 'number',
      slots: {
        prepend: t(`layout.init.form.jwt.minutes`),
      }
    }
  },
]
const menu = defineFormMenuColumns({
  submit:true,
  submitText: t(`layout.init.form.submit`),
  reset: false,
})


const form = ref<Settings>({} as Settings)
const {data: initStateData, execute: exeInitState} = useGet<InitState>(Api.initState)
const {data: initData, execute: exeInitData} = useGet<Settings>(Api.initData)
const {data: initSystemData, execute: exeInitSystem} = usePut(Api.initSystem, form)


const submit = defineFormSubmit(async (done, isValid) => {
  if (isValid) {
    await exeInitSystem()
    if (initSystemData.value) {
      await router.push('/login')
    }
  }

  done()
})

onMounted(async () => {
  await exeInitState()
  await exeInitData()
  if (initStateData.value?.switch !== true) {
    await router.push('/login')
  }else {
    form.value = initData.value as any
  }
})
</script>

<style>
.bg-image {
  @apply flex justify-center items-center flex-col;
  @apply w-full h-screen;
  @apply bg-[url('../assets/background.svg')];
}
.collapse {
  overflow-y: auto /* 开启滚动显示溢出内容 */
}

.init_button .el-button{
  @apply w-full
}
.pro-form .pro-form-menu {
  @apply w-full sticky bottom-0 m-0;
}
</style>