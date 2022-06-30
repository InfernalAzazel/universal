<template>
  <el-dropdown>
        <span class="el-dropdown-link">
          <el-image
              v-if="state.avatar"
              :src="state.avatar"
              class="avatar"
          />
          {{ state.name }}
          <arrow-down class="el-icon-arrow-down el-icon--right" />
        </span>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item @click="loginOut">
          退出
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup lang="ts">
// defineProps<{ name: string }>()
import {useRoute, useRouter} from "vue-router";
import {useGlobalState} from "../../composables";

const route = useRoute()
const router = useRouter()
const state = useGlobalState()

async function loginOut() {
  state.value = {
    name: '',
    avatar: '',
    token: '',
  }
  await router.push('/login')
}

</script>
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
