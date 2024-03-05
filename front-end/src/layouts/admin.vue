<script setup lang="ts">
import Logo from '@/layouts/components/Logo.vue'
import HeaderBottom from '@/layouts/components/HeaderBottom.vue'
import HeaderLeft from '@/layouts/components/HeaderLeft.vue'
import HeaderRight from '@/layouts/components/HeaderRight.vue'
import Footer from '@/layouts/components/Footer.vue'
</script>

<template>
  <pro-layout
    transition="el-fade-in"
    keep-alive
    :include="/^Keep/"
  >
    <template #logo="{ collapse }">
      <Logo :collapse="collapse" />
    </template>
    <template #header-bottom>
      <HeaderBottom />
    </template>
    <template #header-left>
      <HeaderLeft />
    </template>
    <template #header-right>
      <HeaderRight />
    </template>
    <template #footer>
     <Footer />
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
            :ghost="true"
          >
            <component :is="Component" />
          </pro-card>
        </transition>
      </template>
    </router-view>
  </pro-layout>
</template>