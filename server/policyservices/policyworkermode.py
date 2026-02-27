from enum import Enum

class PolicyWorkerMode(Enum):
    """
    Enum for file worker mode
    """

    CHECK_WRITE_PERMISSIONS = 1,
    CHECK_READ_PERMISSIONS = 2,
    CHECK_COPY_PERMISSIONS = 3,
    CHECK_MOVE_PERMISSIONS = 4,
    CHECK_CREATE_PERMISSIONS = 5,
    CHECK_DELETE_PERMISSIONS = 6,
    CHECK_RENAME_PERMISSIONS = 7
