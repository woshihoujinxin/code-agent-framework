# 19 个 Agent 人设 Token 实测对比

> 稳健版：串行+随机间隔防429+异常重跑。每个 agent 以 `claude --agent` 启动，3 固定问题。
> token = input+output+cache_read+cache_write。输入输出钉死，差异来自人设。

| agent | 优化前 | 优化后 | 节省 | 变化% |
|-------|--------|--------|------|------|
| code-tester-e2e | 24,586 | 22,834 | ↓1752 | 7.1% |
| code-discovery-analyst | 20,182 | 20,064 | ↓118 | 0.6% |
| code-ops | 20,526 | 20,418 | ↓108 | 0.5% |
| code-tester-quality | 21,790 | 21,746 | ↓44 | 0.2% |
| code-dev-backend | 21,616 | 21,578 | ↓38 | 0.2% |
| build-builder | 19,088 | 19,052 | ↓36 | 0.2% |
| code-export-specialist | 18,966 | 18,930 | ↓36 | 0.2% |
| code-product-manager | 23,834 | 23,802 | ↓32 | 0.1% |
| code-reviewer | 18,066 | 18,056 | ↓10 | 0.1% |
| code-prototype-critic | 21,862 | 21,860 | ↓2 | 0.0% |
| code-planner | 30,736 | 30,750 | ↑14 | 0.0% |
| code-sage | 19,390 | 19,404 | ↑14 | 0.1% |
| code-prototype-builder | 21,444 | 21,486 | ↑42 | 0.2% |
| code-researcher | 24,840 | 24,886 | ↑46 | 0.2% |
| artifact-validator | 19,326 | 19,416 | ↑90 | 0.5% |
| code-dev-frontend | 21,550 | 21,668 | ↑118 | 0.5% |
| code-tester-correctness | 20,726 | 20,862 | ↑136 | 0.7% |
| code-tester-robustness | 20,362 | 20,616 | ↑254 | 1.2% |
| code-tester-security | 23,614 | 24,074 | ↑460 | 1.9% |
| **合计** | **412,504** | **411,502** | **↓1,002** | **0.2%** |