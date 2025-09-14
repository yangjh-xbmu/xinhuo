#!/bin/bash

# 代理管理工具安装脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROXY_SCRIPT="$SCRIPT_DIR/proxy_manager.sh"
BASHRC_PROXY="$SCRIPT_DIR/.bashrc_proxy"
USER_BASHRC="$HOME/.bashrc"
USER_BASH_PROFILE="$HOME/.bash_profile"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 代理管理工具安装程序${NC}"
echo "================================"

# 检查必要文件
if [[ ! -f "$PROXY_SCRIPT" ]]; then
    echo -e "${RED}错误: 找不到代理管理脚本 $PROXY_SCRIPT${NC}"
    exit 1
fi

if [[ ! -f "$BASHRC_PROXY" ]]; then
    echo -e "${RED}错误: 找不到bash配置文件 $BASHRC_PROXY${NC}"
    exit 1
fi

# 给脚本添加执行权限
chmod +x "$PROXY_SCRIPT"
echo -e "${GREEN}✓ 已设置脚本执行权限${NC}"

# 检查用户的bash配置文件
BASH_CONFIG=""
if [[ -f "$USER_BASHRC" ]]; then
    BASH_CONFIG="$USER_BASHRC"
elif [[ -f "$USER_BASH_PROFILE" ]]; then
    BASH_CONFIG="$USER_BASH_PROFILE"
else
    echo -e "${YELLOW}⚠️  未找到 ~/.bashrc 或 ~/.bash_profile，将创建 ~/.bashrc${NC}"
    BASH_CONFIG="$USER_BASHRC"
    touch "$BASH_CONFIG"
fi

echo -e "${BLUE}📝 将配置添加到: $BASH_CONFIG${NC}"

# 检查是否已经配置过
CONFIG_MARKER="# Proxy Manager Configuration"
if grep -q "$CONFIG_MARKER" "$BASH_CONFIG"; then
    echo -e "${YELLOW}⚠️  检测到已有配置，是否覆盖? (y/N)${NC}"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        # 移除旧配置
        sed -i "/^$CONFIG_MARKER/,/^# End Proxy Manager Configuration/d" "$BASH_CONFIG"
        echo -e "${GREEN}✓ 已移除旧配置${NC}"
    else
        echo -e "${YELLOW}取消安装${NC}"
        exit 0
    fi
fi

# 添加配置到bash文件
cat >> "$BASH_CONFIG" << EOF

$CONFIG_MARKER
# 自动加载代理管理工具
if [[ -f "$BASHRC_PROXY" ]]; then
    source "$BASHRC_PROXY"
fi
# End Proxy Manager Configuration
EOF

echo -e "${GREEN}✓ 配置已添加到 $BASH_CONFIG${NC}"

# 创建全局命令链接（可选）
echo -e "${BLUE}🔗 是否创建全局命令链接? (y/N)${NC}"
read -r create_link
if [[ "$create_link" =~ ^[Yy]$ ]]; then
    LOCAL_BIN="$HOME/.local/bin"
    if [[ ! -d "$LOCAL_BIN" ]]; then
        mkdir -p "$LOCAL_BIN"
        echo -e "${GREEN}✓ 已创建目录 $LOCAL_BIN${NC}"
    fi
    
    ln -sf "$PROXY_SCRIPT" "$LOCAL_BIN/proxy"
    echo -e "${GREEN}✓ 已创建全局命令链接: proxy${NC}"
    
    # 检查PATH
    if [[ ":$PATH:" != *":$LOCAL_BIN:"* ]]; then
        echo -e "${YELLOW}⚠️  请确保 $LOCAL_BIN 在你的 PATH 中${NC}"
        echo -e "   可以添加以下行到你的 $BASH_CONFIG:"
        echo -e "   ${BLUE}export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}"
    fi
fi

echo ""
echo -e "${GREEN}🎉 安装完成！${NC}"
echo "================================"
echo -e "${BLUE}使用方法:${NC}"
echo "  重新加载bash: source $BASH_CONFIG"
echo "  或者重新打开终端"
echo ""
echo -e "${BLUE}可用命令:${NC}"
echo "  proxy-on       启用代理"
echo "  proxy-off      禁用代理"
echo "  proxy-status   查看代理状态"
echo "  git-proxy-on   启用Git代理"
echo "  git-proxy-off  禁用Git代理"
echo ""
echo -e "${YELLOW}注意: 代理将在每次bash启动时自动检查并启用（如果可用）${NC}"