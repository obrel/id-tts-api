from src.lib.g2p_id import G2P
from src.lib.num2words import num2words
import subprocess
import html

class TTSService:
    @staticmethod
    def get_response(text: str, audio: str):
        g2p = G2P()

        text = html.unescape(text)
        text_to_tts = g2p(text)
        text_to_tts = num2words.convert(text_to_tts)

        command = [
            "tts",
            "--text", text_to_tts,
            "--model_path", "./checkpoint_1260000-inference.pth",
            "--config_path", "./config.json",
            "--speaker_idx", audio,
            "--out_path", "./output.wav"
        ]
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            return ""
        else:
            return "./output.wav"
