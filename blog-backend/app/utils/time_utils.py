"""
时间相关的工具函数
"""
from datetime import datetime, timedelta

def format_relative_time_zh(delta):
    """
    将时间差转换为中文相对时间表示
    
    Args:
        delta: 时间差（datetime.timedelta对象）
        
    Returns:
        str: 中文相对时间表示
    """
    seconds = int(abs(delta.total_seconds()))
    
    # 判断是过去还是将来
    is_past = delta.total_seconds() > 0
    
    # 计算各个时间单位
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24
    months = days // 30
    years = days // 365
    
    # 根据时间差返回相应的中文表示
    if seconds < 10:
        return "刚刚" if is_past else "即将"
    elif seconds < 60:
        return f"{seconds}秒前" if is_past else f"{seconds}秒后"
    elif minutes < 60:
        return f"{minutes}分钟前" if is_past else f"{minutes}分钟后"
    elif hours < 24:
        return f"{hours}小时前" if is_past else f"{hours}小时后"
    elif days < 30:
        return f"{days}天前" if is_past else f"{days}天后"
    elif months < 12:
        return f"{months}个月前" if is_past else f"{months}个月后"
    else:
        return f"{years}年前" if is_past else f"{years}年后"

def get_relative_time_zh(dt, now=None):
    """
    获取相对于当前时间的中文相对时间表示
    
    Args:
        dt: 要计算相对时间的datetime对象
        now: 当前时间，默认为None，表示使用当前时间
        
    Returns:
        str: 中文相对时间表示
    """
    if now is None:
        now = datetime.now(dt.tzinfo)
    
    # 计算时间差
    delta = now - dt
    
    return format_relative_time_zh(delta)
