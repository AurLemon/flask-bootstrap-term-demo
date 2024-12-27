<template>
    <footer class="footer-info">
        <h3 class="title">
            联通新闻中心
            <span class="github">
                <a href="https://github.com/AurLemon/flask-bootstrap-term-demo" target="_blank">
                    <img src="../assets/images/GitHub_Logo.svg">
                </a>
            </span>
        </h3>
        <div class="info">
            <div class="name">© 2024 AurLemon (Lin Junle) Flask-Bootstrap Term Demo. All rights reserved.</div>
            <div class="register">
                <a href="https://beian.miit.gov.cn/" target="_blank">
                    ICP备案号：闽ICP备2023007345号-3
                </a>
            </div>
        </div>
    </footer>
</template>

<style scoped lang="scss">
.footer-info {
    padding: 2rem;
    margin-top: auto;
    background: #f9f9f9;

    .title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        line-height: 1;
    }

    .github {
        img {
            $length: 20px;
            display: block;
            width: $length;
            height: $length;
        }
    }

    .info {
        display: flex;
        justify-content: space-between;
    }
}
</style>