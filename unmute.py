from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import ctypes

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_interface = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))

volume_interface.SetMute(0, None)
volume_interface.SetMasterVolumeLevelScalar(0.1, None)
print("✅ Should be unmuted now at 10% volume.")
