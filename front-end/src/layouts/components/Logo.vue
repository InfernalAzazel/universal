<script setup lang="ts">
import { toRefs } from 'vue'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  collapse: {
    type: Boolean,
    default: false,
  }
})
const {collapse} = toRefs(props)
const {t} = useI18n()
</script>

<template>
  <el-image
    v-if="collapse" class="mt-2 ml-2.5"
    style="width: 32px;
            height: 32px"
    src="https://gw.alipayobjects.com/zos/antfincdn/PmY%24TNNDBI/logo.svg"
    fit="cover"
  />
  <div v-else class="flex flex-row">
    <el-image
      class="mt-2 ml-2.5"
      style="width: 32px;
            height: 32px"
      src="https://gw.alipayobjects.com/zos/antfincdn/PmY%24TNNDBI/logo.svg"
      fit="cover"
    />
    <span class="ml-2.5 mt-2.5 font-sans text-2xl h-full">{{t(`layout.title`)}}</span>
  </div>
</template>

<style scoped>

</style>