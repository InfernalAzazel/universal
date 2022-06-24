<template>
  <a-card>
    <a-tree
        v-model:expandedKeys="expandedKeys"
        v-model:checkedKeys="checkedKeys"
        :tree-data="treeData"
        :selectable="false"
        blockNode
    >
      <template #title="{ title, key }" >
        <a-row :gutter="[24, 4]" class="border-8 border-indigo-600 border-black bg-white">
          <a-col :md="20" :sm="12">
            <span class="node-title" >{{ title }} </span>
          </a-col>
          <a-col :md="4" :sm="12">
            <a-space>
              <a-button shape="circle">
                <template #icon><form-outlined /></template>
              </a-button>
              <a-button shape="circle">
                <template #icon><delete-outlined /></template>
              </a-button>
            </a-space>
          </a-col>
        </a-row>
      </template>
<!--      <template #switcherIcon>-->
<!--        <div class="border-2 border-red-500 ">-->
<!--                  <a-row>-->
<!--                    <a-col :span="20">-->
<!--                      <span class="node-title" >{{ title }} </span>-->
<!--                    </a-col>-->
<!--                    <a-col :span="4">-->
<!--                      <a-button type="text" shape="circle">-->
<!--                        <template #icon><SearchOutlined /></template>-->
<!--                      </a-button>-->
<!--                    </a-col>-->
<!--                  </a-row>-->
<!--        </div>-->
<!--      </template>-->

    </a-tree>
  </a-card>
</template>
<script lang="ts" setup>
import { defineComponent, ref, watch } from 'vue';
import type {
  AntTreeNodeDragEnterEvent,
  AntTreeNodeDropEvent,
  DataNode,
  TreeDataItem,
  TreeProps,
} from 'ant-design-vue/es/tree';

const treeData: TreeProps['treeData'] = [
  {
    title: 'parent 1',
    key: '0-0',
    scopedSlots: { title: "custom" },
    children: [
      {
        title: 'parent 1-0',
        key: '0-0-0',
        scopedSlots: { title: "custom" },
        children: [
          { title: 'leaf', key: '0-0-0-0', disableCheckbox: true },
          { title: 'leaf', key: '0-0-0-1' },
        ],
      },
      {
        title: 'parent 1-1',
        key: '0-0-1',
        children: [{ key: '0-0-1-0', title: 'sss' }],
      },
    ],
  },
];
const expandedKeys = ref<string[]>(['0-0-0', '0-0-1']);
const selectedKeys = ref<string[]>(['0-0-0', '0-0-1']);
const checkedKeys = ref<string[]>(['0-0-0', '0-0-1']);
watch(expandedKeys, () => {
  console.log('expandedKeys', expandedKeys);
});
watch(selectedKeys, () => {
  console.log('selectedKeys', selectedKeys);
});
watch(checkedKeys, () => {
  console.log('checkedKeys', checkedKeys);
});
</script>
<style></style>