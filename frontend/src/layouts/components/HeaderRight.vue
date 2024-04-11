<script setup lang="ts">
import Lang from '@/layouts/components/Lang.vue'
import Avatar from '@/layouts/components/Avatar.vue'
import SwitchThemes from '@/layouts/components/SwitchThemes.vue'
</script>

<template>
  <div class="flex space-x-5 items-center ">
    <SwitchThemes />
    <Lang></Lang>
    <Avatar></Avatar>
  </div>
</template>