"""Tests for nvidia_integration.py."""

import os
import unittest
from unittest.mock import MagicMock, patch

os.environ["TESTING"] = "1"

from nvidia_integration import NVIDIAIntegration  # noqa: E402,E403


def make_torch(cuda_available=False, cuda_version="11.8"):
    """Create a mock torch module."""
    tm = MagicMock()
    tm.cuda.is_available.return_value = cuda_available
    tm.version.cuda = cuda_version
    tm.__version__ = "2.0.0"
    tm.device.return_value = MagicMock()
    return tm


class TestNVIDIAInit(unittest.TestCase):
    """Test NVIDIAIntegration initialization."""

    def setUp(self):
        self._patches = []

    def tearDown(self):
        for p in self._patches:
            p.stop()

    def test_gpu_not_available(self):
        tm = make_torch(cuda_available=False)
        p = patch("nvidia_integration.torch", tm)
        p.start()
        self._patches.append(p)
        with patch("nvidia_integration.pynvml", None):
            ni = NVIDIAIntegration()
        self.assertFalse(ni.gpu_available)
        self.assertFalse(ni.blackwell_compatible)

    def test_gpu_available_blackwell_compatible(self):
        tm = make_torch(cuda_available=True, cuda_version="12.4")
        p = patch("nvidia_integration.torch", tm)
        p.start()
        self._patches.append(p)
        with patch("nvidia_integration.pynvml", None):
            ni = NVIDIAIntegration()
        self.assertTrue(ni.gpu_available)
        self.assertTrue(ni.blackwell_compatible)

    def test_gpu_available_not_blackwell(self):
        tm = make_torch(cuda_available=True, cuda_version="11.8")
        p = patch("nvidia_integration.torch", tm)
        p.start()
        self._patches.append(p)
        with patch("nvidia_integration.pynvml", None):
            ni = NVIDIAIntegration()
        self.assertTrue(ni.gpu_available)
        self.assertFalse(ni.blackwell_compatible)


class TestGetGpuInfo(unittest.TestCase):
    """Test get_gpu_info."""

    def setUp(self):
        self._patches = []

    def tearDown(self):
        for p in self._patches:
            p.stop()

    def test_get_gpu_info_no_nvml(self):
        tm = make_torch(cuda_available=False)
        p = patch("nvidia_integration.torch", tm)
        p.start()
        self._patches.append(p)
        with patch("nvidia_integration.pynvml", None):
            ni = NVIDIAIntegration()
        info = ni.get_gpu_info()
        self.assertFalse(info["gpu_available"])
        self.assertIn("device", info)

    def test_get_gpu_info_with_nvml(self):
        tm = make_torch(cuda_available=False)
        p = patch("nvidia_integration.torch", tm)
        p.start()
        self._patches.append(p)
        mp = MagicMock()
        mp.nvmlDeviceGetCount.return_value = 2
        mp.nvmlDeviceGetName.return_value = b"NVIDIA RTX"
        mp.nvmlDeviceGetMemoryInfo.return_value = MagicMock(used=1000, total=8000)
        mp.nvmlDeviceGetUtilizationRates.return_value = MagicMock(gpu=50, memory=40)
        with patch("nvidia_integration.pynvml", mp):
            ni = NVIDIAIntegration()
            ni.nvml_available = True
            info = ni.get_gpu_info()
        self.assertEqual(info["gpu_count"], 2)
        self.assertEqual(len(info["gpus"]), 2)
        self.assertEqual(info["gpus"][0]["name"], "NVIDIA RTX")

    def test_get_gpu_info_nvml_exception(self):
        tm = make_torch(cuda_available=False)
        p = patch("nvidia_integration.torch", tm)
        p.start()
        self._patches.append(p)
        mp = MagicMock()
        mp.nvmlDeviceGetCount.side_effect = Exception("NVML error")
        with patch("nvidia_integration.pynvml", mp):
            ni = NVIDIAIntegration()
            ni.nvml_available = True
            info = ni.get_gpu_info()
        self.assertNotIn("gpus", info)


