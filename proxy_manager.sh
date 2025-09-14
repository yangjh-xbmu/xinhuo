#!/bin/bash

# 代理管理脚本
# 用于管理HTTP/HTTPS代理设置

# 代理配置
PROXY_HOST="127.0.0.1"
PROXY_PORT="10808"
PROXY_URL="http://${PROXY_HOST}:${PROXY_PORT}"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查代理是否可用
check_proxy() {
    if curl -s --connect-timeout 3 --proxy "$PROXY_URL" http://www.google.com > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# 启用代理
enable_proxy() {
    export http_proxy="$PROXY_URL"
    export https_proxy="$PROXY_URL"
    export HTTP_PROXY="$PROXY_URL"
    export HTTPS_PROXY="$PROXY_URL"
    export no_proxy="localhost,127.0.0.1,::1"
    export NO_PROXY="localhost,127.0.0.1,::1"
    
    echo -e "${GREEN}✓ 代理已启用${NC}"
    echo -e "  HTTP代理: ${YELLOW}$http_proxy${NC}"
    echo -e "  HTTPS代理: ${YELLOW}$https_proxy${NC}"
}

# 禁用代理
disable_proxy() {
    unset http_proxy
    unset https_proxy
    unset HTTP_PROXY
    unset HTTPS_PROXY
    unset no_proxy
    unset NO_PROXY
    
    echo -e "${RED}✗ 代理已禁用${NC}"
}

# 显示代理状态
show_proxy_status() {
    if [[ -n "$http_proxy" || -n "$HTTP_PROXY" ]]; then
        echo -e "${GREEN}代理状态: 已启用${NC}"
        echo -e "  HTTP代理: ${YELLOW}${http_proxy:-$HTTP_PROXY}${NC}"
        echo -e "  HTTPS代理: ${YELLOW}${https_proxy:-$HTTPS_PROXY}${NC}"
        
        if check_proxy; then
            echo -e "  连接状态: ${GREEN}✓ 可用${NC}"
        else
            echo -e "  连接状态: ${RED}✗ 不可用${NC}"
        fi
    else
        echo -e "${RED}代理状态: 已禁用${NC}"
    fi
}

# 自动启用代理（bash启动时调用）
auto_enable_proxy() {
    # 检查代理服务是否可用
    if check_proxy; then
        enable_proxy
        echo -e "${GREEN}🚀 代理自动启用成功${NC}"
    else
        echo -e "${YELLOW}⚠️  代理服务不可用，跳过自动启用${NC}"
    fi
}

# 主函数
main() {
    case "$1" in
        "on"|"enable")
            enable_proxy
            ;;
        "off"|"disable")
            disable_proxy
            ;;
        "status"|"show")
            show_proxy_status
            ;;
        "auto")
            auto_enable_proxy
            ;;
        "help"|"--help"|"")
            echo "代理管理脚本"
            echo "用法: $0 [命令]"
            echo ""
            echo "命令:"
            echo "  on, enable    启用代理"
            echo "  off, disable  禁用代理"
            echo "  status, show  显示代理状态"
            echo "  auto          自动启用代理（如果可用）"
            echo "  help          显示此帮助信息"
            echo ""
            echo "快捷别名:"
            echo "  proxy_on      启用代理"
            echo "  proxy_off     禁用代理"
            echo "  proxy_status  显示代理状态"
            ;;
        *)
            echo -e "${RED}错误: 未知命令 '$1'${NC}"
            echo "使用 '$0 help' 查看帮助信息"
            exit 1
            ;;
    esac
}

# 定义快捷别名函数
proxy_on() {
    enable_proxy
}

proxy_off() {
    disable_proxy
}

proxy_status() {
    show_proxy_status
}

# 如果脚本被直接执行
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi

# 如果脚本被source，自动启用代理
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
    auto_enable_proxy
fi