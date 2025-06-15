from langgraph import StateMachine
from .actions import spawn_honeypot, quarantine_ip

THRESHOLD = 0.8

def agent_decision(state):
    severity = state.get("severity", 0)
    src_ip = state.get("src_ip")
    if severity > THRESHOLD:
        spawn_honeypot(src_ip)
        return {"action": "honeypot", "ip": src_ip}
    else:
        # Just log
        return {"action": "log", "ip": src_ip}

agent_sm = StateMachine(
    states=["idle", "decision"],
    transitions={
        "idle": {"on_event": "decision"},
        "decision": {"on_done": "idle"}
    },
    on_enter={
        "decision": agent_decision
    }
)
