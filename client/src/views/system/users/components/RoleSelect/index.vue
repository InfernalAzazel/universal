<template>
  <el-select
      v-model="temp"
      placeholder="Select"
      :value-key="modelValue"
      remote
      filterable
      reserve-keyword
      @change="Change">
    <el-option
        v-for="item in data"
        :key="item.value"
        :label="item.label"
        :value="item.value">
      {{ item.label }}
    </el-option>
  </el-select>
</template>

<script lang="ts" setup>
import {ElSelect} from "element-plus";
import {onMounted, reactive, ref, toRefs, watch} from "vue";
import {useGlobalState} from "../../../../../composables";
import {useAll} from "../../../../../composables/crud";
import {Api} from "../../../../../utils";
import {useI18n} from "vue-i18n";
const {t} = useI18n()

const state = useGlobalState()
const props =defineProps({
  modelValue: {
    type: Object,
    default: {
      id: "",
      name_zh_cn: "",
      name_en_us: ""
    },
  },
})

const {modelValue} = toRefs(props)
const {list: RoleData,loadAll: exeRoleloadAll} = useAll(Api.roleAll)
const data = ref<any[]>([])
const temp = ref(state.value.locales === 'en-us'? modelValue?.value.name_en_us: modelValue?.value.name_zh_cn)
const emit = defineEmits(['update:modelValue'])
const Change = (val:any) => {
  temp.value = state.value.locales === 'en-us'? val.name_en_us: val.name_zh_cn
  emit('update:modelValue', val)
}



onMounted(async () => {
  data.value = []
  await exeRoleloadAll()
  data.value.push({
    value: {
      id: "***",
      name_zh_cn: "***",
      name_en_us: "***"
    },
    label: t(`system.users.association_role_delete`),
  })
  RoleData.value?.forEach(item => {
    data.value.push({
      label: state.value.locales === 'en-us'? item.name_en_us: item.name_zh_cn,
      value: {id: item.id, name_zh_cn: item.name_zh_cn, name_en_us: item.name_en_us}
    })
  })
})

watch(modelValue, (newVal, oldVal) => {
  Change(newVal)
}, {
  immediate: true
})
</script>