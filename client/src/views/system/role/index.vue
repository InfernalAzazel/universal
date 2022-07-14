<template>
  <pro-card>
    <pro-crud
        v-model="form"
        v-model:search="serachForm"
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
        @delete="deleteRow"
        :table-columns="tableColumns"
        :rules="rules"
        layout="total, ->, jumper, prev, pager, next, sizes"
        border
        stripe
    >
      <template #action>
        <pro-column-setting
            v-model="tableColumns"
        />
      </template>
      <template #menu="{row, size }">
        <el-button
            :size="size"
            type="success"
            link
            @click="openDrawer(row)"
        >
          设置权限
        </el-button>
      </template>
    </pro-crud>
    <el-drawer v-model="drawer" direction="rtl">
      <template #title>
        <h2>权限设置</h2>
      </template>
      <template #default>
        <el-tabs type="border-card">
          <el-tab-pane label="角色菜单">
            <div class="relative w-full h-10">
              <el-button class="absolute top-0 right-0" type="primary" @click="handleMenuTreeOK">确定</el-button>
            </div>
            <el-tree
                ref="menuTreeRef"
                :data="menuTreeData"
                show-checkbox
                :default-checked-keys="menuCheckedKeys"
                node-key="id"
                :props="menuDefaultProps"
            />
          </el-tab-pane>
          <el-tab-pane label="角色接口">
            <div class="relative w-full h-10">
              <el-button class="absolute top-0 right-0" type="primary" @click="handleInterfaceTreeOK">确定</el-button>
            </div>
            <el-tree
                ref="interfaceTreeRef"
                :data="interfaceTreeData"
                show-checkbox
                :default-checked-keys="interfaceCheckedKeys"
                node-key="id"
                :props="interfaceDefaultProps"
            />
          </el-tab-pane>
        </el-tabs>
      </template>
    </el-drawer>
  </pro-card>

</template>
<script lang="ts" setup>
import {ref, markRaw} from 'vue'
import {useGlobalState, useGet, usePost, usePut, useDelete} from '../../../composables'
import RichEditor from '../../../components/RichEditor/index.vue'
import {ElMessage, ElTree} from 'element-plus'
import {
  defineCrudColumns,
  defineCrudMenuColumns,
} from 'element-pro-components'
import {Api} from "../../../utils";
import {useCrud, useList} from "../../../composables/crud";

interface Role {
  id: string
  key: string
  name: string
  description: string
  menu_nodes: any
  interface_nodes: any
}

const menu = defineCrudMenuColumns({
  label: 'Operations',
  addText: 'New',
  detailText: '详细',
  editText: '编辑',
  delText: '删除',
  searchText: 'Search',
  searchResetText: 'Reset Search',
  submitText: '提交',
  resetText: 'Reset Form',
  detail: true,
  edit: true,
  del: true,
  searchReset: true,
  // detailProps: { type: 'success', plain: false },
  // editProps: { type: 'default', plain: true },
  // delProps: { type: 'info', plain: true },
})
const drawer = ref(false)
// 当前
const currentRoleRow = ref<Role>({
  id: '',
  key: '',
  name: '',
  description: '',
  menu_nodes: [],
  interface_nodes: [],
})
const menuCheckedKeys = ref<string[]>([])
const interfaceCheckedKeys = ref<string[]>([])
const columns = defineCrudColumns([
  {
    label: 'ID',
    prop: 'id',
    component: 'el-input',
    hide: true,
    detail: true,
    props: {
      disabled: true
    }
  },
  {
    label: '角色ID',
    prop: 'key',
    component: 'el-input',
    form: true,
    search: true,
    detail: true,
  },
  {
    label: '角色名称',
    prop: 'name',
    component: 'el-input',
    form: true,
    search: true,
    detail: true,
  },
  {
    label: '描述',
    prop: 'description',
    component: 'el-input',
    props: {
      type: 'textarea',
      rows: 14,
      minRows: 12,
      maxRows: 24,
    },
    form: true,
    detail: true,
  },
])
const tableColumns = ref(JSON.parse(JSON.stringify(columns)))
const menuTreeRef = ref<InstanceType<typeof ElTree>>()
const menuDefaultProps = {
  children: 'children',
  label: 'title',
}
const interfaceTreeRef = ref<InstanceType<typeof ElTree>>()
const interfaceDefaultProps = {
  children: 'children',
  label: 'describe',
}
const rules = {
  key: {required: true, message: '请输入角色ID', trigger: 'blur'},
  name: {required: true, message: '请输入角色名称', trigger: 'blur'},
  description: {required: true, message: '请输入描述内容', trigger: 'blur'},
}


const {
  list: menuTreeData,
  serachForm: searchMenuForm,
  loadList: exeMenuList,
} = useList(Api.menuList)
const {
  data: interfaceTreeData,
  execute: exeInterfaceGroup,
} = useGet(Api.interfaceGroup)
const {execute: exeRoleMenuNodesEdit} = usePut(Api.roleEdit, currentRoleRow)

searchMenuForm.value.page_size = 1000000

const {
  form,
  serachForm,
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
} = useCrud(Api.roleList, Api.roleAdd, Api.roleEdit, Api.roleDelete, true)


// 抽屉
const openDrawer = (row: any) => {
  drawer.value = true
  currentRoleRow.value = row
  // 更新菜单Tree
  exeMenuList()
  // 添加菜单Tree状态
  menuCheckedKeys.value = []
  currentRoleRow.value.menu_nodes.forEach((item: { id: any }) => {
    menuCheckedKeys.value.push(item.id)
  })

  // 更新接口Tree
  exeInterfaceGroup()
  // 添加接口Tree状态
  interfaceCheckedKeys.value = []
  currentRoleRow.value.interface_nodes.forEach((item: { id: any }) => {
    interfaceCheckedKeys.value.push(item.id)
  })
}

// 处理菜单提交
const handleMenuTreeOK = () => {
  currentRoleRow.value.menu_nodes = menuTreeRef.value?.getCheckedNodes()
  exeRoleMenuNodesEdit()
}

// 处理接口提交
const handleInterfaceTreeOK = () => {
  currentRoleRow.value.interface_nodes = interfaceTreeRef.value?.getCheckedNodes()
  exeRoleMenuNodesEdit()
}



</script>
<style></style>