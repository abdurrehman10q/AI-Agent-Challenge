from enum import Enum

class Decision(str, Enum):
    APPROVE = "approve"
    FLAG = "flag"
    BLOCK = "block"
    ESCALATE = "escalate"

RISK_THRESHOLDS = {
    Decision.BLOCK: 0.8,
    Decision.ESCALATE: 0.6,
    Decision.FLAG: 0.4,
    Decision.APPROVE: 0.0,
}