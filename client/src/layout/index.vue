<template>
    <pro-layout
        :locale="locale"
        v-bind="layoutConf"
        v-model:openKeys="state.openKeys"
        v-model:collapsed="state.collapsed"
        v-model:selectedKeys="state.selectedKeys"
        :breadcrumb="{ routes: breadcrumb }"

    >
        <!--    <template #headerContentRender>-->
        <!--      <a :style="{ margin: '0 8px', fontSize: '20px' }" @click="handleCollapsed">-->
        <!--        <MenuUnfoldOutlined v-if="state.collapsed"/>-->
        <!--        <MenuFoldOutlined v-else/>-->
        <!--      </a>-->
        <!--    </template>-->
        <!-- custom right-content -->
        <!--    <template #rightContentRender>-->
        <!--      <Notice :count="0"/>-->
        <!--      <AvatarList name="kylin"/>-->
        <!--      <LangList/>-->
        <!--    </template>-->
        <template #footerRender>
            <div>
                <h5 class="flex justify-center text-yellow-500">Copyright © 2022 kylin</h5>
            </div>
        </template>
        <router-view></router-view>

    </pro-layout>
</template>


<script setup lang="ts">
import {computed, reactive, ref} from 'vue';
import {useRouter} from 'vue-router';
import {getMenuData, clearMenuItem} from '@ant-design-vue/pro-layout';
import AvatarList from '../components/AvatarList/index.vue'
import LangList from '../components/LangList/index.vue'
import Notice from '../components/Notice/index.vue'

const locale = (i18n: string) => i18n;
const router = useRouter();
const loading = ref(false);
const {menuData} = getMenuData(clearMenuItem(router.getRoutes()));

const handleCollapsed = () => {
    state.collapsed = !state.collapsed;
};
const breadcrumb = computed(() =>
    router.currentRoute.value.matched.concat().map(item => {
        return {
            path: item.path,
            breadcrumbName: item.meta.title || '',
        };
    }),
);
const state = reactive({
    collapsed: false,
    openKeys: [],
    selectedKeys: [],
})
const layoutConf = reactive({
    title: 'AdminTemplate',
    navTheme: 'light',
    layout: 'side',
    splitMenus: false,
    menuData,
    headerHeight: 48,
    //fixSiderbar: true,
     fixedHeader: true,
});
</script>
