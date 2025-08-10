from io import BytesIO
from .policyworkerstatus import PolicyWorkerStatus


class PolicyWorkerResult:
    def __init__(self):
        self.data: BytesIO = BytesIO()
        self.status: PolicyWorkerStatus = None