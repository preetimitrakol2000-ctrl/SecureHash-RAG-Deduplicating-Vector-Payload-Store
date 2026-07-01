import ctypes
import os
import sys
import hashlib

class HashBridge:
    def __init__(self):
        if not os.path.exists("./libhash.so") and not os.path.exists("./libhash.dll"):
            if sys.platform.startswith("win"):
                os.system("gcc -shared -o libhash.dll dedup_hash.c")
                lib_path = "./libhash.dll"
            else:
                os.system("gcc -shared -fPIC -o libhash.so dedup_hash.c")
                lib_path = "./libhash.so"
        else:
            lib_path = "./libhash.dll" if sys.platform.startswith("win") else "./libhash.so"

        self.lib = ctypes.CDLL(lib_path)
        self.lib.init_table.restype = ctypes.c_void_p
        self.lib.register_document_payload.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
        self.lib.register_document_payload.restype = ctypes.c_int
        self.lib.clear_table.argtypes = [ctypes.c_void_p]
        
        self.table_ptr = self.lib.init_table()

    def process_and_deduplicate(self, raw_text: str, doc_id: int) -> int:
        # Generate SHA-256 string footprint signature values out of python pipeline strings
        text_hash = hashlib.sha256(raw_text.encode('utf-8')).hexdigest()
        return self.lib.register_document_payload(self.table_ptr, text_hash.encode('utf-8'), doc_id)

    def __del__(self):
        if hasattr(self, 'lib') and self.table_ptr:
            self.lib.clear_table(self.table_ptr)
