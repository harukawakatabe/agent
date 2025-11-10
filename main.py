"""主入口文件 - 提供命令行交互界面"""
import sys
from agents.fitness_agent import fitness_agent
import config


def print_banner():
    """打印欢迎横幅"""
    banner = """
    ╔════════════════════════════════════════╗
    ║    健身记录分析Agent系统                ║
    ║    Fitness Record Analysis Agent       ║
    ╚════════════════════════════════════════╝
    """
    print(banner)


def print_help():
    """打印帮助信息"""
    help_text = """
使用说明：
- 输入你的查询，例如：
  * "帮我看看今天的运动表现"
  * "分析我这次的记录"
  * "最近一周的运动趋势"
  * "对比上个月和这个月的运动数据"
  
- 输入 'quit' 或 'exit' 退出程序
- 输入 'help' 查看帮助信息
    """
    print(help_text)


def check_config():
    """检查配置是否完整"""
    if not config.OPENAI_API_KEY:
        print("⚠️  警告: 未配置OPENAI_API_KEY")
        print("请在.env文件中设置OPENAI_API_KEY，或设置环境变量")
        print("示例: OPENAI_API_KEY=your-api-key-here")
        return False
    return True


def main():
    """主函数"""
    print_banner()
    
    # 检查配置
    if not check_config():
        response = input("\n是否继续？(y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    print("\n✅ Agent已就绪，可以开始查询了！")
    print_help()
    print("\n" + "="*50)
    
    # 交互循环
    while True:
        try:
            # 获取用户输入
            user_query = input("\n💬 请输入你的查询: ").strip()
            
            if not user_query:
                continue
            
            # 处理特殊命令
            if user_query.lower() in ['quit', 'exit', '退出']:
                print("\n👋 再见！")
                break
            
            if user_query.lower() in ['help', '帮助']:
                print_help()
                continue
            
            # 执行Agent查询
            print("\n🤔 正在分析中...")
            print("-" * 50)
            
            response = fitness_agent.invoke(user_query)
            
            print("\n📊 分析结果:")
            print(response)
            print("-" * 50)
        
        except KeyboardInterrupt:
            print("\n\n👋 程序已中断，再见！")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {str(e)}")
            print("请检查配置和网络连接")


if __name__ == "__main__":
    main()

