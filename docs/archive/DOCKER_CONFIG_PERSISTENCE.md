# Docker 配置持久化说明

**日期**: 2026-03-30

---

## 问题现象

用户在 Web UI 中保存的大模型 API 配置，在 Docker 版本更新、重建镜像或替换容器后丢失，需要重新填写。

---

## 根因

原实现将用户 API 配置保存到：

`/app/config/user_config.json`

但 Docker 仅持久化了以下目录：

- `/app/data`
- `/app/logs`
- `/app/output`
- `/app/cache`
- `/app/backups`
- `/app/project_templates`
- `/app/plugins`

`/app/config` 未做持久化，因此容器重建后该目录会回到镜像默认状态，用户保存的配置自然丢失。

---

## 修复方案

新增统一运行时配置路径模块：

- 环境变量：`AINOVEL_CONFIG_DIR`
- Docker 默认值：`/app/data/config`

应用会将以下运行时配置写入持久化目录：

- `user_config.json`
- `generation_config.json`
- `custom_prompts.json`
- `novel_tool_config.json`

同时，启动时会自动补齐默认配置文件，避免首次运行时持久化目录为空导致配置缺失。

---

## 效果

更新 Docker 版本后，只要 NAS 上的 `/share/CACHEDEV1_DATA/Container/ainovel/data` 没被删除：

- API Key 不会丢
- 提供商模型配置不会丢
- 生成参数不会丢
- 自定义提示词不会丢

---

## 运维建议

1. 更新代码后重新构建镜像
2. 重建或重启容器
3. 确认容器内环境变量 `AINOVEL_CONFIG_DIR=/app/data/config`
4. 首次启动后检查 `/share/CACHEDEV1_DATA/Container/ainovel/data/config/` 是否已生成配置文件
