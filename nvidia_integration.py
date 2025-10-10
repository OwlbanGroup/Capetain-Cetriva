import torch
import logging
from typing import Dict, Any, Optional
import pynvml

logger = logging.getLogger(__name__)

class NVIDIAIntegration:
    """
    Handles NVIDIA Blackwell integration for GPU acceleration, monitoring, and control.
    Provides visibility into GPU resources and project management on NVIDIA platforms.
    """

    def __init__(self):
        self.gpu_available = torch.cuda.is_available()
        self.device = torch.device("cuda" if self.gpu_available else "cpu")
        self.blackwell_compatible = self._check_blackwell_compatibility()
        self._init_nvml()

    def _init_nvml(self):
        """Initialize NVIDIA Management Library for monitoring."""
        try:
            pynvml.nvmlInit()
            self.nvml_available = True
            logger.info("NVIDIA NVML initialized for GPU monitoring.")
        except Exception as e:
            self.nvml_available = False
            logger.warning(f"NVML initialization failed: {e}. GPU monitoring limited.")

    def _check_blackwell_compatibility(self) -> bool:
        """Check if CUDA version supports Blackwell (requires CUDA 12.4+)."""
        if not self.gpu_available:
            return False
        cuda_version = torch.version.cuda
        if cuda_version:
            major, minor = map(int, cuda_version.split('.')[:2])
            compatible = (major > 12) or (major == 12 and minor >= 4)
            logger.info(f"CUDA version {cuda_version} - Blackwell compatible: {compatible}")
            return compatible
        return False

    def get_gpu_info(self) -> Dict[str, Any]:
        """Get detailed GPU information for visibility and control."""
        info = {
            "gpu_available": self.gpu_available,
            "device": str(self.device),
            "blackwell_compatible": self.blackwell_compatible,
            "cuda_version": torch.version.cuda,
            "pytorch_version": torch.__version__,
        }
        if self.nvml_available:
            try:
                device_count = pynvml.nvmlDeviceGetCount()
                info["gpu_count"] = device_count
                gpus = []
                for i in range(device_count):
                    handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                    name = pynvml.nvmlDeviceGetName(handle)
                    memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                    utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    gpus.append({
                        "index": i,
                        "name": name.decode('utf-8') if isinstance(name, bytes) else name,
                        "memory_used": memory_info.used,
                        "memory_total": memory_info.total,
                        "utilization_gpu": utilization.gpu,
                        "utilization_memory": utilization.memory,
                    })
                info["gpus"] = gpus
            except Exception as e:
                logger.error(f"Error retrieving GPU info: {e}")
        return info

    def allocate_gpu_resources(self, gpu_id: int = 0) -> Optional[torch.device]:
        """Allocate specific GPU for project control."""
        if not self.gpu_available or not self.nvml_available:
            logger.warning("GPU allocation not available.")
            return None
        try:
            device = torch.device(f"cuda:{gpu_id}")
            torch.cuda.set_device(device)
            logger.info(f"Allocated GPU {gpu_id} for project.")
            return device
        except Exception as e:
            logger.error(f"Failed to allocate GPU {gpu_id}: {e}")
            return None

    def log_project_status(self, project_name: str = "Capetain-Cetriva"):
        """Log project status on NVIDIA resources for visibility."""
        info = self.get_gpu_info()
        logger.info(f"Project '{project_name}' NVIDIA Status: {info}")
        # Placeholder for Fleet Command API integration
        # e.g., api_call to NVIDIA Fleet Command for remote monitoring
        print(f"NVIDIA Project Control Log: {info}")  # For user visibility

    def shutdown(self):
        """Shutdown NVIDIA resources."""
        if self.nvml_available:
            pynvml.nvmlShutdown()
            logger.info("NVIDIA NVML shutdown.")

# Singleton instance for global use
nvidia_integration = NVIDIAIntegration()
