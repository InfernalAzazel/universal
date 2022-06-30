<template>
  <pro-card>
    <template #header>
      <el-button-group class="">
        <el-button  icon="Document" />
        <el-button  icon="Refresh" />
      </el-button-group>
    </template>
    <el-tree
        :allow-drop="allowDrop"
        :allow-drag="allowDrag"
        :data="data"
        draggable
        default-expand-all
        node-key="id"
        @node-drag-start="handleDragStart"
        @node-drag-enter="handleDragEnter"
        @node-drag-leave="handleDragLeave"
        @node-drag-over="handleDragOver"
        @node-drag-end="handleDragEnd"
        @node-drop="handleDrop"
        :expand-on-click-node="false"
        class=""
    >
      <template #default="{ node, data }">
        <span class="custom-tree-node">
          <div>
            <el-icon @click="append(data)" :size="20">
               <component is="Edit"/>
             </el-icon>
            <span >
              {{ node.label }}
            </span>
            <el-tag class="ml-5">Tag 1</el-tag>
            <a class="ml-5" href="/admin">/admin</a>
          </div>
          <div>
             <el-icon class="hover:bg-blue-300" @click="append(data)" :size="20">
               <component is="Edit"/>
             </el-icon>
            <el-icon class="hover:bg-blue-300" @click="remove(node, data)" :size="20">
              <component is="Delete"/>
             </el-icon>
          </div>
        </span>
      </template>
    </el-tree>

  </pro-card>
</template>
<script lang="ts" setup>

import type Node from 'element-plus/es/components/tree/src/model/node'
import type {DragEvents} from 'element-plus/es/components/tree/src/model/useDragNode'
import type {DropType} from 'element-plus/es/components/tree/src/tree.type'


const defaultProps = {
  children: 'children',
  label: 'label',
  disabled: 'disabled',
}

const handleDragStart = (node: Node, ev: DragEvents) => {
  console.log('drag start', node)
}
const handleDragEnter = (
    draggingNode: Node,
    dropNode: Node,
    ev: DragEvents
) => {
  console.log('tree drag enter:', dropNode.label)
}
const handleDragLeave = (
    draggingNode: Node,
    dropNode: Node,
    ev: DragEvents
) => {
  console.log('tree drag leave:', dropNode.label)
}
const handleDragOver = (draggingNode: Node, dropNode: Node, ev: DragEvents) => {
  console.log('tree drag over:', dropNode.label)
}
const handleDragEnd = (
    draggingNode: Node,
    dropNode: Node,
    dropType: DropType,
    ev: DragEvents
) => {
  console.log('tree drag end:', dropNode && dropNode.label, dropType)
}
const handleDrop = (
    draggingNode: Node,
    dropNode: Node,
    dropType: DropType,
    ev: DragEvents
) => {
  console.log('tree drop:', dropNode.label, dropType)
}
const allowDrop = (draggingNode: Node, dropNode: Node, type: DropType) => {
  if (dropNode.data.label === 'Level two 3-1') {
    return type !== 'inner'
  } else {
    return true
  }
}
const allowDrag = (draggingNode: Node) => {
  return !draggingNode.data.label.includes('Level three 3-1-1')
}

let id = 1000
const append = (data: any) => {
  // const newChild = { id: id++, label: 'testtest', children: [] }
  // if (!data.children) {
  //   data.children = []
  // }
  // data.children.push(newChild)
  // dataSource.value = [...dataSource.value]
}

interface Tree {
  id: number
  label: string
  children?: Tree[]
}

const remove = (node: Node, data: Tree) => {
  // const parent = node.parent
  // const children: Tree[] = parent.data.children || parent.data
  // const index = children.findIndex((d) => d.id === data.id)
  // children.splice(index, 1)
  // dataSource.value = [...dataSource.value]
}

const data = [
  {
    label: 'Level one 1',
    children: [
      {
        label: 'Level two 1-1',
      },
    ],
  },
  {
    label: 'Level one 2',
    children: [
      {
        label: 'Level two 2-1',
      },
      {
        label: 'Level two 2-2',
        children: [
          {
            label: 'Level three 2-2-1',
          },
        ],
      },
    ],
  },
  {
    label: 'Level one 3',
    children: [
      {
        label: 'Level two 3-1',

      },
      {
        label: 'Level two 3-2',
      },
    ],
  },
]

</script>
<style>

.custom-tree-node {
  @apply flex flex-1 items-center justify-between;
  @apply text-sm;
}




</style>