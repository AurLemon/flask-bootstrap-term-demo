<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

const userInfo = ref(null)
const loading = ref(true)
const error = ref(null)
const token = localStorage.getItem("token")

onMounted(async () => {
    if (token) {
        try {
            const response = await axios.get("/api/user/info", {
                headers: {
                    Authorization: `Bearer ${token}`
                },
            });

            if (response.data.status === "success") {
                userInfo.value = response.data.data
            } else {
                error.value = "无法获取用户信息"
            }
        } catch (err) {
            error.value = "请求失败，请稍后再试"
            console.error(err)
        }
    } else {
        error.value = "未登录，请先登录"
    }
    loading.value = false
});
</script>

<template>
    <div class="container mt-5">
        <div v-if="loading" class="text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">加载中...</span>
            </div>
        </div>

        <div v-if="error" class="alert alert-danger text-center" role="alert">
            {{ error }}
        </div>

        <div v-if="userInfo" class="card shadow-lg rounded-lg">
            <div class="card-header bg-primary text-white">
                <h3 class="mb-0">用户信息</h3>
            </div>
            <div class="card-body">
                <div class="row mb-3">
                    <div class="col-md-4">
                        <h5 class="text-muted">用户名</h5>
                        <p class="h5">{{ userInfo.username }}</p>
                    </div>
                    <div class="col-md-4">
                        <h5 class="text-muted">姓名</h5>
                        <p class="h5">{{ userInfo.first_name }} {{ userInfo.last_name }}</p>
                    </div>
                    <div class="col-md-4">
                        <h5 class="text-muted">注册日期</h5>
                        <p class="h5">{{ userInfo.reg_date }}</p>
                    </div>
                </div>

                <div class="row">
                    <div class="col-md-4">
                        <h5 class="text-muted">角色</h5>
                        <p class="h5">{{ userInfo.is_admin ? "管理员" : "普通用户" }}</p>
                    </div>
                    <div class="col-md-4">
                        <h5 class="text-muted">申请状态</h5>
                        <p class="h5">{{ userInfo.apply_status === "true" ? "已申请" : "未申请" }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">
@use '../assets/styles/media_screen.scss' as media;

.container {
    max-width: 960px;
    margin-top: 50px;
    padding: 0 20px;
}

.card {
    border-radius: 20px;
}

.card-header {
    color: white;
    padding: 20px;
    border-top-left-radius: 20px;
    border-top-right-radius: 20px;
    font-size: 24px;
    font-weight: 600;
}

.card-body {
    background-color: #f8f9fa;
    padding: 30px;
    border-bottom-left-radius: 20px;
    border-bottom-right-radius: 20px;
}

h5.text-muted {
    color: #6c757d;
    font-size: 16px;
}

.h5 {
    font-size: 20px;
    font-weight: 500;
}

.alert {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 30px;
    border-radius: 15px;
}

@include media.media-screen(phone) {
    .container {
        max-width: 100%;
    }

    .card-body {
        padding: 20px;
    }

    .card-header {
        font-size: 20px;
    }

    .h5 {
        font-size: 18px;
    }
}
</style>