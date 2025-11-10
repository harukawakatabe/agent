"""数据分析工具 - 提供运动数据分析功能"""
from typing import List, Dict, Any
try:
    from langchain_core.tools import tool
except ImportError:
    from langchain.tools import tool
import json


@tool
def analyze_workout_trends(data: str) -> str:
    """
    分析运动趋势
    
    Args:
        data: JSON格式的运动记录数据字符串
    
    Returns:
        趋势分析结果
    """
    try:
        records = json.loads(data) if isinstance(data, str) else data
        
        if not records:
            return "没有足够的数据进行趋势分析"
        
        # 分析逻辑（伪代码）
        # 实际实现时可以分析：
        # - 运动频率趋势
        # - 运动时长趋势
        # - 卡路里消耗趋势
        # - 心率变化趋势
        
        total_workouts = len(records)
        total_duration = sum(r.get("duration", 0) for r in records)
        total_calories = sum(r.get("calories_burned", 0) for r in records)
        
        analysis = f"""
趋势分析结果：
- 总运动次数：{total_workouts}次
- 总运动时长：{total_duration}分钟
- 总消耗卡路里：{total_calories}卡
- 平均每次运动时长：{total_duration/total_workouts:.1f}分钟（如果总次数>0）
        """
        
        return analysis.strip()
    
    except Exception as e:
        return f"分析失败: {str(e)}"


@tool
def compare_workout_performance(
    period1_data: str,
    period2_data: str,
    period1_name: str = "期间1",
    period2_name: str = "期间2"
) -> str:
    """
    比较两个时期的运动表现
    
    Args:
        period1_data: 第一个时期的JSON数据
        period2_data: 第二个时期的JSON数据
        period1_name: 第一个时期的名称
        period2_name: 第二个时期的名称
    
    Returns:
        比较分析结果
    """
    try:
        data1 = json.loads(period1_data) if isinstance(period1_data, str) else period1_data
        data2 = json.loads(period2_data) if isinstance(period2_data, str) else period2_data
        
        def calculate_stats(data):
            if not data:
                return {"count": 0, "duration": 0, "calories": 0}
            return {
                "count": len(data),
                "duration": sum(r.get("duration", 0) for r in data),
                "calories": sum(r.get("calories_burned", 0) for r in data)
            }
        
        stats1 = calculate_stats(data1)
        stats2 = calculate_stats(data2)
        
        comparison = f"""
运动表现对比：
{period1_name}:
  - 运动次数：{stats1['count']}次
  - 总时长：{stats1['duration']}分钟
  - 总卡路里：{stats1['calories']}卡

{period2_name}:
  - 运动次数：{stats2['count']}次
  - 总时长：{stats2['duration']}分钟
  - 总卡路里：{stats2['calories']}卡

变化：
  - 运动次数：{stats2['count'] - stats1['count']:+d}次
  - 总时长：{stats2['duration'] - stats1['duration']:+d}分钟
  - 总卡路里：{stats2['calories'] - stats1['calories']:+d}卡
        """
        
        return comparison.strip()
    
    except Exception as e:
        return f"比较分析失败: {str(e)}"


@tool
def get_exercise_type_distribution(data: str) -> str:
    """
    获取运动类型分布
    
    Args:
        data: JSON格式的运动记录数据
    
    Returns:
        运动类型分布统计
    """
    try:
        records = json.loads(data) if isinstance(data, str) else data
        
        if not records:
            return "没有数据可分析"
        
        # 统计各运动类型的次数和时长
        type_stats = {}
        for record in records:
            ex_type = record.get("exercise_type", "未知")
            if ex_type not in type_stats:
                type_stats[ex_type] = {"count": 0, "duration": 0, "calories": 0}
            
            type_stats[ex_type]["count"] += 1
            type_stats[ex_type]["duration"] += record.get("duration", 0)
            type_stats[ex_type]["calories"] += record.get("calories_burned", 0)
        
        # 格式化输出
        result = "运动类型分布：\n"
        for ex_type, stats in sorted(type_stats.items(), key=lambda x: x[1]["count"], reverse=True):
            result += f"- {ex_type}: {stats['count']}次, {stats['duration']}分钟, {stats['calories']}卡\n"
        
        return result.strip()
    
    except Exception as e:
        return f"分析失败: {str(e)}"


# 导出所有分析工具
ANALYSIS_TOOLS = [
    analyze_workout_trends,
    compare_workout_performance,
    get_exercise_type_distribution
]

