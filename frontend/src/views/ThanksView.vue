<script setup>
import { ref } from 'vue'

const teamMember = ref([
    {
        name: '林俊乐',
        description: '负责前端 + 后端的所有逻辑和编写。'
    },
    {
        name: '陈波',
        description: '负责讨论基本功能的设计。'
    },
    {
        name: '赵腾驹',
        description: '负责外围设计。'
    }
])
</script>

<template>
    <div class="page">
        <div class="container mt-5">
            <div class="text-center mb-4">
                <h1>鸣谢</h1>
                <p class="lead">本项目的团队由以下几位组成并完成任务</p>
            </div>

            <div class="row">
                <div class="col-md-4" v-for="member in teamMember">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">{{ member.name }}</h5>
                            <p class="card-text">{{ member.description }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="text-center mt-5">
                <p class="lead">项目主要以轻便快速部署为主🌹👍</p>
            </div>
        </div>
    </div>
</template>