import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    LEADER = "leader"
    REQUESTOR = "requestor"

class RequestStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
