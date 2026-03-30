# 自动重写上下文参数兼容修复报告

**日期**: 2026-03-30

---

## 问题结论

本次自动重写失败属于**代码接口兼容问题**，不是大模型 API 故障。

直接证据：

```text
TypeError: AutoNovelGenerator._build_smart_context() got an unexpected keyword argument 'max_tokens_limit'
```

该异常发生在 Python 本地方法调用阶段，尚未执行到 `self.api_client.generate(...)`，因此与模型供应商、网络请求、模型返回内容无关。

---

## 根因分析

`src/ui/features/auto_generation.py` 中：

- `_rewrite_chapter()` 的一条调用链在运行环境中传入了 `max_tokens_limit=...`
- `_build_smart_context()` 当前签名只接受 `max_tokens`

这说明存在以下至少一种情况：

1. 容器内运行代码与当前工作区代码不同步
2. 热更新后仍有旧模块实例驻留
3. 某次重构只修改了方法定义或调用方的一侧，未完全同步

---

## 修复策略

为了避免旧代码和新代码混跑导致自动重写直接失败，已将 `_build_smart_context()` 调整为兼容双参数名：

- `max_tokens`
- `max_tokens_limit`（旧调用别名）

兼容逻辑：

- 如果只传入 `max_tokens_limit`，自动映射到 `max_tokens`
- 记录 warning 日志，提示部署版本存在接口漂移
- 如果两个参数都未传，使用默认值 `4000`

这样可以同时兜住：

- 当前仓库代码
- 容器中可能残留的旧调用链
- 未来尚未完全同步的部署版本

---

## 影响判断

### 修复前

- 自动重写 100% 在本地抛 `TypeError`
- 每次重写尝试都会立即失败
- 质量评估后无法真正进入重写生成

### 修复后

- 自动重写可以继续执行到模型调用阶段
- 若后续还有失败，才需要继续排查 API、上下文长度、模型输出质量等问题

---

## 后续建议

1. 重新部署当前版本到容器，避免继续依赖兼容层
2. 重启应用进程，清理可能驻留的旧模块实例
3. 观察日志中是否还出现 `max_tokens_limit` 兼容警告
4. 如果兼容警告消失但自动重写仍失败，再继续检查：
   - API超时
   - 上下文过长
   - 模型空响应
   - 质量评估阈值过严
