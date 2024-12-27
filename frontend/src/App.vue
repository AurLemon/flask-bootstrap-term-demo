<script setup>
import NavComp from './components/NavComp.vue'
import FooterComp from './components/FooterComp.vue'
</script>

<template>
  <nav class="navbar navbar-default">
    <NavComp />
  </nav>
  <main>
    <div class="main-page">
      <RouterView />
    </div>
    <FooterComp />
  </main>
</template>

<style scoped lang="scss">
main {
  flex: 1 0 100%;
  display: flex;
  flex-direction: column;
}
</style>