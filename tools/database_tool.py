"""数据库查询工具 - 封装为LangChain Tool"""
from typing import Optional, List, Dict, Any
from langchain_core.tools import tool
from database.connection import db_connection
from database.models import WorkoutRecord
from database.mock_data import get_mock_records, get_today_summary, get_statistics


@tool
def query_workout_records(
    user_id: int = 1,
    date: Optional[str] = None,
    exercise_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 100
) -> str:
    """
    查询运动记录数据
    
    Args:
        user_id: 用户ID，默认为1
        date: 查询指定日期的记录（格式：YYYY-MM-DD），如"2024-01-15"
        exercise_type: 运动类型，如"跑步"、"游泳"等
        start_date: 开始日期（格式：YYYY-MM-DD），用于范围查询
        end_date: 结束日期（格式：YYYY-MM-DD），用于范围查询
        limit: 返回记录数量限制，默认100条
    
    Returns:
        JSON格式的运动记录数据字符串
    """
    try:
        # 构建SQL查询
        query = "SELECT * FROM workout_records WHERE user_id = %(user_id)s"
        params = {"user_id": user_id}
        
        if date:
            query += " AND date = %(date)s"
            params["date"] = date
        elif start_date and end_date:
            query += " AND date BETWEEN %(start_date)s AND %(end_date)s"
            params["start_date"] = start_date
            params["end_date"] = end_date
        
        if exercise_type:
            query += " AND exercise_type = %(exercise_type)s"
            params["exercise_type"] = exercise_type
        
        query += " ORDER BY date DESC, created_at DESC LIMIT %(limit)s"
        params["limit"] = limit
        
        """
        实际MySQL查询实现（伪代码）：
        
        results = db_connection.execute_query(query, params)
        """
        
        # 使用模拟数据替代数据库查询
        results = get_mock_records(
            user_id=user_id,
            date_filter=date,
            exercise_type=exercise_type,
            start_date=start_date,
            end_date=end_date,
            limit=limit
        )
        
        if not results:
            return "未找到匹配的运动记录"
        
        # 格式化返回结果
        import json
        return json.dumps(results, ensure_ascii=False, indent=2)
    
    except Exception as e:
        return f"查询失败: {str(e)}"


@tool
def get_today_workout_summary(user_id: int = 1) -> str:
    """
    获取今天的运动汇总信息
    
    Args:
        user_id: 用户ID，默认为1
    
    Returns:
        今天的运动汇总统计信息
    """
    try:
        from datetime import date
        today = date.today().isoformat()
        
        # 查询今天的记录
        query = """
        SELECT 
            COUNT(*) as total_workouts,
            SUM(duration) as total_duration,
            SUM(calories_burned) as total_calories,
            AVG(heart_rate_avg) as avg_heart_rate,
            GROUP_CONCAT(DISTINCT exercise_type) as exercise_types
        FROM workout_records
        WHERE user_id = %(user_id)s AND date = %(date)s
        """
        params = {"user_id": user_id, "date": today}
        
        """
        实际MySQL查询实现（伪代码）：
        
        results = db_connection.execute_query(query, params)
        if results:
            summary = results[0]
            return f"今天共完成{summary['total_workouts']}次运动，总时长{summary['total_duration']}分钟，消耗{summary['total_calories']}卡路里，平均心率{summary['avg_heart_rate']:.0f}次/分，运动类型：{summary['exercise_types']}"
        else:
            return "今天还没有运动记录"
        """
        
        # 使用模拟数据替代数据库查询
        summary = get_today_summary(user_id)
        
        if summary["total_workouts"] > 0:
            return f"今天共完成{summary['total_workouts']}次运动，总时长{summary['total_duration']}分钟，消耗{summary['total_calories']}卡路里，平均心率{summary['avg_heart_rate']:.0f}次/分，运动类型：{summary['exercise_types']}"
        else:
            return "今天还没有运动记录"
    
    except Exception as e:
        return f"查询失败: {str(e)}"


@tool
def get_workout_statistics(
    user_id: int = 1,
    days: int = 7
) -> str:
    """
    获取指定天数内的运动统计数据
    
    Args:
        user_id: 用户ID，默认为1
        days: 统计天数，默认7天
    
    Returns:
        统计信息字符串
    """
    try:
        from datetime import date, timedelta
        end_date = date.today()
        start_date = end_date - timedelta(days=days-1)
        
        query = """
        SELECT 
            date,
            COUNT(*) as workout_count,
            SUM(duration) as total_duration,
            SUM(calories_burned) as total_calories,
            AVG(heart_rate_avg) as avg_heart_rate
        FROM workout_records
        WHERE user_id = %(user_id)s 
            AND date BETWEEN %(start_date)s AND %(end_date)s
        GROUP BY date
        ORDER BY date DESC
        """
        params = {
            "user_id": user_id,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
        
        """
        实际MySQL查询实现（伪代码）：
        
        results = db_connection.execute_query(query, params)
        # 格式化统计结果并返回
        """
        
        # 使用模拟数据替代数据库查询
        stats = get_statistics(user_id=user_id, days=days)
        
        if not stats:
            return f"过去{days}天没有运动记录"
        
        result_lines = [f"过去{days}天的运动统计数据："]
        for stat in stats:
            result_lines.append(
                f"  {stat['date']}: {stat['workout_count']}次运动, "
                f"总时长{stat['total_duration']}分钟, "
                f"消耗{stat['total_calories']}卡路里, "
                f"平均心率{stat['avg_heart_rate']:.1f}次/分"
            )
        
        return "\n".join(result_lines)
    
    except Exception as e:
        return f"查询失败: {str(e)}"


# 导出所有工具
DATABASE_TOOLS = [
    query_workout_records,
    get_today_workout_summary,
    get_workout_statistics
]

