<template>
  <div style="margin-right: 12px">
    <a-dropdown :trigger="['click']">
      <global-outlined />
      <template #overlay>
        <a-menu>
          <a-menu-item key="0">
            <a href="http://www.alipay.com/">
              <UserOutlined/>
              个人中心</a>
          </a-menu-item>
          <a-menu-item key="1">
            <a href="http://www.taobao.com/">
              <UserOutlined/>
              个人设置</a>
          </a-menu-item>
          <a-menu-divider/>
          <a-menu-item key="3">
            <UserOutlined/>
            退出登录
          </a-menu-item>
        </a-menu>
      </template>

    </a-dropdown>
  </div>
</template>

<script lang="ts" setup>
</script>

<style scoped>

</style>
