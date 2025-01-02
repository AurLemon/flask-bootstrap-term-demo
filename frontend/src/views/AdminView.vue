<script setup>
import { ref, computed, watch } from 'vue'
import axios from 'axios'
import DailyHots from '@/components/DailyHots.vue'

const userList = ref([])
const filteredList = ref([])
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = 10

axios.get('/api/users').then(res => {
    userList.value = res.data.data
    filteredList.value = userList.value
})

const paginatedList = computed(() => {
    const start = (currentPage.value - 1) * pageSize
    const end = currentPage.value * pageSize
    return filteredList.value.slice(start, end)
})

const totalPages = computed(() => {
    return Math.ceil(filteredList.value.length / pageSize)
})

const updateSearch = () => {
    if (searchQuery.value.trim() === '') {
        filteredList.value = userList.value
    } else {
        filteredList.value = userList.value.filter(user => {
            return (
                user.first_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                user.last_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                user.username.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                user.id.toString().includes(searchQuery.value)
            )
        })
    }
    currentPage.value = 1
}

const changePage = (page) => {
    if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
    }
}

const getToken = () => {
    return localStorage.getItem('token');
}

const editUser = (id) => {
    const user = userList.value.find(u => u.id === id);
    const token = getToken();
    
    if (!token) {
        console.log('没有授权 token，无法编辑');
        return;
    }

    if (user.isEditing) {
        saveUser(id, {
            first_name: user.first_name,
            last_name: user.last_name,
            username: user.username
        });
    } else {
        user.isEditing = !user.isEditing;
    }
}

const saveUser = (id, userData) => {
    const token = getToken();
    
    if (!token) {
        console.log('没有授权 token，无法保存');
        return;
    }

    axios.put(`/api/user/${id}`, userData, {
        headers: { Authorization: `Bearer ${token}` }
    })
        .then(res => {
            if (res.data.status === 'success') {
                const user = userList.value.find(u => u.id === id);
                Object.assign(user, userData);
                user.isEditing = false;
            } else {
                console.log('保存用户失败', res.data.message);
            }
        })
        .catch(err => {
            console.error('保存用户失败', err);
        });
}

const deleteUser = (id) => {
    const token = getToken();
    
    if (!token) {
        console.log('没有授权 token，无法删除');
        return;
    }

    axios.delete(`/api/user/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
    })
        .then(res => {
            if (res.data.status === 'success') {
                userList.value = userList.value.filter(user => user.id !== id);
                filteredList.value = [...userList.value];
            } else {
                console.log('删除用户失败', res.data.message);
            }
        })
        .catch(err => {
            console.error('删除用户失败', err);
        });
}

watch(searchQuery, updateSearch)
</script>

<template>
    <div class="page">
        <div class="container">
            <div class="container-inner">
                <div class="operation-form">
                    <a href="https://www.baidu.com" class="btn btn-success">新建</a>
                    <a href="https://www.baidu.com" class="btn btn-info">批量导入</a>
                    <a href="https://www.baidu.com" class="btn btn-warning">导出</a>
                </div>
                <div class="search-form">
                    <form class="form-inline" @submit.prevent="updateSearch">
                        <div class="form-group">
                            <input v-model="searchQuery" type="text" class="form-control" placeholder="请输入关键字" />
                        </div>
                        <button type="submit" class="btn btn-default">搜索</button>
                    </form>
                </div>
            </div>
        </div>

        <div class="container" data-example-id="bordered-table">
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>名字</th>
                        <th>姓氏</th>
                        <th>用户名</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in paginatedList" :key="user.id">
                        <th scope="row">{{ user.id }}</th>
                        <td>
                            <template v-if="user.isEditing">
                                <input v-model="user.first_name" type="text" />
                            </template>
                            <template v-else>{{ user.first_name }}</template>
                        </td>
                        <td>
                            <template v-if="user.isEditing">
                                <input v-model="user.last_name" type="text" />
                            </template>
                            <template v-else>{{ user.last_name }}</template>
                        </td>
                        <td>
                            <template v-if="user.isEditing">
                                <input v-model="user.username" type="text" />
                            </template>
                            <template v-else>@{{ user.username }}</template>
                        </td>
                        <td class="split">
                            <a class="btn btn-primary btn-xs" @click="editUser(user.id)">
                                <span class="bi bi-pen" aria-hidden="true"></span>
                                {{ user.isEditing ? '保存' : '编辑' }}
                            </a>
                            <a class="btn btn-danger btn-xs" @click="deleteUser(user.id)">
                                <span class="bi bi-trash" aria-hidden="true"></span> 删除
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="container clearfix">
            <div class="col-md-8">
                <div class="bs-example" data-example-id="table-within-panel">
                    <div class="panel panel-default">
                        <div class="panel-heading">最新申请列表</div>
                        <div class="panel-body">注意，最新24小时提交的数据，如有疑问请联系主管</div>
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>名字</th>
                                    <th>姓氏</th>
                                    <th>用户名</th>
                                </tr>
                            </thead>
                            <tbody v-if="userList && userList.length > 0">
                                <tr v-for="user in userList" :key="user.id">
                                    <th scope="row" v-if="user.apply_status === 'true'">{{ user.id }}</th>
                                    <td v-if="user.apply_status === 'true'">{{ user.first_name }}</td>
                                    <td v-if="user.apply_status === 'true'">{{ user.last_name }}</td>
                                    <td v-if="user.apply_status === 'true'">@{{ user.username }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <ul class="pagination">
                    <li :class="{ disabled: currentPage === 1 }">
                        <a href="#" aria-label="Previous" @click.prevent="changePage(currentPage - 1)">
                            <span aria-hidden="true">«</span>
                        </a>
                    </li>
                    <li v-for="page in totalPages" :key="page" :class="{ active: currentPage === page }">
                        <a href="#" @click.prevent="changePage(page)">{{ page }}</a>
                    </li>
                    <li :class="{ disabled: currentPage === totalPages }">
                        <a href="#" aria-label="Next" @click.prevent="changePage(currentPage + 1)">
                            <span aria-hidden="true">»</span>
                        </a>
                    </li>
                </ul>
            </div>
            <DailyHots />
        </div>
    </div>
</template>


<style scoped lang="scss">
.container-inner {
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
}

.operation-form,
.form-inline {
    display: flex;
    gap: 3px;
}

.split {
    display: flex;
    flex-wrap: wrap;
    gap: 3px;
}

td input {
    width: 150px;
    padding: 2px 10px;
    border: 1px solid #dedede;
    border-radius: 4px;
    outline: none;
}
</style>