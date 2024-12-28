<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const newsId = route.params.id

const newsData = ref(null)
const errorMessage = ref('')

onMounted(() => {
    axios.get(`/api/news/${newsId}`)
    .then(response => {
        if (response.data.status === 'success' && response.data.data) {
            newsData.value = response.data.data
        } else {
            errorMessage.value = response.data.data.message || '新闻不存在'
        }
    })
    .catch(error => {
        errorMessage.value = '加载新闻失败，请稍后再试'
        console.error(error)
    })
})
</script>

<template>
    <div class="container mt-4">
        <div v-if="errorMessage" class="alert alert-danger" role="alert">
            {{ errorMessage }}
        </div>

        <div v-else-if="newsData" class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">{{ newsData.title }}</h3>
            </div>
            <div class="panel-body">
                <div v-if="newsData.image_url">
                    <img :src="newsData.image_url" alt="News Image" class="img-fluid mb-3" />
                </div>
                <p><strong>作者：</strong> {{ newsData.author }}</p>
                <p><strong>发布时间：</strong> {{ newsData.publish_date }}</p>
                <p><strong>查看次数：</strong> {{ newsData.view_count }}</p>
                <p><strong>内容：</strong> {{ newsData.content }}</p>

                <p class="details">{{ newsData.details_content }}</p>
            </div>
        </div>

        <div v-else>
            <p>正在加载新闻详情...</p>
        </div>
    </div>
</template>

<style scoped lang="scss">
.details {
    font-size: 16px;
    margin-top: 1rem;
}
</style>
