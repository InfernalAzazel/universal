<template>
    <page-container
        :tab-list="tab.list"
        :tab-active-key="tab.activeKey"
        :on-tab-change="handleTabChange">
            <template #tags>
              <a-tag>tag1</a-tag>
              <a-tag color="pink">tag2</a-tag>
            </template>
            <a-button @click="handleClick">Button</a-button>
            <p v-for="item in new Array(20)" :key="item">text block...</p>

    </page-container>
</template>
<script lang="ts" setup>
import {reactive} from "vue";

const tab = reactive({
    list: [
        {tab: 'tab1', key: 'tab1'},
        {tab: 'tab2', key: 'tab2'},
        {tab: 'tab3', key: 'tab3'}
    ],
    activeKey : 'tab1'
})

const handleTabChange = (key: any) => {
    tab.activeKey = key
    console.log('PageHeader::tabChange', key)
}
</script>
<style></style>
