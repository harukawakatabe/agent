"""模拟数据 - 用于测试，替代真实的数据库查询"""
from datetime import date, datetime, timedelta
from typing import List, Dict, Any
import random


# 模拟运动记录数据
MOCK_WORKOUT_RECORDS = [
    {
        "id": 1,
        "user_id": 1,
        "date": date.today().isoformat(),
        "exercise_type": "跑步",
        "duration": 30,
        "calories_burned": 300,
        "heart_rate_avg": 145,
        "notes": "晨跑5公里",
        "created_at": datetime.now().isoformat()
    },
    {
        "id": 2,
        "user_id": 1,
        "date": date.today().isoformat(),
        "exercise_type": "力量训练",
        "duration": 45,
        "calories_burned": 250,
        "heart_rate_avg": 120,
        "notes": "胸肌训练",
        "created_at": datetime.now().isoformat()
    },
    {
        "id": 3,
        "user_id": 1,
        "date": (date.today() - timedelta(days=1)).isoformat(),
        "exercise_type": "游泳",
        "duration": 60,
        "calories_burned": 400,
        "heart_rate_avg": 130,
        "notes": "自由泳1000米",
        "created_at": (datetime.now() - timedelta(days=1)).isoformat()
    },
    {
        "id": 4,
        "user_id": 1,
        "date": (date.today() - timedelta(days=2)).isoformat(),
        "exercise_type": "跑步",
        "duration": 40,
        "calories_burned": 350,
        "heart_rate_avg": 150,
        "notes": "夜跑6公里",
        "created_at": (datetime.now() - timedelta(days=2)).isoformat()
    },
    {
        "id": 5,
        "user_id": 1,
        "date": (date.today() - timedelta(days=3)).isoformat(),
        "exercise_type": "瑜伽",
        "duration": 30,
        "calories_burned": 150,
        "heart_rate_avg": 90,
        "notes": "拉伸放松",
        "created_at": (datetime.now() - timedelta(days=3)).isoformat()
    },
    {
        "id": 6,
        "user_id": 1,
        "date": (date.today() - timedelta(days=4)).isoformat(),
        "exercise_type": "力量训练",
        "duration": 50,
        "calories_burned": 280,
        "heart_rate_avg": 125,
        "notes": "背部训练",
        "created_at": (datetime.now() - timedelta(days=4)).isoformat()
    },
    {
        "id": 7,
        "user_id": 1,
        "date": (date.today() - timedelta(days=5)).isoformat(),
        "exercise_type": "跑步",
        "duration": 35,
        "calories_burned": 320,
        "heart_rate_avg": 148,
        "notes": "间歇跑训练",
        "created_at": (datetime.now() - timedelta(days=5)).isoformat()
    },
    {
        "id": 8,
        "user_id": 1,
        "date": (date.today() - timedelta(days=6)).isoformat(),
        "exercise_type": "游泳",
        "duration": 45,
        "calories_burned": 350,
        "heart_rate_avg": 135,
        "notes": "蛙泳800米",
        "created_at": (datetime.now() - timedelta(days=6)).isoformat()
    }
]


def get_mock_records(
    user_id: int = 1,
    date_filter: str = None,
    exercise_type: str = None,
    start_date: str = None,
    end_date: str = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    获取模拟运动记录
    
    Args:
        user_id: 用户ID
        date_filter: 日期过滤（YYYY-MM-DD）
        exercise_type: 运动类型过滤
        start_date: 开始日期
        end_date: 结束日期
        limit: 返回数量限制
    
    Returns:
        过滤后的运动记录列表
    """
    results = [r for r in MOCK_WORKOUT_RECORDS if r["user_id"] == user_id]
    
    if date_filter:
        results = [r for r in results if r["date"] == date_filter]
    
    if start_date and end_date:
        results = [r for r in results if start_date <= r["date"] <= end_date]
    
    if exercise_type:
        results = [r for r in results if r["exercise_type"] == exercise_type]
    
    # 按日期降序排序
    results.sort(key=lambda x: x["date"], reverse=True)
    
    return results[:limit]


def get_today_summary(user_id: int = 1) -> Dict[str, Any]:
    """
    获取今天的运动汇总
    
    Args:
        user_id: 用户ID
    
    Returns:
        汇总统计字典
    """
    today = date.today().isoformat()
    today_records = get_mock_records(user_id=user_id, date_filter=today)
    
    if not today_records:
        return {
            "total_workouts": 0,
            "total_duration": 0,
            "total_calories": 0,
            "avg_heart_rate": 0,
            "exercise_types": ""
        }
    
    total_workouts = len(today_records)
    total_duration = sum(r["duration"] for r in today_records)
    total_calories = sum(r["calories_burned"] for r in today_records)
    avg_heart_rate = sum(r["heart_rate_avg"] for r in today_records) / total_workouts if total_workouts > 0 else 0
    exercise_types = ", ".join(set(r["exercise_type"] for r in today_records))
    
    return {
        "total_workouts": total_workouts,
        "total_duration": total_duration,
        "total_calories": total_calories,
        "avg_heart_rate": round(avg_heart_rate, 1),
        "exercise_types": exercise_types
    }


def get_statistics(user_id: int = 1, days: int = 7) -> List[Dict[str, Any]]:
    """
    获取指定天数内的统计数据
    
    Args:
        user_id: 用户ID
        days: 天数
    
    Returns:
        按日期分组的统计列表
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=days-1)
    
    all_records = get_mock_records(
        user_id=user_id,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat()
    )
    
    # 按日期分组
    stats_by_date = {}
    for record in all_records:
        record_date = record["date"]
        if record_date not in stats_by_date:
            stats_by_date[record_date] = {
                "date": record_date,
                "workout_count": 0,
                "total_duration": 0,
                "total_calories": 0,
                "heart_rates": []
            }
        
        stats_by_date[record_date]["workout_count"] += 1
        stats_by_date[record_date]["total_duration"] += record["duration"]
        stats_by_date[record_date]["total_calories"] += record["calories_burned"]
        stats_by_date[record_date]["heart_rates"].append(record["heart_rate_avg"])
    
    # 计算平均心率并格式化
    result = []
    for record_date, stats in sorted(stats_by_date.items(), reverse=True):
        avg_heart_rate = sum(stats["heart_rates"]) / len(stats["heart_rates"]) if stats["heart_rates"] else 0
        result.append({
            "date": stats["date"],
            "workout_count": stats["workout_count"],
            "total_duration": stats["total_duration"],
            "total_calories": stats["total_calories"],
            "avg_heart_rate": round(avg_heart_rate, 1)
        })
    
    return result

