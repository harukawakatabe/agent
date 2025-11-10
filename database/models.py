"""数据模型定义 - 定义数据库表结构"""
from typing import Optional
from datetime import date, datetime


class WorkoutRecord:
    """运动记录数据模型"""
    
    def __init__(
        self,
        id: Optional[int] = None,
        user_id: int = 1,
        date: date = None,
        exercise_type: str = "",
        duration: int = 0,  # 分钟
        calories_burned: int = 0,
        heart_rate_avg: int = 0,
        notes: str = "",
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.date = date or date.today()
        self.exercise_type = exercise_type
        self.duration = duration
        self.calories_burned = calories_burned
        self.heart_rate_avg = heart_rate_avg
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "date": self.date.isoformat() if isinstance(self.date, date) else str(self.date),
            "exercise_type": self.exercise_type,
            "duration": self.duration,
            "calories_burned": self.calories_burned,
            "heart_rate_avg": self.heart_rate_avg,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else str(self.created_at)
        }


# 数据库表结构定义（SQL）
WORKOUT_RECORDS_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS workout_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    exercise_type VARCHAR(50) NOT NULL,
    duration INT NOT NULL COMMENT '运动时长（分钟）',
    calories_burned INT DEFAULT 0 COMMENT '消耗卡路里',
    heart_rate_avg INT DEFAULT 0 COMMENT '平均心率',
    notes TEXT COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_date (user_id, date),
    INDEX idx_date (date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='运动记录表';
"""

# PostgreSQL版本的表结构
WORKOUT_RECORDS_TABLE_SCHEMA_POSTGRESQL = """
CREATE TABLE IF NOT EXISTS workout_records (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    exercise_type VARCHAR(50) NOT NULL,
    duration INTEGER NOT NULL,
    calories_burned INTEGER DEFAULT 0,
    heart_rate_avg INTEGER DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_user_date ON workout_records(user_id, date);
CREATE INDEX IF NOT EXISTS idx_date ON workout_records(date);
"""

