<script setup>
import { onMounted } from "vue"
import axios from "axios"
import { RouterLink } from "vue-router"
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const token = localStorage.getItem("token")

const userLogout = () => {
    userStore.setUsername("未登录")
    localStorage.removeItem("token")
}

onMounted(async () => {
    if (token) {
        try {
            const response = await axios.get("/api/user/info", {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })

            if (response.data.status === "success") {
                userStore.setUsername(response.data.data.username)
            } else {
                userStore.setUsername("未登录")
            }
        } catch (error) {
            console.error("获取用户信息失败", error)
            userStore.setUsername("未登录")
        }
    }
})
</script>

<template>
    <nav class="navbar navbar-default">
        <div class="container">
            <div class="navbar-header">
                <a class="navbar-brand" href="#">联通新闻中心</a>
            </div>

            <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                <ul class="nav navbar-nav">
                    <li>
                        <RouterLink to="/">博客</RouterLink>
                    </li>
                    <li>
                        <RouterLink to="/admin">管理</RouterLink>
                    </li>
                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true"
                            aria-expanded="false">
                            其它 <span class="caret"></span>
                        </a>
                        <ul class="dropdown-menu">
                            <li>
                                <RouterLink to="/upload">上传文件</RouterLink>
                            </li>
                            <li role="separator" class="divider"></li>
                            <li>
                                <RouterLink to="/thanks">鸣谢</RouterLink>
                            </li>
                        </ul>
                    </li>
                </ul>

                <ul class="nav navbar-nav navbar-right">
                    <li>
                        <RouterLink to="/login">登录</RouterLink>
                    </li>
                    <li class="developing">
                        <RouterLink to="/register">注册</RouterLink>
                    </li>
                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true"
                            aria-expanded="false">
                            {{ userStore.username }} <span class="caret"></span>
                        </a>
                        <ul class="dropdown-menu">
                            <li>
                                <RouterLink to="/user">个人信息</RouterLink>
                            </li>
                            <li class="developing">
                                <a>我的资料</a>
                            </li>
                            <li class="developing">
                                <a>重置密码</a>
                            </li>
                            <li role="separator" class="divider"></li>
                            <li @click="userLogout">
                                <a>退出登录</a>
                            </li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<style scoped lang="scss">
.navbar-brand {
    font-weight: bold;
}

.developing a {
    filter: grayscale(1) opacity(0.2);
    cursor: not-allowed;
}

.dropdown-menu {
    a {
        cursor: pointer;
    }
}
</style>
