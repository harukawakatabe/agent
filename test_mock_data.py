"""测试模拟数据模块 - 不依赖langchain，直接测试数据逻辑"""
from database.mock_data import get_mock_records, get_today_summary, get_statistics
import json
from datetime import date


def test_mock_data():
    """测试模拟数据模块"""
    print("=" * 60)
    print("测试模拟数据模块")
    print("=" * 60)
    
    # 测试1: 获取所有记录
    print("\n1. 获取所有模拟记录:")
    all_records = get_mock_records()
    print(f"   总记录数: {len(all_records)}")
    print(f"   前3条记录:")
    for i, record in enumerate(all_records[:3], 1):
        print(f"     {i}. {record['date']} - {record['exercise_type']} - {record['duration']}分钟")
    
    # 测试2: 获取今天的汇总
    print("\n2. 获取今天的运动汇总:")
    summary = get_today_summary(user_id=1)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    
    if summary["total_workouts"] > 0:
        print(f"\n   今天共完成{summary['total_workouts']}次运动，")
        print(f"   总时长{summary['total_duration']}分钟，")
        print(f"   消耗{summary['total_calories']}卡路里，")
        print(f"   平均心率{summary['avg_heart_rate']:.1f}次/分，")
        print(f"   运动类型：{summary['exercise_types']}")
    
    # 测试3: 获取统计数据
    print("\n3. 获取过去7天的统计数据:")
    stats = get_statistics(user_id=1, days=7)
    print(f"   共{len(stats)}天的数据:")
    for stat in stats:
        print(f"     {stat['date']}: {stat['workout_count']}次运动, "
              f"{stat['total_duration']}分钟, {stat['total_calories']}卡路里, "
              f"平均心率{stat['avg_heart_rate']:.1f}次/分")
    
    # 测试4: 按日期查询
    print("\n4. 按日期查询（今天）:")
    today = date.today().isoformat()
    today_records = get_mock_records(user_id=1, date_filter=today)
    print(f"   今天有{len(today_records)}条记录:")
    for record in today_records:
        print(f"     - {record['exercise_type']}: {record['duration']}分钟, "
              f"{record['calories_burned']}卡路里")
    
    # 测试5: 按运动类型查询
    print("\n5. 按运动类型查询（跑步）:")
    running_records = get_mock_records(user_id=1, exercise_type="跑步")
    print(f"   跑步记录共{len(running_records)}条:")
    for record in running_records:
        print(f"     - {record['date']}: {record['duration']}分钟, "
              f"{record['calories_burned']}卡路里")
    
    # 测试6: 按日期范围查询
    print("\n6. 按日期范围查询（过去3天）:")
    from datetime import timedelta
    end_date = date.today()
    start_date = end_date - timedelta(days=2)
    range_records = get_mock_records(
        user_id=1,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat()
    )
    print(f"   过去3天共有{len(range_records)}条记录")
    
    print("\n" + "=" * 60)
    print("✅ 所有测试完成！模拟数据模块工作正常")
    print("=" * 60)


if __name__ == "__main__":
    print("开始测试模拟数据模块...")
    print("注意：此测试不依赖langchain，直接测试数据逻辑\n")
    
    try:
        test_mock_data()
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

