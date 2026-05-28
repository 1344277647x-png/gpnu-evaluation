# GPnu 公选课教师评价系统

学生评价公选课老师教学质量的平台，学弟学妹选课参考利器。

## 技术栈

- **前端**: Vue 3 + Vite + Element Plus + ECharts + Pinia
- **后端**: Python Flask + SQLAlchemy + PyMySQL
- **数据库**: MySQL 8.0+
- **认证**: JWT (access + refresh token)

## 快速启动

### 1. 数据库

```bash
mysql -u root -p < backend/init_db.sql
```

默认管理员：`admin`，密码需通过 Python 生成 bcrypt 哈希后更新。

### 2. 后端

```bash
cd backend
pip install -r requirements.txt
python app.py
# 运行在 http://localhost:5000
```

### 3. 前端

```bash
cd frontend
npm install
npm run dev
# 运行在 http://localhost:5173
```

## 功能概览

| 功能 | 说明 |
|---|---|
| 课程广场 | 搜索、按分类/学期筛选、按评分/时间排序 |
| 课程详情 | 雷达图四维度评分、评价列表 |
| 提交评价 | 教学质量/课程内容/考核方式/给分公平度 四维度打分 |
| 提交新课 | 学生提交课程，管理员审核后上线 |
| 个人中心 | 修改信息、修改密码、我的评价、我的课程 |
| 管理面板 | 课程审核、用户管理、数据统计 |

## 项目结构

```
├── backend/           # Flask 后端
│   ├── app.py         # 入口
│   ├── models.py      # SQLAlchemy 模型
│   ├── auth.py        # 认证
│   ├── courses.py     # 课程
│   ├── reviews.py     # 评价
│   ├── teachers.py    # 教师
│   ├── categories.py  # 分类
│   ├── admin.py       # 管理
│   ├── my.py          # 个人中心
│   ├── utils.py       # 工具函数
│   ├── config.py      # 配置
│   └── init_db.sql    # 建表脚本
├── frontend/          # Vue 3 前端
│   └── src/
│       ├── views/     # 页面
│       ├── components/# 组件
│       ├── stores/    # Pinia 状态
│       ├── api/       # Axios
│       └── router/    # 路由
└── .env.example       # 环境变量模板
```
