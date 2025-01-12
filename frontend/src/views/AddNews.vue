<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const title = ref('')
const content = ref('')
const imageUrl = ref('')
const detailsContent = ref('')
const isPublished = ref(false)
const submitError = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const newsList = ref([])
const currentPage = ref(1)
const pageSize = 10
const totalNews = ref(0)

const paginatedNews = computed(() => {
    const start = (currentPage.value - 1) * pageSize
    const end = currentPage.value * pageSize
    return newsList.value.slice(start, end)
})

const loadNews = async () => {
    try {
        const response = await axios.get('/api/news')
        if (response.data.status === 'success') {
            newsList.value = response.data.data
            totalNews.value = newsList.value.length
        }
    } catch (error) {
        console.error('加载新闻列表失败', error)
    }
}

const addNews = async () => {
    try {
        if (!title.value || !content.value) {
            submitError.value = true
            errorMessage.value = '请填写所有必填字段（标题、内容）'
            return
        }

        const token = localStorage.getItem('token')
        if (!token) {
            submitError.value = true
            errorMessage.value = '用户未登录，请先登录'
            return
        }

        const response = await axios.post(
            '/api/news/add',
            {
                title: title.value,
                content: content.value,
                image_url: imageUrl.value,
                details_content: detailsContent.value,
                is_published: isPublished.value
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        )

        if (response.data.status === 'success') {
            submitError.value = false
            successMessage.value = '新闻新增成功！'
            clearForm()
            loadNews()
        } else {
            submitError.value = true
            errorMessage.value = response.data.data.message || '新闻新增失败'
        }
    } catch (error) {
        submitError.value = true
        errorMessage.value = '发生错误，请稍后再试'
        console.error(error)
    }
}

const clearForm = () => {
    title.value = ''
    content.value = ''
    imageUrl.value = ''
    detailsContent.value = ''
    isPublished.value = false
}

const deleteNews = async (id) => {
    const token = localStorage.getItem('token')
    if (!token) {
        alert('用户未登录，请先登录')
        return
    }

    if (confirm('确定要删除这条新闻吗？')) {
        try {
            const response = await axios.delete(`/api/news/${id}`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })

            if (response.data.status === 'success') {
                alert('新闻删除成功！')
                loadNews()
            } else {
                alert(response.data.data.message || '删除失败')
            }
        } catch (error) {
            alert('发生错误，无法删除新闻')
            console.error(error)
        }
    }
}

const changePage = (page) => {
    if (page >= 1 && page <= Math.ceil(totalNews.value / pageSize)) {
        currentPage.value = page
    }
}

onMounted(() => {
    loadNews()
})
</script>

<template>
    <div class="container mt-5">
        <h2 class="mb-4">新增新闻</h2>
        <form @submit.prevent="addNews" class="needs-validation">
            <div class="mb-3">
                <label for="news-title" class="form-label">标题</label>
                <input v-model="title" type="text" class="form-control" id="news-title" placeholder="请输入新闻标题"
                    required />
            </div>
            <div class="mb-3">
                <label for="news-content" class="form-label">内容</label>
                <textarea v-model="content" class="form-control" id="news-content" rows="5" placeholder="请输入新闻内容"
                    required></textarea>
            </div>
            <div class="mb-3">
                <label for="news-image-url" class="form-label">图片 URL</label>
                <input v-model="imageUrl" type="text" class="form-control" id="news-image-url"
                    placeholder="请输入图片链接（可选）" />
            </div>
            <div class="mb-3">
                <label for="news-details-content" class="form-label">详细内容</label>
                <textarea v-model="detailsContent" class="form-control" id="news-details-content" rows="3"
                    placeholder="请输入详细内容（可选）"></textarea>
            </div>
            <div class="mb-3 form-check">
                <input v-model="isPublished" type="checkbox" class="form-check-input" id="news-is-published" />
                <label for="news-is-published" class="form-check-label">是否发布</label>
            </div>
            <div class="d-flex align-items-center">
                <button type="submit" class="btn btn-primary me-3">提交新闻</button>
                <button type="button" class="btn btn-secondary" @click="clearForm">重置表单</button>
            </div>
            <div v-if="submitError" class="alert alert-danger mt-3" role="alert">
                {{ errorMessage }}
            </div>
            <div v-if="successMessage" class="alert alert-success mt-3" role="alert">
                {{ successMessage }}
            </div>
        </form>

        <!-- 新闻管理列表 -->
        <h3 class="mt-5">新闻管理</h3>
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>#</th>
                    <th>标题</th>
                    <th>作者</th>
                    <th>发布时间</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="news in paginatedNews" :key="news.id">
                    <td>{{ news.id }}</td>
                    <td>{{ news.title }}</td>
                    <td>{{ news.author }}</td>
                    <td>{{ news.publish_date }}</td>
                    <td>
                        <button class="btn btn-danger btn-sm" @click="deleteNews(news.id)">
                            删除
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>

        <!-- 分页 -->
        <nav v-if="totalNews > pageSize" aria-label="Page navigation">
            <ul class="pagination">
                <li class="page-item" :class="{ disabled: currentPage === 1 }">
                    <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">
                        上一页
                    </a>
                </li>
                <li class="page-item" v-for="page in Math.ceil(totalNews / pageSize)" :key="page"
                    :class="{ active: currentPage === page }">
                    <a class="page-link" href="#" @click.prevent="changePage(page)">
                        {{ page }}
                    </a>
                </li>
                <li class="page-item" :class="{ disabled: currentPage === Math.ceil(totalNews / pageSize) }">
                    <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">
                        下一页
                    </a>
                </li>
            </ul>
        </nav>
    </div>
</template>

<style scoped>
.container {
    max-width: 720px;
    margin: auto;
}

.needs-validation > div {
    margin-top: 10px;
}

textarea {
    resize: none;
}

.table {
    margin-top: 20px;
}

.pagination {
    margin-top: 20px;
    justify-content: center;
}
</style>
