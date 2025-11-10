"""健身记录分析Agent - 使用LangGraph构建"""
from typing import Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
try:
    from langchain_core.messages import BaseMessage
except ImportError:
    from langchain.schema import BaseMessage
import config
from agents.nodes import (
    query_router_node,
    database_query_node,
    analysis_node,
    response_node
)


# 定义Agent状态
class AgentState(TypedDict):
    """Agent状态定义"""
    messages: Annotated[list[BaseMessage], add_messages]
    query: str
    intent: str
    data: str
    analysis: str
    response: str


class FitnessAgent:
    """健身记录分析Agent"""
    
    def __init__(self):
        """初始化Agent"""
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """
        构建LangGraph状态图
        
        Returns:
            配置好的StateGraph实例
        """
        # 创建状态图
        workflow = StateGraph(AgentState)
        
        # 添加节点
        workflow.add_node("query_router", query_router_node)
        workflow.add_node("database_query", database_query_node)
        workflow.add_node("analysis", analysis_node)
        workflow.add_node("response", response_node)
        
        # 定义边和条件路由
        workflow.set_entry_point("query_router")
        
        # 从query_router到database_query
        workflow.add_edge("query_router", "database_query")
        
        # 从database_query到analysis
        workflow.add_edge("database_query", "analysis")
        
        # 从analysis到response
        workflow.add_edge("analysis", "response")
        
        # 从response到END
        workflow.add_edge("response", END)
        
        # 编译图
        app = workflow.compile()
        
        return app
    
    def invoke(self, query: str, user_id: int = 1) -> str:
        """
        执行Agent推理
        
        Args:
            query: 用户查询
            user_id: 用户ID
        
        Returns:
            Agent生成的回复
        """
        # 初始化状态
        initial_state: AgentState = {
            "messages": [],
            "query": query,
            "intent": "",
            "data": "",
            "analysis": "",
            "response": ""
        }
        
        # 运行Agent
        try:
            result = self.graph.invoke(initial_state)
            return result.get("response", "抱歉，无法生成回复")
        except Exception as e:
            return f"Agent执行出错: {str(e)}"
    
    def stream(self, query: str, user_id: int = 1):
        """
        流式执行Agent推理（用于实时显示过程）
        
        Args:
            query: 用户查询
            user_id: 用户ID
        
        Yields:
            每个节点的执行结果
        """
        initial_state: AgentState = {
            "messages": [],
            "query": query,
            "intent": "",
            "data": "",
            "analysis": "",
            "response": ""
        }
        
        try:
            for event in self.graph.stream(initial_state):
                yield event
        except Exception as e:
            yield {"error": str(e)}


# 创建全局Agent实例
fitness_agent = FitnessAgent()

