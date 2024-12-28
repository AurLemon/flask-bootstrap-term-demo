<template>
    <div class="page">
        <div class="login-container">
            <h2>用户注册</h2>
            <form>
                <div class="form-group">
                    <label for="role">角色</label>
                    <select multiple class="form-control" id="role">
                        <option>普通用户</option>
                        <option>管理员</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="user">用户名</label>
                    <input type="text" class="form-control" id="user" placeholder="请输入用户名" />
                </div>

                <div class="form-group">
                    <label for="pwd">密码</label>
                    <input type="password" class="form-control" id="pwd" placeholder="请输入密码" />
                </div>

                <div class="form-group">
                    <label for="code">验证码</label>
                    <div class="row">
                        <div class="col-xs-7">
                            <input type="password" class="form-control" id="code" placeholder="请输入验证码" />
                        </div>
                        <div class="col-xs-5">
                            <img style="width: 133px; height: 33px" />
                        </div>
                    </div>
                </div>

                <div class="form-group">
                    <label for="code">短信验证码</label>
                    <div class="row">
                        <div class="col-xs-7">
                            <input type="text" class="form-control" id="sms" placeholder="请输入短信验证码" />
                        </div>
                        <div class="col-xs-5">
                            <input type="button" class="btn btn-default btn-block" value="发送验证码" />
                        </div>
                    </div>
                </div>

                <div class="sumbit-wrapper">
                    <button type="submit" class="btn btn-primary">注册</button>
                    <div class="login-info">用户名或密码错误</div>
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
    }

    .login-info {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
}
</style>
