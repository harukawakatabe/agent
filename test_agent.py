"""测试脚本 - 验证Agent逻辑（不需要数据库连接）"""
from tools.database_tool import query_workout_records, get_today_workout_summary, get_workout_statistics
from database.mock_data import get_mock_records, get_today_summary, get_statistics
import json


def test_database_tools():
    """测试数据库工具"""
    print("=" * 60)
    print("测试数据库工具")
    print("=" * 60)
    
    # 测试1: 查询所有记录
    print("\n1. 测试查询所有运动记录:")
    result = query_workout_records.invoke({"user_id": 1, "limit": 5})
    print(result[:200] + "..." if len(result) > 200 else result)
    
    # 测试2: 查询今天的汇总
    print("\n2. 测试获取今天的运动汇总:")
    result = get_today_workout_summary.invoke({"user_id": 1})
    print(result)
    
    # 测试3: 查询统计数据
    print("\n3. 测试获取过去7天的统计数据:")
    result = get_workout_statistics.invoke({"user_id": 1, "days": 7})
    print(result)
    
    # 测试4: 按日期查询
    print("\n4. 测试按日期查询:")
    from datetime import date
    today = date.today().isoformat()
    result = query_workout_records.invoke({"user_id": 1, "date": today})
    print(result[:300] + "..." if len(result) > 300 else result)
    
    # 测试5: 按运动类型查询
    print("\n5. 测试按运动类型查询（跑步）:")
    result = query_workout_records.invoke({"user_id": 1, "exercise_type": "跑步", "limit": 3})
    print(result[:300] + "..." if len(result) > 300 else result)


def test_mock_data():
    """测试模拟数据"""
    print("\n" + "=" * 60)
    print("测试模拟数据模块")
    print("=" * 60)
    
    # 测试获取所有记录
    print("\n1. 所有模拟记录数量:", len(get_mock_records()))
    
    # 测试获取今天的汇总
    print("\n2. 今天的运动汇总:")
    summary = get_today_summary()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    
    # 测试获取统计数据
    print("\n3. 过去7天的统计数据:")
    stats = get_statistics(days=7)
    for stat in stats:
        print(f"  {stat['date']}: {stat['workout_count']}次运动, "
              f"{stat['total_duration']}分钟, {stat['total_calories']}卡路里")


if __name__ == "__main__":
    print("开始测试健身记录分析Agent...")
    print("\n注意：此测试使用模拟数据，不需要真实的数据库连接")
    
    try:
        test_mock_data()
        test_database_tools()
        print("\n" + "=" * 60)
        print("✅ 所有测试完成！")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

