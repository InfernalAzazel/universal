import platform
import psutil
from fastapi import APIRouter, Depends

from app.models.common import ResponseModel
from app.utils.custom_response import ResponseMessages
from app.utils.dependencies import get_language

router = APIRouter(
    prefix="/api",
    tags=["private admin"],
    responses={
        200: {"model": ResponseModel},
        422: {"model": ResponseModel}
    }
)


def convert_bytes(n):
    # 1024 bytes = 1 kilobyte
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']:
        if n < 1024:
            return f"{n:.2f} {unit}"
        n /= 1024
    return f"{n:.2f} YB"


@router.get("/v1/private/admin/dashboard/monitor")
def read_system_info(
        language: str = Depends(get_language),
        # _: UserResponseModel = Depends(auto_current_user_permission),
):
    system_info = {
        # 操作系统和Python的相关信息
        "os_info": {
            "operating_system": platform.system(),
            "os_version_detail": platform.version(),
            "os_release": platform.release(),
            "computer_network_name": platform.node(),
            "processor_info": platform.processor(),
            "python_version": platform.python_version(),
        },
        # 当前CPU使用率百分比
        "cpu_usage": {
            "logical_cpus_total": f"{psutil.cpu_count()}",
            "physical_cpus_total": f"{psutil.cpu_count()}",
            "percent": f"{psutil.cpu_percent()}%",
        },
        # 总内存，已使用内存及使用率
        "memory_usage": {
            "total": convert_bytes(psutil.virtual_memory().total),
            "used": convert_bytes(psutil.virtual_memory().used),
            "percent": f"{psutil.virtual_memory().percent}%"
        },
        # 网络发送与接收的数据量
        "network_traffic": {
            "bytes_sent": convert_bytes(psutil.net_io_counters().bytes_sent),
            "bytes_recv": convert_bytes(psutil.net_io_counters().bytes_recv),
        },
        # 各个磁盘分区的总大小，已使用大小及使用率
        "disk_usage": [{
            "device": disk.device,
            "mountpoint": disk.mountpoint,
            "total": convert_bytes(psutil.disk_usage(disk.mountpoint).total),
            "used": convert_bytes(psutil.disk_usage(disk.mountpoint).used),
            "percent": f"{psutil.disk_usage(disk.mountpoint).percent}%",
        } for disk in psutil.disk_partitions()],

    }
    return ResponseMessages(locale=language, data=system_info)