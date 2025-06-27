from src.lib.g2p_id import G2P
import subprocess
import html

class TTSService:
    @staticmethod
    def get_response(text: str):
        g2p = G2P()

        text = html.unescape(text)
        text_to_tts = g2p(text)

        command = [
            "tts",
            "--text", text_to_tts,
            "--model_path", "./checkpoint_1260000-inference.pth",
            "--config_path", "./config.json",
            "--speaker_idx", "wibowo",
            "--out_path", "./output.wav"
        ]
        result = subprocess.run(command, capture_output=True, text=True)
    
        if result.returncode != 0:
            return ""
        else:
            return "./output.wav"
