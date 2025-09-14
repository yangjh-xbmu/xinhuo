# 代理管理工具

一个简单易用的bash代理管理工具，支持自动启用代理和手动控制。

## 功能特性

- ✅ bash启动时自动检查并启用代理
- ✅ 手动启用/禁用代理
- ✅ 代理状态检查和显示
- ✅ Git代理管理
- ✅ 友好的彩色输出
- ✅ 代理连接可用性检测

## 文件说明

- `proxy_manager.sh` - 主要的代理管理脚本
- `.bashrc_proxy` - bash配置文件，用于自动加载
- `install_proxy.sh` - 自动安装脚本
- `PROXY_README.md` - 使用说明文档

## 快速安装

### 方法1: 使用安装脚本（推荐）

```bash
# 给安装脚本执行权限
chmod +x install_proxy.sh

# 运行安装脚本
./install_proxy.sh

# 重新加载bash配置
source ~/.bashrc
```

### 方法2: 手动安装

1. 给脚本添加执行权限：
```bash
chmod +x proxy_manager.sh
```

2. 将以下内容添加到你的 `~/.bashrc` 或 `~/.bash_profile`：
```bash
# Proxy Manager Configuration
# 自动加载代理管理工具
if [[ -f "/path/to/your/.bashrc_proxy" ]]; then
    source "/path/to/your/.bashrc_proxy"
fi
# End Proxy Manager Configuration
```

3. 重新加载配置：
```bash
source ~/.bashrc
```

## 使用方法

### 基本命令

```bash
# 启用代理
proxy-on
# 或者
./proxy_manager.sh on

# 禁用代理
proxy-off
# 或者
./proxy_manager.sh off

# 查看代理状态
proxy-status
# 或者
./proxy_manager.sh status

# 查看帮助
./proxy_manager.sh help
```

### Git代理管理

```bash
# 启用Git代理
git-proxy-on

# 禁用Git代理
git-proxy-off
```

### 自动代理

代理工具会在每次bash启动时自动检查代理服务是否可用：
- 如果代理服务可用，自动启用代理
- 如果代理服务不可用，跳过启用并显示警告

## 配置说明

### 代理设置

默认代理配置在 `proxy_manager.sh` 中：
```bash
PROXY_HOST="127.0.0.1"
PROXY_PORT="10808"
```

如需修改代理地址或端口，请编辑这两个变量。

### 环境变量

启用代理时，工具会设置以下环境变量：
- `http_proxy`
- `https_proxy`
- `HTTP_PROXY`
- `HTTPS_PROXY`
- `no_proxy` (localhost,127.0.0.1,::1)
- `NO_PROXY` (localhost,127.0.0.1,::1)

## 故障排除

### 代理无法启用

1. 检查代理服务是否运行：
```bash
netstat -an | grep 10808
```

2. 检查代理配置是否正确：
```bash
proxy-status
```

3. 手动测试代理连接：
```bash
curl --proxy http://127.0.0.1:10808 http://www.google.com
```

### bash配置未生效

1. 确认配置已添加到正确的文件：
```bash
cat ~/.bashrc | grep "Proxy Manager"
```

2. 重新加载配置：
```bash
source ~/.bashrc
```

3. 或者重新打开终端

### 权限问题

确保脚本有执行权限：
```bash
chmod +x proxy_manager.sh
chmod +x install_proxy.sh
```

## 卸载

1. 从 `~/.bashrc` 中移除配置：
```bash
sed -i '/^# Proxy Manager Configuration/,/^# End Proxy Manager Configuration/d' ~/.bashrc
```

2. 删除相关文件：
```bash
rm -f proxy_manager.sh .bashrc_proxy install_proxy.sh PROXY_README.md
```

3. 如果创建了全局链接，删除它：
```bash
rm -f ~/.local/bin/proxy
```

## 高级用法

### 在脚本中使用

```bash
#!/bin/bash

# 加载代理管理工具
source /path/to/.bashrc_proxy

# 启用代理
proxy_on

# 你的网络操作
curl https://api.example.com

# 禁用代理
proxy_off
```

### 条件代理

```bash
# 只在特定网络环境下启用代理
if ping -c 1 8.8.8.8 > /dev/null 2>&1; then
    echo "直连网络可用，不启用代理"
else
    echo "直连网络不可用，尝试启用代理"
    proxy_on
fi
```

## 注意事项

1. 代理设置只对当前shell会话有效
2. 某些应用可能需要单独配置代理
3. 代理服务必须在指定端口运行才能自动启用
4. 建议定期检查代理服务状态

## 支持的系统

- Linux (所有发行版)
- macOS
- Windows (WSL/Git Bash/Cygwin)

## 许可证

本工具采用MIT许可证，可自由使用和修改。