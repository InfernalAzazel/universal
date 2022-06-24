<template>
  <pro-layout class="docs-layout">
    <template #logo="{ collapse }" class="">
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
        <span class="ml-2.5 mt-2.5 font-sans text-2xl h-full">universal</span>
      </div>
    </template>
    <template #footer>
      <p class="flex justify-center">Copyright © 2022 kylin</p>
    </template>
    <template #header-left>
      <pro-breadcrumb separator=">"/>
    </template>
    <template #header-right>
      <span>header-right</span>
    </template>

    <template #header-bottom>
      <pro-tabs
          ref="childTabs"
          style="margin-bottom: 15px"
      />
    </template>

    <router-view>
      <template #default="{ Component, route }">
        <transition
            name="el-fade-in"
            mode="out-in"
            appear
        >
          <pro-card
              :key="route.fullPath"
              shadow="never"
          >
            <component :is="Component"/>
          </pro-card>
        </transition>
      </template>
    </router-view>
  </pro-layout>
</template>


<script setup lang="ts">
import {inject, shallowRef} from "vue";

const tabs = inject('tabs', undefined) // Get top-level `Tabs` inject
const childTabs = shallowRef({})
</script>
