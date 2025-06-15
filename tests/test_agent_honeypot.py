import pytest
from unittest.mock import patch
from backend.agent import agent_decision

@pytest.mark.asyncio
async def test_agent_honeypot_spawn():
    state = {"severity": 0.95, "src_ip": "1.2.3.4"}
    with patch("backend.actions.spawn_honeypot") as mock_spawn:
        result = agent_decision(state)
        mock_spawn.assert_called_once_with("1.2.3.4")
        assert result["action"] == "honeypot"
