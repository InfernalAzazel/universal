<script lang="ts" setup>
import { ref } from 'vue'
import { ElTree } from 'element-plus'
import { nanoid } from 'nanoid'
import { defineCrudColumns, defineCrudMenuColumns } from 'element-pro-components'
import { useI18n } from 'vue-i18n'
import {
  type API,
  useInterfaceArrayRequest,
  useMenuArrayRequest,
  useRoleCrudRequest,
  useRoleEditRequest
} from '@/services'
import { getTagType, getTreeDataAndHalfCheckedKeys, splitString } from '@/utils'

type InterfaceGroupTree = {
  uid: string;
  isFather: boolean;
  title: string;
  children: API.Interface[];
}

const { t } = useI18n()
const crudRef = ref()
const menu = defineCrudMenuColumns({
  label: t(`crud.label`),
  addText: t(`crud.addText`),
  detailText: t(`crud.detailText`),
  editText: t(`crud.editText`),
  searchText: t(`crud.searchText`),
  searchResetText: t(`crud.searchResetText`),
  submitText: t(`crud.submitText`),
  resetText: t(`crud.resetText`),
  detail: false,
  edit: false,
  del: false,
  searchReset: true,
  fixed: 'right',
  width: '350'
})


const currentRow = ref<API.Role | any>({})
const currentUID = ref<string>('')

const columns = defineCrudColumns([
  {
    label: t(`system.role.uid`),
    prop: 'uid',
    component: 'el-input',
    detail: true,
    props: {
      disabled: true
    }
  },
  {
    label: t(`system.role.title`),
    prop: 'title',
    component: 'el-input',
    form: true,
    search: true,
    detail: true
  },
  {
    label: t(`system.role.description`),
    prop: 'description',
    component: 'el-input',
    props: {
      type: 'textarea',
      rows: 14,
      minRows: 12,
      maxRows: 24
    },
    form: true,
    detail: true
  },
  {
    label: t(`el-date-picker.create_at`),
    prop: 'create_at',
    component: 'el-date-picker',
    props: {
      type: 'datetimerange',
      rangeSeparator: '-',
      startPlaceholder: 'start',
      endPlaceholder: 'end',
      format: 'YYYY-MM-DD',
      valueFormat: 'YYYY-MM-DDTHH:mm:ss'
    },
    search: true,
    detail: true
  },
  {
    label: t(`el-date-picker.update_at`),
    prop: 'update_at',
    component: 'el-date-picker',
    props: {
      type: 'datetimerange',
      rangeSeparator: '-',
      startPlaceholder: 'start',
      endPlaceholder: 'end',
      format: 'YYYY-MM-DD',
      valueFormat: 'YYYY-MM-DDTHH:mm:ss'
    },
    search: true,
    detail: true
  }
])
const tableColumns = ref(JSON.parse(JSON.stringify(columns)))

const isDialogPermission = ref(false)
const permissionType = ref<number>(0)

const menuTreeRef = ref<InstanceType<typeof ElTree>>()
const menuCheckedKeys = ref<string[]>([])
const menuQuery = ref({})
const menuTrees = ref([])
const menuAllHalfCheckedKeys = ref([])

const interfaceTreeRef = ref<InstanceType<typeof ElTree>>()
const interfaceCheckedKeys = ref<string[]>([])
const interfaceQuery = ref({})
const InterfaceTrees = ref([])
const interfaceAllHalfCheckedKeys = ref([])

const treeDefaultProps = ref({
  children: 'children',
  label: 'title'
})

const rules = {
  title: { required: true, message: t(`rules.role.title`), trigger: 'blur' },
  description: { required: true, message: t(`rules.role.description`), trigger: 'blur' }
}

const {
  form,
  searchForm,
  detail,
  loadList,
  currentPage,
  pageSize,
  list,
  total,
  isFetching,
  beforeOpen,
  submit,
  search,
  deleteRow
} = useRoleCrudRequest(true)

const { data: interfaceData, execute: exeInterface } = useInterfaceArrayRequest(interfaceQuery)
const { data: menuData, execute: exeMenu } = useMenuArrayRequest(menuQuery)
const { execute: exeRoleEdit } = useRoleEditRequest(currentUID, currentRow)

function getInterfaceGroupTrees(data: API.Interface[]) {
  const halfCheckedKeys: Set<string> = new Set()
  const groupTrees: InterfaceGroupTree[] = data.reduce((acc: InterfaceGroupTree[], entry: API.Interface) => {
    let group = acc.find(g => g.title === entry.group)
    if (group) {
      group.children.push(entry)
    } else {
      const uid = nanoid()
      halfCheckedKeys.add(uid)
      acc.push({ uid: uid, title: entry.group, isFather: true, children: [entry] })
    }
    return acc
  }, [])
  return { groupTrees, halfCheckedKeys: Array.from(halfCheckedKeys) }
}

