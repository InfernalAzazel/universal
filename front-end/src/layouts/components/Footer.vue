<script setup lang="ts">
const currentYear: number = new Date().getFullYear();
</script>

<template>
  <p class="flex justify-center">{{`Copyright © 2022~${currentYear} kylin`}}</p>
</template>

<style scoped>

</style>