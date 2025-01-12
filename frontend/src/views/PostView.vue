<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const newContent = ref('')
const submitError = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const dataList = ref([])
const currentPage = ref(1)
const pageSize = 10

const paginatedList = computed(() => {
    const start = (currentPage.value - 1) * pageSize
    const end = currentPage.value * pageSize
    return dataList.value.slice(start, end)
})

const totalPages = computed(() => {
    return Math.ceil(dataList.value.length / pageSize)
})

const loadData = async () => {
    try {
        const response = await axios.get('/api/data')
        if (response.data.status === 'success') {
            dataList.value = response.data.data
        } else {
            console.error('加载数据失败：', response.data.message)
        }
    } catch (error) {
        console.error('加载数据失败：', error)
    }
}

const submitData = async () => {
    try {
        if (!newContent.value.trim()) {
            submitError.value = true
            errorMessage.value = '内容不能为空'
            return
        }

        const response = await axios.post('/api/data', { content: newContent.value })
        if (response.data.status === 'success') {
            successMessage.value = '数据提交成功！'
            newContent.value = ''
            loadData()
        } else {
            submitError.value = true
            errorMessage.value = response.data.message || '数据提交失败'
        }
    } catch (error) {
        submitError.value = true
        errorMessage.value = '发生错误，请稍后再试'
        console.error(error)
    }
}

const changePage = (page) => {
    if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
    }
}

onMounted(() => {
    loadData()
})
</script>

<template>
    <div class="container mt-5">
        <h2 class="mb-4">测试数据管理</h2>

        <!-- 提交数据 -->
        <div class="card mb-4">
            <div class="card-body">
                <h5 class="card-title">传输数据</h5>
                <form @submit.prevent="submitData" class="needs-validation">
                    <div class="form-group">
                        <label for="new-content">请输入内容</label>
                        <input v-model="newContent" type="text" class="form-control" id="new-content"
                            placeholder="输入字符串" />
                    </div>
                    <div class="mt-3">
                        <button type="submit" class="btn btn-primary">提交</button>
                    </div>
                </form>

                <!-- 提交成功和错误消息 -->
                <div v-if="successMessage" class="alert alert-success mt-3" role="alert">
                    {{ successMessage }}
                </div>
                <div v-if="submitError" class="alert alert-danger mt-3" role="alert">
                    {{ errorMessage }}
                </div>
            </div>
        </div>

        <!-- 查看数据列表 -->
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">查看数据</h5>
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>内容</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in paginatedList" :key="item.id">
                            <td>{{ item.id }}</td>
                            <td>{{ item.content }}</td>
                        </tr>
                    </tbody>
                </table>

                <!-- 分页 -->
                <nav v-if="totalPages > 1" aria-label="Page navigation">
                    <ul class="pagination justify-content-center">
                        <li class="page-item" :class="{ disabled: currentPage === 1 }">
                            <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">上一页</a>
                        </li>
                        <li class="page-item" v-for="page in totalPages" :key="page"
                            :class="{ active: currentPage === page }">
                            <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
                        </li>
                        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                            <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">下一页</a>
                        </li>
                    </ul>
                </nav>
            </div>
        </div>
    </div>
</template>

<style scoped>
.container {
    max-width: 800px;
    margin: auto;
}

.table {
    margin-top: 20px;
}

.pagination {
    margin-top: 20px;
}
</style>
