<script setup lang="ts">
import {useRouter} from "vue-router";
import { useI18n } from 'vue-i18n'
import { useGlobalState } from '@/composables/store'
const avatar = "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif";
const router = useRouter()
const state = useGlobalState()

const {t} = useI18n()
async function loginOut() {
  state.value.access_token = ''
  state.value.token_type = ''
  await router.push('/login')
}

</script>
<template>
  <el-dropdown>
        <span class="el-dropdown-link">
          <el-image
            :src="avatar"
            class="avatar"
          />
          <arrow-down class="el-icon-arrow-down el-icon--right" />
        </span>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item @click="loginOut">
          {{t(`layout.avatar.exit`)}}
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>


<style scoped>
.header-icon {
  margin: 0 16px 0 0;
  padding: 0;
  border: 0;
  background-color: transparent;
  cursor: pointer;
}
.header-icon svg {
  width: 28px;
  height: 28px;
  fill: var(--el-text-color-primary);
}
.el-dropdown-link .avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  vertical-align: middle;
}
.el-icon-arrow-down {
  width: var(--el-font-size-base);
  height: var(--el-font-size-base);
  vertical-align: middle;
}
</style>