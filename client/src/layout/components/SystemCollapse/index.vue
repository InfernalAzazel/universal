<template>
  <el-collapse class="">
    <el-collapse-item :title="title" name="1">
      <el-scrollbar class="w-full" style="height: 300px">
        <div class="flex flex-col" v-for="v in columns">
          <el-divider v-if="v.component === 'el-divider'" content-position="left">{{ v.label }}</el-divider>
          <el-input v-if="v.component === 'el-input'" class="mt-2" v-model="form[v.prop]" :placeholder="v.props.placeholder">
            <template #prepend>{{ v.label }}</template>
          </el-input>
        </div>
      </el-scrollbar>

    </el-collapse-item>
  </el-collapse>
</template>

<script lang="ts" setup>
const props = defineProps({
  title: {
    type: String,
    default: '',
  },
  form: {
    type: [Array, Object],
    default: [],
  },
  columns: {
    type: [Array, Object],
    default: [],
  },
})

</script>

<style scoped>

</style>