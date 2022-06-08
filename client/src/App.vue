<template>
<a-config-provider :getPopupContainer="getPopupContainer">
  <router-view />
</a-config-provider>
</template>
<script lang="ts" setup>
const getPopupContainer = (el: Element, dialogContext: any) => {
  if (dialogContext) {
    return dialogContext.getDialogWrap();
  }
  return document.body;
};


</script>
<style>
#app {
  height: 100%;
}
</style>
