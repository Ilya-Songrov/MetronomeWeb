from dataclasses import dataclass, field, asdict

@dataclass
class JSON_RPC_BASE:
    jsonrpc: str    = "2.0"
    id: int         = None

@dataclass
class JSON_RPC_RQ(JSON_RPC_BASE):
    method: str     = ""
    params: dict    = field(default_factory=dict)

    def __str__(self):
        return f'JSON_RPC_RQ<{self.jsonrpc=},{self.method=},{self.params=},{self.id=}>'

@dataclass
class JSON_RPC_RS(JSON_RPC_BASE):
    result: dict    = field(default_factory=dict)

    def __str__(self):
        return f'JSON_RPC_RS<{self.jsonrpc=},{self.result=},{self.id}>'
    