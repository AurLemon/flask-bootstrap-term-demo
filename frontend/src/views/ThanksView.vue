<script setup>
import { ref } from 'vue'

const teamMember = ref([
    
])
</script>

<template>
    <div class="page">
        <div class="container mt-5">
            <div class="text-center mb-4">
                <h1>鸣谢</h1>
                <p class="lead">在此，我们特别感谢以下支持和帮助我们完成项目的个人与组织：</p>
            </div>

            <div class="row">
                <div class="col-md-4" v-for="member in teamMember">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">林俊乐</h5>
                            <p class="card-text">感谢张三在项目中的技术支持，帮助我们解决了多个技术难题。</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="text-center mt-5">
                <p class="lead">我们衷心感谢所有为本项目做出贡献的人！</p>
            </div>
        </div>
    </div>
</template>