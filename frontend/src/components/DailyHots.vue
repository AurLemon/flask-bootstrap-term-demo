<script setup>
import { ref } from 'vue'
import { useGlobalStore } from '../stores/global'
import { RouterLink } from 'vue-router'
import axios from 'axios'

const globalStore = useGlobalStore()
const dailyHots = ref([])
const recentRelease = ref([])

axios.get('/api/news/hot')
.then(response => {
    dailyHots.value = response.data.data.daily_hots
    recentRelease.value = response.data.data.recent_release    
})
.catch(error => {
    console.error('获取数据失败', error);
})
</script>

<template>
    <div class="daily-hots col-md-4">
        <div class="panel panel-default">
            <div class="panel-heading">
                <span class="bi bi-fire" aria-hidden="true"></span> 24小时热门推荐
            </div>
            <div class="panel-body">
                <RouterLink :to="`/news/${hot.id}`" v-for="hot in dailyHots" :key="hot.id">
                    {{ hot.title }} <span class="subtitle">({{ hot.view_count }})</span>
                </RouterLink>
            </div>
        </div>
        <div class="panel panel-default">
            <div class="panel-heading">
                <span class="bi bi-fire" aria-hidden="true"></span> 最新发布
            </div>
            <div class="panel-body">
                <RouterLink :to="`/news/${release.id}`" v-for="release in recentRelease" :key="release.id">
                    {{ release.title }} <span class="subtitle">({{ release.publish_date }})</span>
                </RouterLink>
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">
.panel-body {
    display: flex;
    flex-direction: column;
    gap: 4px;

    & > a {
        display: block;
    }

    &::before, &::after {
        content: none;
    }
}
</style>