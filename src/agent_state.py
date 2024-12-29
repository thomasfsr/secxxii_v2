from typing import TypedDict

class AgentState(TypedDict):
    current_user: str
    question: str
    sql_query: str
    query_result: str
    query_rows: list
    attempts: int
    relevance: str
    sql_error: bool