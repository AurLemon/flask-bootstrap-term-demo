<script setup>
import NavComp from './components/NavComp.vue'
import FooterComp from './components/FooterComp.vue'
</script>

<template>
    <NavComp />
    <div class="main-content">
        <main>
            <RouterView />
        </main>
        <FooterComp />
    </div>
</template>

<style scoped lang="scss">
.main-content {
    flex: 1 0 100%;
    display: flex;
    flex-direction: column;

    main {
        display: flex;
        flex-direction: column;
        min-height: 75vh;
    }
}
</style>