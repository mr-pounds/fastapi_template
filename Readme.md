# FastAPI_Template

数据库依赖: [tortoise-orm](https://tortoise.github.io/index.html)

## FastAPI 的项目结构

```text
- db: sqlite files
- doc: related documents
- src: source code
.gitignore
conf.yaml
Pipfile
Pipfile.lock
Readme.md
```

## 源码结构

```text
- apps: 具体的业务模块逻辑
	- ...
- models：数据库的db实例及orm实现
- utils： 工具方法
constant.py： 全局使用的常量
dependencies.py： 接口的依赖方法
exception.py：全局的异常实现方法
main.py： 入口方法
response.py： response基础方法的封装
```
