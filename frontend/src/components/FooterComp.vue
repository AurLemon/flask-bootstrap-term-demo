<template>
    <footer class="footer-info">
        <div class="footer-wrapper">
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
        </div>
    </footer>
</template>

<style scoped lang="scss">
@use '../assets/styles/media_screen.scss' as media;

.footer-info {
    margin-top: auto;
    background: #f9f9f9;

    .footer-wrapper {
        display: flex;
        flex-direction: column;
        padding: 1.75rem;
        padding-bottom: 3.75rem;
        width: media.$media-screen-value-pad;
        margin: 0 auto;

        @include media.media-screen(mobile) {
            width: 100%;
        }
    }

    .title {
        display: flex;
        align-items: center;
        gap: 1rem;
        line-height: 1;
    }

    .github {
        img {
            $length: 18px;
            display: block;
            width: $length;
            height: $length;
        }
    }

    .info {
        display: flex;
        justify-content: space-between;

        @include media.media-screen(mobile) {
            flex-direction: column;
        }
    }
}
</style>