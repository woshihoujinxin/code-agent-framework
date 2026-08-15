# 鸿蒙（HarmonyOS）官方模板

> **模板来源**：华为鸿蒙官方项目结构
> **适用场景**：鸿蒙应用开发（ArkTS + ArkUI）

---

## 目录结构

```
{project}/
├── AppScope/              # 应用全局配置
│   └── app.json5         # 应用配置（包名/版本/权限）
├── entry/                 # 主模块（应用入口）
│   ├── src/
│   │   └── main/
│   │       ├── ets/      # ArkTS 源码
│   │       │   ├── entryability/    # Ability 入口
│   │       │   ├── pages/           # 页面
│   │       │   └── utils/           # 工具类
│   │       └── resources/           # 资源文件
│   └── build-profile.json5         # 模块构建配置
├── oh_modules/           # 依赖模块（类似 node_modules）
├── hvigor/               # 构建工具配置
├── build-profile.json5   # 项目构建配置
├── oh-package.json5      # 项目依赖配置
└── hvigorfile.ts         # 构建脚本入口
```

---

## 依赖约定

- **IDE**：DevEco Studio >= 4.0
- **SDK**：HarmonyOS SDK API 9+
- **语言**：ArkTS（TypeScript 超集）
- **UI**：ArkUI 声明式 UI
- **构建**：hvigorw（基于 Gradle）

---

## 端口与数据库约定

- **调试端口**：随机（DevEco 自动分配）
- **数据库**：关系型数据库（RDB，仅应用内）
- **网络**：需在 `module.json5` 声明 `requestPermissions`

---

## 模板文件 vs 业务代码

**模板生成文件**（不测、不删、按需修改配置）：
- `AppScope/` 全局配置目录
- `entry/src/main/resources/` 资源文件
- `build-profile.json5`、`oh-package.json5`
- `hvigor/`、`hvigorfile.ts` 构建配置
- `oh_modules/` 依赖目录
- 本 `README.md` 文件

**需业务实现文件**（需测试、需实现）：
- `entry/src/main/ets/entryability/`（Ability 入口）
- `entry/src/main/ets/pages/`（页面业务逻辑）
- `entry/src/main/ets/utils/`（工具类）
- `entry/src/main/ets/` 下新增的业务模块

---

## 实现示例（参考）

### 1. 页面示例（entry/src/main/ets/pages/Index.ets）

```typescript
@Entry
@Component
struct Index {
  @State message: string = 'Hello World'

  build() {
    Row() {
      Column({ space: 10 }) {
        Text(this.message)
          .fontSize(50)
          .fontWeight(FontWeight.Bold)

        Button('点击改变')
          .onClick(() => {
            this.message = '你好，鸿蒙'
          })
      }
      .width('100%')
    }
    .height('100%')
  }
}
```

### 2. Ability 入口（entry/src/main/ets/entryability/EntryAbility.ets）

```typescript
import UIAbility from '@ohos.app.ability.UIAbility'
import Window from '@ohos.window'

export default class EntryAbility extends UIAbility {
  onWindowStageCreate(windowStage: Window.WindowStage) {
    windowStage.loadContent('pages/Index', (err) => {
      if (err.code) {
        return
      }
    })
  }
}
```

---

## 注意事项

1. **权限声明**：网络/存储等权限需在 `module.json5` 声明
2. **页面路由**：使用 `@ohos.router` 进行页面跳转
3. **状态管理**：使用 `@State`/`@Prop`/`@Provide`/@Inject` 管理状态
4. **资源访问**：通过 `$r('app.type.name')` 访问资源文件
5. **依赖管理**：通过 `oh-package.json5` 管理，使用 `ohpm install` 安装

---

## 配置修改要点

### 应用配置（AppScope/app.json5）
```json5
{
  "app": {
    "bundleName": "com.example.{project}",
    "versionCode": 1000000,
    "versionName": "1.0.0"
  }
}
```

### 模块配置（entry/build-profile.json5）
```json5
{
  "apiType": "stageMode",
  "buildOption": {},
  "targetOptions": {}
}
```

---

> **维护**：框架维护者 | **模板来源**：华为鸿蒙官方 | **最后更新**：2025-08-15
