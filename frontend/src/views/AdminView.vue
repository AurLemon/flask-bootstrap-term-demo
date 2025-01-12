<script setup>
import { ref, computed, watch } from 'vue'
import axios from 'axios'
import DailyHots from '@/components/DailyHots.vue'

const userList = ref([])
const filteredList = ref([])
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = 10
const isAddingUser = ref(false)
const newUser = ref({
    first_name: '',
    last_name: '',
    username: '',
    password: '',
    apply_status: 0,
    is_admin: false
})

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

const addUser = () => {
    const token = getToken();

    if (!token) {
        console.log('没有授权 token，无法添加');
        return;
    }

    axios.post('/api/user/add', newUser.value, {
        headers: { Authorization: `Bearer ${token}` }
    }).then(res => {
        if (res.data.status === 'success') {
            userList.value.push(res.data.data.user_info)
            filteredList.value = [...userList.value]
            isAddingUser.value = false
            newUser.value = {
                first_name: '',
                last_name: '',
                username: '',
                password: '',
                apply_status: 0,
                is_admin: false
            }
        } else {
            console.log('添加用户失败', res.data.message)
        }
    }).catch(err => {
        console.error('添加用户失败', err)
    })
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
                <div class="operation-form mb-3">
                    <a @click="isAddingUser = true" class="btn btn-success">新建</a>
                </div>
                <div class="search-form">
                    <form class="form-inline d-flex" @submit.prevent="updateSearch">
                        <input v-model="searchQuery" type="text" class="form-control me-2" placeholder="请输入关键字" />
                        <button type="submit" class="btn btn-default">搜索</button>
                    </form>
                </div>
                <div v-if="isAddingUser" class="add-user-form mb-3">
                    <h3 class="mb-4">新增用户</h3>
                    <form @submit.prevent="addUser" class="needs-validation">
                        <div class="row g-3">
                            <!-- 名字 -->
                            <div class="col-md-6">
                                <label for="first_name" class="form-label">名字</label>
                                <div class="input-group">
                                    <span class="input-group-text"><i class="bi bi-person"></i></span>
                                    <input id="first_name" v-model="newUser.first_name" type="text" class="form-control"
                                        placeholder="请输入名字" required />
                                </div>
                            </div>
                            <!-- 姓氏 -->
                            <div class="col-md-6">
                                <label for="last_name" class="form-label">姓氏</label>
                                <div class="input-group">
                                    <span class="input-group-text"><i class="bi bi-person"></i></span>
                                    <input id="last_name" v-model="newUser.last_name" type="text" class="form-control"
                                        placeholder="请输入姓氏" required />
                                </div>
                            </div>
                        </div>
                        <div class="row g-3 mt-3">
                            <!-- 用户名 -->
                            <div class="col-md-6">
                                <label for="username" class="form-label">用户名</label>
                                <div class="input-group">
                                    <span class="input-group-text"><i class="bi bi-person-circle"></i></span>
                                    <input id="username" v-model="newUser.username" type="text" class="form-control"
                                        placeholder="请输入用户名" required />
                                </div>
                            </div>
                            <!-- 密码 -->
                            <div class="col-md-6">
                                <label for="password" class="form-label">密码</label>
                                <div class="input-group">
                                    <span class="input-group-text"><i class="bi bi-lock"></i></span>
                                    <input id="password" v-model="newUser.password" type="password" class="form-control"
                                        placeholder="请输入密码" required />
                                </div>
                            </div>
                        </div>
                        <div class="row g-3 mt-3 end">
                            <!-- 申请状态 -->
                            <div class="col-md-6">
                                <label for="apply_status" class="form-label">申请状态</label>
                                <select id="apply_status" v-model="newUser.apply_status" class="form-select">
                                    <option value="0">未申请</option>
                                    <option value="1">已申请</option>
                                </select>
                            </div>
                            <!-- 是否为管理员 -->
                            <div class="col-md-6">
                                <label class="form-label d-block">是否为管理员</label>
                                <div class="form-check">
                                    <input id="is_admin" v-model="newUser.is_admin" type="checkbox"
                                        class="form-check-input" />
                                    <label for="is_admin" class="form-check-label">是</label>
                                </div>
                            </div>
                        </div>
                        <!-- 按钮 -->
                        <div class="mt-4">
                            <button type="submit" class="btn btn-primary me-2">提交</button>
                            <button type="button" @click="isAddingUser = false" class="btn btn-secondary">取消</button>
                        </div>
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
                                    <th scope="row" v-if="user.apply_status == 1">{{ user.id }}</th>
                                    <td v-if="user.apply_status == 1">{{ user.first_name }}</td>
                                    <td v-if="user.apply_status == 1">{{ user.last_name }}</td>
                                    <td v-if="user.apply_status == 1">@{{ user.username }}</td>
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
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;

    .add-user-form {
        flex: 1 1 100%;
        padding: 20px;
        margin-top: 20px;
        background: #f7f7f7;
        border-radius: 16px;

        .input-group {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .end {
            margin-top: 10px;

            & > .col-md-6 {
                display: flex;
                align-items: center;
                gap: 10px;

                .form-label, .form-check-label {
                    margin: 0;
                }
            }
        }

        .row.g-3 > .col-md-6 {
            margin-top: 10px;
        }

        h3 {
            margin: 0;
        }

        .mt-4 {
            margin-top: 12px;
        }
    }
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