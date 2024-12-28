<script setup>
import { useGlobalStore } from './stores/global'
import NavComp from './components/NavComp.vue'
import FooterComp from './components/FooterComp.vue'

const globalStore = useGlobalStore()

const init = (() => {

})()
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