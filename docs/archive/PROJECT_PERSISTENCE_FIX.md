# 项目数据持久化修复说明

**日期**: 2026-03-30

---

## 问题现象

用户创建并保存的项目，在 Docker 更新、重建镜像或替换容器后丢失，需要重新创建。

---

## 根因

项目管理原实现将项目数据写入相对目录：

- `projects/`
- `exports/`

在 Docker 容器内，这两个目录位于镜像工作目录 `/app` 下，但并未挂载到 NAS 持久化目录。
因此只要容器重建，项目文件和导出文件就会随着容器层一起消失。

---

## 修复方案

新增统一运行时数据目录机制：

- 环境变量：`AINOVEL_DATA_DIR`
- 默认 Docker 目录：`/app/data`

项目与导出路径调整为：

- 项目目录：`/app/data/projects`
- 导出目录：`/app/data/exports`

同时，应用启动时会自动尝试迁移旧版 `projects/` 目录中的项目数据：

- 已存在于新目录中的文件不会被覆盖
- 不会删除旧目录，仅复制缺失内容

---

## 效果

修复后，只要 NAS 上 `/share/CACHEDEV1_DATA/Container/ainovel/data` 保留：

- 项目列表不会因容器重建而丢失
- 项目章节内容不会因更新镜像而丢失
- 导出文件也会保留在持久化目录中

---

## 运维建议

1. 更新代码并重建容器
2. 首次启动后检查：
   - `/share/CACHEDEV1_DATA/Container/ainovel/data/projects/`
   - `/share/CACHEDEV1_DATA/Container/ainovel/data/exports/`
3. 如果旧容器里曾保存过项目，确认启动日志中是否出现项目迁移日志