async function handleOpenDialogPermission(value: number, row: any) {
  // value == 0 代表打开菜单 1 代表打开接口
  permissionType.value = value
  currentUID.value = row.uid || ''
  currentRow.value = row
  if (value === 0) {
    menuQuery.value = { is_all_query: true }
    await exeMenu()
    if (menuData.value) {
      const { treeData, halfCheckedKeys } = getTreeDataAndHalfCheckedKeys(menuData.value?.data || [])
      menuTrees.value = treeData
      menuAllHalfCheckedKeys.value = halfCheckedKeys
      menuCheckedKeys.value = currentRow.value.menu_permission  // 设置选中
    }

  } else {
    interfaceQuery.value = { is_all_query: true }
    await exeInterface()
    if (interfaceData.value) {
      const { groupTrees, halfCheckedKeys } = getInterfaceGroupTrees(interfaceData.value?.data || [])
      InterfaceTrees.value = groupTrees
      interfaceAllHalfCheckedKeys.value = halfCheckedKeys
      interfaceCheckedKeys.value = currentRow.value.interface_permission  // 设置选中
    }
  }
  isDialogPermission.value = true
}

async function handleSave() {
  isDialogPermission.value = false
  if (permissionType.value === 0) {
    currentRow.value.menu_permission =  menuTreeRef.value?.getCheckedKeys()
  } else {
    const keys = interfaceTreeRef.value?.getCheckedKeys()
    currentRow.value.interface_permission = keys?.filter((key) => !interfaceAllHalfCheckedKeys.value.includes(key))
  }
  await exeRoleEdit()
  await loadList()
}

</script>
<template>
  <pro-card>
    <pro-crud
      ref="crudRef"
      v-model="form"
      v-model:search="searchForm"
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      v-loading="isFetching"
      :columns="columns"
      :menu="menu"
      :data="list"
      :total="total"
      :detail="detail"
      :before-open="beforeOpen"
      @search="search"
      @load="loadList"
      @search-reset="loadList"
      @submit="submit"
      :table-columns="tableColumns"
      :rules="rules"
      layout="total, ->, jumper, prev, pager, next, sizes"
      border
      stripe
      show-overflow-tooltip
    >
      <template #action>
        <pro-column-setting
          v-model="tableColumns"
        />
      </template>
      <template #menu="{row, size }">
        <el-button :size="size" type="primary" @click="handleOpenDialogPermission(0, row)" link> {{t(`system.role.menu_permissions`)}}</el-button>
        <el-button :size="size" type="primary" @click="handleOpenDialogPermission(1, row)" link> {{t(`system.role.interface_permissions`)}}</el-button>
        <el-button :size="size" type="primary" @click="crudRef.openDialog('edit', row)" link> {{ t(`crud.editText`) }}
        </el-button>
        <el-button :size="size" type="info" @click="crudRef.openDialog('detail', row)" link>
          {{ t(`crud.detailText`) }}
        </el-button>
        <el-popconfirm :title="$t(`crud.isDelText`)" @confirm="deleteRow(row)">
          <template #reference>
            <el-button
              :size="size"
              type="danger"
              link
            >
              {{ $t(`crud.delText`) }}
            </el-button>
          </template>
        </el-popconfirm>
      </template>
    </pro-crud>
    <el-dialog v-model="isDialogPermission" :title="permissionType===0?t(`system.role.menu_permissions_set`): t(`system.role.interface_permissions_set`)">
      <template v-if="permissionType === 0">
        <el-tree
          ref="menuTreeRef"
          node-key="uid"
          :props="treeDefaultProps"
          :default-checked-keys="menuCheckedKeys"
          :data="menuTrees"
          show-checkbox
        >
        </el-tree>
      </template>
      <template v-else>
        <el-tree
          ref="interfaceTreeRef"
          node-key="uid"
          :props="treeDefaultProps"
          :default-checked-keys="interfaceCheckedKeys"
          :data="InterfaceTrees"
          show-checkbox
        >
          <template #default="{ node, data }">
            <template v-for="(value, index) in splitString(node.label)" :key="index">
              <el-tag v-if="data.isFather" class="ml-1" :size="size" type="info">{{ value }}</el-tag>
              <el-tag v-else class="ml-1" :size="size" :type="getTagType(data.method)">{{ value }}</el-tag>
            </template>
          </template>
        </el-tree>
      </template>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="isDialogPermission = false">
            {{t(`system.role.permissions_cancel`)}}
          </el-button>
          <el-button type="primary" @click="handleSave">
            {{t(`system.role.permissions_save`)}}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </pro-card>
</template>
<style></style>