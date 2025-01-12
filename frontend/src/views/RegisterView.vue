<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const firstName = ref('')
const lastName = ref('')
const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const applyStatus = ref(0)
const isAdmin = ref(false)
const registerError = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const register = async () => {
    try {
        if (password.value !== confirmPassword.value) {
            registerError.value = true
            errorMessage.value = '密码和确认密码不一致'
            return
        }

        const response = await axios.post('/api/register', {
            first_name: firstName.value,
            last_name: lastName.value,
            username: username.value,
            password: password.value,
            apply_status: applyStatus.value,
            is_admin: isAdmin.value
        })

        if (response.data.status === 'success') {
            registerError.value = false
            successMessage.value = '注册成功！即将跳转到登录页面...'

            setTimeout(() => {
                router.push('/login')
            }, 2000)
        } else {
            registerError.value = true
            errorMessage.value = response.data.data.message || '注册失败'
        }
    } catch (error) {
        registerError.value = true
        errorMessage.value = '发生错误，请稍后再试'
        console.error(error)
    }
}
</script>

<template>
    <div class="page">
        <div class="register-container">
            <h2>用户注册</h2>
            <form @submit.prevent="register">
                <div class="row">
                    <div class="col-md-6">
                        <div class="form-group">
                            <label for="first_name">名字</label>
                            <input v-model="firstName" type="text" class="form-control" id="first_name"
                                placeholder="请输入名字" required />
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-group">
                            <label for="last_name">姓氏</label>
                            <input v-model="lastName" type="text" class="form-control" id="last_name"
                                placeholder="请输入姓氏" required />
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="col-md-12">
                        <div class="form-group">
                            <label for="username">用户名</label>
                            <input v-model="username" type="text" class="form-control" id="username"
                                placeholder="请输入用户名" required />
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="col-md-6">
                        <div class="form-group">
                            <label for="password">密码</label>
                            <input v-model="password" type="password" class="form-control" id="password"
                                placeholder="请输入密码" required />
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-group">
                            <label for="confirm_password">确认密码</label>
                            <input v-model="confirmPassword" type="password" class="form-control" id="confirm_password"
                                placeholder="请再次输入密码" required />
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="col-md-6">
                        <div class="form-group">
                            <label for="apply_status">申请状态</label>
                            <select v-model="applyStatus" class="form-control" id="apply_status">
                                <option value="0">未申请</option>
                                <option value="1">已申请</option>
                            </select>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-group">
                            <label for="is_admin">是否为管理员</label>
                            <div class="form-check">
                                <input v-model="isAdmin" type="checkbox" class="form-check-input" id="is_admin" />
                                <label class="form-check-label" for="is_admin">
                                    管理员
                                </label>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="submit-wrapper">
                    <button type="submit" class="btn btn-primary">注册</button>
                </div>

                <div v-if="registerError" class="register-info error">
                    {{ errorMessage }}
                </div>

                <div v-if="successMessage" class="register-info success">
                    {{ successMessage }}
                </div>
            </form>
        </div>
    </div>
</template>

<style scoped lang="scss">
.page {
    margin: auto;
}

.register-container {
    margin: auto;
    padding: 20px;
    padding-bottom: 48px;
    max-width: 720px;

    h2 {
        text-align: center;
    }

    .submit-wrapper {
        margin-top: 20px;
    }

    .register-info {
        margin-top: 15px;
        text-align: center;
        font-size: 14px;
    }

    .error {
        color: red;
    }

    .success {
        color: green;
    }

    @media (max-width: 768px) {
        .row {
            flex-direction: column;
        }
    }
}
</style>
