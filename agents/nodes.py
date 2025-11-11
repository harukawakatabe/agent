"""Agent节点定义 - 定义LangGraph中的各个节点"""
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import config
from utils.prompts import QUERY_ROUTER_PROMPT, ANALYSIS_PROMPT, RESPONSE_PROMPT
from tools.database_tool import DATABASE_TOOLS
from tools.analysis_tool import ANALYSIS_TOOLS


# 初始化LLM
llm = ChatOpenAI(
    model=config.OPENAI_MODEL,
    temperature=config.AGENT_CONFIG["temperature"],
    api_key=config.OPENAI_API_KEY,
    base_url=config.OPENAI_BASE_URL
)


def query_router_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    查询路由节点 - 识别用户查询意图
    
    Args:
        state: Agent状态字典
    
    Returns:
        更新后的状态，包含intent字段
    """
    query = state.get("query", "")
    
    # 使用LLM识别意图
    prompt = QUERY_ROUTER_PROMPT.format_messages(query=query)
    response = llm.invoke(prompt)
    
    intent = response.content.strip().lower()
    
    # 简单的意图映射
    if "今天" in query or "今日" in query:
        intent = "today_performance"
    elif "历史" in query or "过去" in query or "最近" in query:
        intent = "historical_analysis"
    elif "对比" in query or "比较" in query:
        intent = "comparison"
    elif "趋势" in query:
        intent = "trend_analysis"
    else:
        intent = "general_query"
    
    return {
        **state,
        "intent": intent
    }


def database_query_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    数据库查询节点 - 根据意图查询数据库
    
    Args:
        state: Agent状态字典
    
    Returns:
        更新后的状态，包含data字段
    """
    intent = state.get("intent", "")
    query = state.get("query", "")
    
    data = ""
    
    try:
        if intent == "today_performance":
            # 使用工具获取今天的汇总
            result = DATABASE_TOOLS[1].invoke({"user_id": 1})  # get_today_workout_summary
            data = result
        
        elif intent == "historical_analysis":
            # 查询历史记录
            result = DATABASE_TOOLS[0].invoke({
                "user_id": 1,
                "limit": 50
            })  # query_workout_records
            data = result
        
        elif intent == "trend_analysis":
            # 获取统计数据
            result = DATABASE_TOOLS[2].invoke({
                "user_id": 1,
                "days": 7
            })  # get_workout_statistics
            data = result
        
        else:
            # 默认查询最近的记录
            result = DATABASE_TOOLS[0].invoke({
                "user_id": 1,
                "limit": 20
            })
            data = result
    
    except Exception as e:
        data = f"查询数据时出错: {str(e)}"
    
    return {
        **state,
        "data": data
    }


def analysis_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    数据分析节点 - 对查询到的数据进行分析
    
    Args:
        state: Agent状态字典
    
    Returns:
        更新后的状态，包含analysis字段
    """
    data = state.get("data", "")
    intent = state.get("intent", "")
    
    analysis = ""
    
    try:
        if intent == "trend_analysis" or intent == "historical_analysis":
            # 使用分析工具
            if data and data != "未找到匹配的运动记录":
                result = ANALYSIS_TOOLS[0].invoke({"data": data})  # analyze_workout_trends
                analysis = result
            else:
                analysis = "数据不足，无法进行趋势分析"
        
        elif intent == "comparison":
            # 对比分析需要特殊处理
            analysis = "对比分析功能（需要两个时间段的数据）"
        
        else:
            # 使用LLM进行一般性分析
            if data:
                prompt = ANALYSIS_PROMPT.format_messages(data=data)
                response = llm.invoke(prompt)
                analysis = response.content
            else:
                analysis = "暂无数据可分析"
    
    except Exception as e:
        analysis = f"分析过程中出错: {str(e)}"
    
    return {
        **state,
        "analysis": analysis
    }


def response_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    回复生成节点 - 生成最终的用户回复
    
    Args:
        state: Agent状态字典
    
    Returns:
        更新后的状态，包含response字段
    """
    query = state.get("query", "")
    data = state.get("data", "")
    analysis = state.get("analysis", "")
    
    # 构建消息历史
    messages = [
        HumanMessage(content=f"用户查询：{query}"),
    ]
    
    if data:
        messages.append(AIMessage(content=f"查询到的数据：\n{data}"))
    
    if analysis:
        messages.append(AIMessage(content=f"分析结果：\n{analysis}"))
    
    try:
        # 使用LLM生成回复
        prompt = RESPONSE_PROMPT.format_messages(messages=messages)
        response = llm.invoke(prompt)
        
        final_response = response.content
    
    except Exception as e:
        final_response = f"生成回复时出错: {str(e)}"
    
    return {
        **state,
        "response": final_response
    }

