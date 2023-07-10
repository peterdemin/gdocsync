import os
import tempfile


class PandocClient:
    def convert_rtf_to_rst(self, rtf_bytes: bytes) -> str:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_name = os.path.join(temp_dir, "source.rtf")
            target_name = os.path.join(temp_dir, "target.rst")
            with open(source_name, "wb") as f_in:
                f_in.write(rtf_bytes)
            os.system(f"pandoc -s {source_name} -o {target_name}")
            with open(target_name, "rt", encoding='utf-8') as f_out:
                return f_out.read()
