<script setup>
import { ref } from 'vue'

</script>

<template>
  <div class="page">
    <div class="container">
      <div style="margin: 10px 0">
        <a href="https://www.baidu.com" class="btn btn-success">新建</a>
        <a href="https://www.baidu.com" class="btn btn-im=info">批量导入</a>
        <a href="https://www.baidu.com" class="btn btn-warning">导出</a>
        <div style="float: right">
          <form class="form-inline">
            <div class="form-group">
              <input
                type="text"
                class="form-control"
                placeholder="请输入关键字"
              />
            </div>
            <button type="submit" class="btn btn-default">搜索</button>
          </form>
        </div>
      </div>
    </div>

    <div class="container" data-example-id="bordered-table">
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>#</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Username</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th scope="row">1</th>
            <td><a href="https://www.baidu.com">Mark</a></td>
            <td>Otto</td>
            <td>@mdo</td>
            <td>
              <a href="https://www.baidu.com" class="btn btn-primary btn-xs"
                >编辑</a
              >
              <a href="https://www.baidu.com" class="btn btn-danger btn-xs"
                >删除</a
              >
            </td>
          </tr>
          <tr>
            <th scope="row">2</th>
            <td><a href="https://www.baidu.com">Mark</a></td>
            <td>Thornton</td>
            <td>@fat</td>
            <td>
              <a href="https://www.baidu.com" class="btn btn-primary btn-xs"
                >编辑</a
              >
              <a href="https://www.baidu.com" class="btn btn-danger btn-xs"
                >删除</a
              >
            </td>
          </tr>
          <tr>
            <th scope="row">3</th>
            <td><a href="https://www.baidu.com">Mark</a></td>
            <td>the Bird</td>
            <td>@twitter</td>
            <td>
              <a href="https://www.baidu.com" class="btn btn-primary btn-xs"
                ><span
                  class="glyphicon glyphicon-edit"
                  aria-hidden="true"
                ></span
              ></a>
              <a href="https://www.baidu.com" class="btn btn-danger btn-xs"
                ><span
                  class="glyphicon glyphicon-trash"
                  aria-hidden="true"
                ></span
              ></a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="container clearfix">
      <div class="col-md-8">
        <div class="bs-example" data-example-id="table-within-panel">
          <div class="panel panel-default">
            <!-- Default panel contents -->
            <div class="panel-heading">最新申请列表</div>
            <div class="panel-body">
              <p>注意，最新24小时提交的数据，如有疑问请联系主管</p>
            </div>

            <!-- Table -->
            <table class="table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>First Name</th>
                  <th>Last Name</th>
                  <th>Username</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th scope="row">1</th>
                  <td>Mark</td>
                  <td>Otto</td>
                  <td>@mdo</td>
                </tr>
                <tr>
                  <th scope="row">2</th>
                  <td>Jacob</td>
                  <td>Thornton</td>
                  <td>@fat</td>
                </tr>
                <tr>
                  <th scope="row">3</th>
                  <td>Larry</td>
                  <td>the Bird</td>
                  <td>@twitter</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <ul class="pagination">
          <li class="disabled">
            <a href="#" aria-label="Previous"
              ><span aria-hidden="true">«</span></a
            >
          </li>
          <li class="active">
            <a href="#">1 <span class="sr-only">(current)</span></a>
          </li>
          <li><a href="#">2</a></li>
          <li><a href="#">3</a></li>
          <li><a href="#">4</a></li>
          <li><a href="#">5</a></li>
          <li>
            <a href="#" aria-label="Next"><span aria-hidden="true">»</span></a>
          </li>
        </ul>
      </div>
      <div class="col-md-4">
        <div class="panel panel-default">
          <div class="panel-heading">
            <span class="glyphicon glyphicon-fire" aria-hidden="true"></span
            >24小时热门推荐
          </div>
          <div class="panel-body">
            <a href="#" class=".a1">放假了</a>
          </div>
        </div>
        <div class="panel panel-default">
          <div class="panel-heading">
            <span class="glyphicon glyphicon-fire" aria-hidden="true"></span
            >24小时热门推荐
          </div>
          <div class="panel-body">
            <a href="#" class=".a1">放假了</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
