<script setup lang="ts">
import { type Disk, useMonitorDictRequest } from '@/services'
import { onMounted, ref, watchEffect } from 'vue'
import { useI18n } from 'vue-i18n'

const {t} = useI18n()
const { data, execute } = useMonitorDictRequest()
const columns = ref<Record<string, string>[]>([])
const detail = ref<Record<string, string>>({})
const os_info = ref<Record<string, string>>({})
const cpu_usage = ref<Record<string, string>>({})
const memory_usage = ref<Record<string, string>>({})
const network_traffic = ref<Record<string, string>>({})


watchEffect(() => {
  if (data.value) {
    const disk_usage = data.value?.data?.disk_usage || []

    os_info.value = data.value?.data?.os_info || {}
    cpu_usage.value = data.value?.data?.cpu_usage || {}
    memory_usage.value = data.value?.data?.memory_usage || {}
    network_traffic.value = data.value?.data?.network_traffic || {}
    columns.value = []
    detail.value = {}
    // 遍历 disk_usage 数组，为每个 key 添加后缀
    disk_usage.forEach((disk: Disk, index: number) => {
      const suffix = index + 1 // 从 1 开始的后缀
      Object.entries(disk).forEach(([key, value]) => {
        const newKey = t(`dashboard.monitor.disk_info.${key}`) + '-' + suffix
        columns.value.push({ label: newKey, prop: newKey })
        detail.value[newKey] = value
      })
    })
  }
})

onMounted(async () => {
  await execute()
})
</script>

<template>
  <div class="flex flex-row space-x-1 pb-2.5">
    <pro-card shadow="always" :header="t(`dashboard.monitor.server`)">
      <el-descriptions v-for="(value, key) in os_info" :key="key">
        <el-descriptions-item :label="t(`dashboard.monitor.server.${key}`)">
          <el-tooltip :content="value">
            <span class="text-ellipsis">{{ value }}</span>
          </el-tooltip>
        </el-descriptions-item>
      </el-descriptions>
    </pro-card>
    <pro-card shadow="always" :header="t(`dashboard.monitor.memory`)">
      <el-descriptions v-for="(value, key) in memory_usage" :key="key">
        <el-descriptions-item :label="t(`dashboard.monitor.memory.${key}`)">
          <el-tooltip :content="value">
            <span class="text-ellipsis">{{ value }}</span>
          </el-tooltip>
        </el-descriptions-item>
      </el-descriptions>
    </pro-card>
    <pro-card shadow="always" :header="t(`dashboard.monitor.cpu`)">
      <el-descriptions v-for="(value, key) in cpu_usage" :key="key">
        <el-descriptions-item :label="t(`dashboard.monitor.cpu.${key}`)">
          <el-tooltip :content="value">
            <span class="text-ellipsis">{{ value }}</span>
          </el-tooltip>
        </el-descriptions-item>
      </el-descriptions>
    </pro-card>
    <pro-card shadow="always" :header="t(`dashboard.monitor.total_network_traffic`)">
      <el-descriptions v-for="(value, key) in network_traffic" :key="key">
        <el-descriptions-item :label="t(`dashboard.monitor.total_network_traffic.${key}`)">
          <el-tooltip :content="value">
            <span class="text-ellipsis">{{ value }}</span>
          </el-tooltip>
        </el-descriptions-item>
      </el-descriptions>
    </pro-card>
  </div>
  <pro-descriptions
    :columns="columns"
    :detail="detail"
    :title="t(`dashboard.monitor.disk_info`)"
    border
    :column="1"
  />
</template>

<style scoped>
.text-ellipsis {
  width: 150px; /* 设置一个宽度，超出这个宽度的文本会被省略 */
  white-space: nowrap; /* 保证文本在一行内显示不换行 */
  overflow: hidden; /* 隐藏超出容器宽度的文本 */
  text-overflow: ellipsis; /* 在文本溢出容器时显示省略号 */
}
</style>