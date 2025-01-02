<script setup>
import { RouterLink, RouterView } from "vue-router"
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
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">
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
                    <li>
                        <RouterLink to="/register">注册</RouterLink>
                    </li>
                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">
                            AurLemon <span class="caret"></span>
                        </a>
                        <ul class="dropdown-menu">
                            <li>
                                <a href="#">个人中心</a>
                            </li>
                            <li>
                                <a href="#">我的资料</a>
                            </li>
                            <li>
                                <a href="#">重置密码</a>
                            </li>
                            <li role="separator" class="divider"></li>
                            <li>
                                <a href="#">退出登录</a>
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
</style>
