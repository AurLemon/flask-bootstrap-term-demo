# flask-bootstrap-term-demo
学校期末前特有的实训周，实训课的大作业 ~~（水的）~~，按着[这个教程](https://www.bilibili.com/video/BV1y1kjYvEsH/)来弄的，写的快的话半小时差不多。

Flask + Bootstrap，把路由写好就差不多。

~~（一开始还以为 Django，没想到是 Flask，其实自己更想用 Nest 写）~~

## 食用教程
0. **克隆仓库和安装运行环境。** 使用 `git clone https://github.com/AurLemon/flask-bootstrap-term-demo.git` 从 GitHub 克隆仓库。确保安装好 Python 3 和 pip。

1. **配置依赖包和虚拟环境。** 项目提供好了初始化脚本，在 Linux 下，切换到项目目录下以后，执行 `chmod +x init.sh` 赋予脚本执行权限后，继续执行 `./init.sh` 开始初始化；若在 Windows 下，双击打开 init.bat。

2. **安装成功后，根据系统环境激活虚拟环境** 。Linux 使用 `source .venv/bin/activate`；Windows 使用 `call .venv\Scripts\activate.bat`。激活成功后终端主机名前会出现 `(.venv)` 前缀。

3. **在虚拟环境下启动服务。** 使用 `python app.py` 启动服务。出现以下信息代表成功：
```shell
(.venv) root@aurlemon-sh3:/home/project_workspace/flask-bootstrap-term-demo# python app.py
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 123-053-804
```
打开浏览器，访问 `http://127.0.0.1:5000` 即可。如果需要停止服务，按 Ctrl+C（^C 信号）后即可终止。输入 `deactivate` 退出虚拟环境，退出后前缀 `(.venv)` 会消失。

## TODO List
- [x] 路由
    - [x] Blog
    - [x] Login
    - [x] Admin
- [x] 模板
    - [ ] Index
- [x] 部署脚本