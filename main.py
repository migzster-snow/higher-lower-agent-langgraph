from typing import Dict, TypedDict, List
from langgraph.graph import StateGraph, START, END
import random

class AgentState(TypedDict):
    secret_number: int
    name: str
    lower_bound: int
    upper_bound: int
    numbers: List[int]
    counter: int
    message: str

def greeting_node(state: AgentState) -> AgentState:
    state['secret_number'] = random.randint(state['lower_bound'], state['upper_bound'])
    state['message'] = f"Hello, your name is {state['name']}. The secret number is {state['secret_number']}. The random numbers between {state['lower_bound']} and {state['upper_bound']} are:"
    state['counter'] = 0
    return state

def random_node(state: AgentState) -> AgentState:
    random_number = random.randint(state['lower_bound'], state['upper_bound'])
    state['numbers'].append(random_number)
    state['message'] += f" {random_number}"
    if random_number < state['secret_number']:
        state['lower_bound'] = random_number + 1
    else:
        state['upper_bound'] = random_number - 1
    state['counter'] += 1
    return state

def loop_condition(state: AgentState) -> AgentState:
    if state['counter'] >= 7 or state['secret_number'] in state['numbers']:
        return 'exit'
    return 'loop'

graph = StateGraph(AgentState)
graph.add_node("greeting", greeting_node)
graph.add_node("random", random_node)
graph.add_edge(START, "greeting")
graph.add_edge("greeting", "random")
graph.add_conditional_edges(
    "random",
    loop_condition,
    {
        "loop": "random",
        "exit": END
    }
)

app = graph.compile()

result = app.invoke({
    "name": "Jonah",
    "lower_bound": 1,
    "upper_bound": 10,
    "numbers": [],
    "counter": 0,
})

print("Result:", result['message'])

# Result: Hello, your name is Jonah. The secret number is 8. The random numbers between 1 and 10 are: 6 10 9 8