class TestAllocateGpuResources(unittest.TestCase):
    """Test allocate_gpu_resources."""

    def setUp(self):
        self._patches = []

    def tearDown(self):
        for p in self._patches:
            p.stop()

    def test_allocate_gpu_not_available(self):
        tm = make_torch(cuda_available=False)
        p = patch("nvidia_integration.torch", tm)
        p.start()
        self._patches.append(p)
        with patch("nvidia_integration.pynvml", None):
            ni = NVIDIAIntegration()
        result = ni.allocate_gpu_resources(0)
        self.assertIsNone(result)

    def test_allocate_gpu_with_nvml(self):
        tm = make_torch(cuda_available=True, cuda_version="12.4")
        p = patch("nvidia_integration.torch", tm)
        p.start()
        self._patches.append(p)
        with patch("nvidia_integration.pynvml", MagicMock()):
            ni = NVIDIAIntegration()
            ni.nvml_available = True
            result = ni.allocate_gpu_resources(1)
        tm.cuda.set_device.assert_called_once()
        self.assertIsNotNone(result)

    def test_allocate_gpu_exception(self):
        tm = make_torch(cuda_available=True, cuda_version="12.4")
        tm.cuda.set_device.side_effect = Exception("CUDA error")
        p = patch("nvidia_integration.torch", tm)
        p.start()
        self._patches.append(p)
        with patch("nvidia_integration.pynvml", MagicMock()):
            ni = NVIDIAIntegration()
            ni.nvml_available = True
            result = ni.allocate_gpu_resources(0)
        self.assertIsNone(result)


class TestShutdown(unittest.TestCase):
    """Test log_project_status and shutdown."""

    def setUp(self):
        self._patches = []

    def tearDown(self):
        for p in self._patches:
            p.stop()

    def test_log_project_status(self):
        tm = make_torch(cuda_available=False)
        p = patch("nvidia_integration.torch", tm)
        p.start()
        self._patches.append(p)
        with patch("nvidia_integration.pynvml", None):
            ni = NVIDIAIntegration()
        with patch("builtins.print") as mp:
            ni.log_project_status("Test Project")
            mp.assert_called_once()
            self.assertIn("NVIDIA Project Control Log", str(mp.call_args))

    def test_shutdown_with_nvml(self):
        tm = make_torch(cuda_available=False)
        p = patch("nvidia_integration.torch", tm)
        p.start()
        self._patches.append(p)
        mp = MagicMock()
        with patch("nvidia_integration.pynvml", mp):
            ni = NVIDIAIntegration()
            ni.nvml_available = True
            ni.shutdown()
        mp.nvmlShutdown.assert_called_once()

    def test_shutdown_without_nvml(self):
        tm = make_torch(cuda_available=False)
        p = patch("nvidia_integration.torch", tm)
        p.start()
        self._patches.append(p)
        with patch("nvidia_integration.pynvml", None):
            ni = NVIDIAIntegration()
            ni.nvml_available = False
            ni.shutdown()


class TestNvmlInit(unittest.TestCase):
    """Test _init_nvml edge cases."""

    def setUp(self):
        self._patches = []

    def tearDown(self):
        for p in self._patches:
            p.stop()

    def test_init_nvml_testing_mode(self):
        tm = make_torch(cuda_available=False)
        p = patch("nvidia_integration.torch", tm)
        p.start()
        self._patches.append(p)
        mp = MagicMock()
        with patch("nvidia_integration.pynvml", mp):
            with patch.dict("os.environ", {"TESTING": "1"}):
                ni = NVIDIAIntegration()
        self.assertFalse(ni.nvml_available)

    def test_init_nvml_success(self):
        tm = make_torch(cuda_available=False)
        p = patch("nvidia_integration.torch", tm)
        p.start()
        self._patches.append(p)
        mp = MagicMock()
        mp.nvmlInit.return_value = None
        with patch("nvidia_integration.pynvml", mp):
            with patch.dict("os.environ", {"TESTING": "", "UNIT_TEST": ""}):
                ni = NVIDIAIntegration()
        self.assertTrue(ni.nvml_available)

    def test_init_nvml_library_not_found(self):
        tm = make_torch(cuda_available=False)
        p = patch("nvidia_integration.torch", tm)
        p.start()
        self._patches.append(p)
        mp = MagicMock()
        mp.NVMLError_LibraryNotFound = type("E", (Exception,), {})
        mp.nvmlInit.side_effect = mp.NVMLError_LibraryNotFound("not found")
        with patch("nvidia_integration.pynvml", mp):
            with patch.dict("os.environ", {"TESTING": "", "UNIT_TEST": ""}):
                ni = NVIDIAIntegration()
        self.assertFalse(ni.nvml_available)

    def test_init_nvml_general_exception(self):
        tm = make_torch(cuda_available=False)
        p = patch("nvidia_integration.torch", tm)
        p.start()
        self._patches.append(p)
        mp = MagicMock()
        mp.NVMLError_LibraryNotFound = type("E", (Exception,), {})
        mp.nvmlInit.side_effect = RuntimeError("Init failed")
        with patch("nvidia_integration.pynvml", mp):
            with patch.dict("os.environ", {"TESTING": "", "UNIT_TEST": ""}):
                ni = NVIDIAIntegration()
        self.assertFalse(ni.nvml_available)


if __name__ == "__main__":
    unittest.main()
