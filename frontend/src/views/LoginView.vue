<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const role = ref('普通用户')
const username = ref('')
const password = ref('')
const code = ref('')
const sms = ref('')
const loginError = ref(false)
const errorMessage = ref('')
const router = useRouter()

const login = async () => {
    try {
        const response = await axios.post('/api/login', {
            username: username.value,
            password: password.value
        })

        if (response.data.status === 'success') {
            const resToken = response.data.data.token
            localStorage.setItem('token', resToken)

            const infoRes = await axios.get("/api/user/info", {
                headers: {
                    Authorization: `Bearer ${resToken}`
                }
            })

            const userName = infoRes.data.data.username
            userStore.setUsername(userName)
            
            loginError.value = false
            router.push('/')
        } else {
            loginError.value = true
            errorMessage.value = response.data.data.message || '登录失败'
        }
    } catch (error) {
        loginError.value = true
        errorMessage.value = '发生错误，请稍后再试'
        console.error(error)
    }
}
const sendSmsCode = () => {
    alert('短信验证码已发送（此功能为界面展示，不实际发送）')
}
</script>

<template>
    <div class="page">
        <div class="login-container">
            <h2>用户登录</h2>
            <h5 class="text-center">测试账号：aurlemon / 密码：114514</h5>
            <form @submit.prevent="login">
                <div class="form-group">
                    <label for="role">角色</label>
                    <select v-model="role" class="form-control" id="role">
                        <option>普通用户</option>
                        <option>管理员</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="user">用户名</label>
                    <input v-model="username" type="text" class="form-control" id="user" placeholder="请输入用户名" />
                </div>

                <div class="form-group">
                    <label for="pwd">密码</label>
                    <input v-model="password" type="password" class="form-control" id="pwd" placeholder="请输入密码" />
                </div>

                <div class="form-group">
                    <label for="code">验证码</label>
                    <div class="row">
                        <div class="col-xs-7">
                            <input v-model="code" type="text" class="form-control" id="code" placeholder="请输入验证码" />
                        </div>
                        <div class="col-xs-5">
                            <img src="@/assets/images/captcha_test_image.png" style="width: 133px; height: 33px" />
                        </div>
                    </div>
                </div>

                <div class="form-group">
                    <label for="sms">短信验证码</label>
                    <div class="row">
                        <div class="col-xs-7">
                            <input v-model="sms" type="text" class="form-control" id="sms" placeholder="请输入短信验证码" />
                        </div>
                        <div class="col-xs-5">
                            <button type="button" class="btn btn-default btn-block" @click="sendSmsCode">发送验证码</button>
                        </div>
                    </div>
                </div>

                <div class="submit-wrapper">
                    <button type="submit" class="btn btn-primary">登录</button>
                    <div v-if="loginError" class="login-info">{{ errorMessage }}</div>
                </div>
            </form>
        </div>
    </div>
</template>

<style scoped lang="scss">
.page {
    margin: auto;
}

.login-container {
    margin: auto;
    padding: 20px;
    padding-bottom: 48px;
    max-width: 480px;

    h2 {
        text-align: center;
    }

    .sumbit-wrapper {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
        position: relative;
    }

    .login-info {
        position: absolute;
        top: calc(100% + 0.5rem);
        color: red;
    }

    .login-info {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
}
</style>
