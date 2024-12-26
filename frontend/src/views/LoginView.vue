<script setup>
</script>

<template>
  <div class="page">
     <h2>用户登录</h2>

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
        <input type="text" class="form-control" id="user" placeholder="请输入用户名">
      </div>

      <div class="form-group">
        <label for="pwd">密码</label>
        <input type="password" class="form-control" id="pwd" placeholder="请输入密码">
      </div>

      <div class="form-group">
        <label for="code">验证码</label>
        <div class="row">
          <div class="col-xs-7">
            <input type="password" class="form-control" id="code" placeholder="请输入验证码">
          </div>
          <div class="col-xs-5">
            <img src="R-C.jpg" style="width: 133px; height: 33px;">
          </div>
          
        </div>
        
      </div>
      <div class="form-group">
        <label for="code">短信验证码</label>
        <div class="row">
          <div class="col-xs-7">
            <input type="text" class="form-control" id="sms" placeholder="请输入短信验证码">
          </div>
          <div class="col-xs-5">
           <input type="button" class="btn btn-default btn-block" value="发送验证码"  disabled="disabled">
          </div>
          
        </div>
        
      </div>
      <button type="submit" class="btn btn-primary">登  录</button>
      <span style="color: red;">用户名或密码错误</span>
    </form>
  </div>
</template>
