def fix_thai_text(text):
        # แผนที่สำหรับแทนที่ตัวอักษรที่เสียหาย
        replacements = {
            "": "้",  # วรรณยุกต์ไม้โท
            "": "้",  # วรรณยุกต์ไม้โท
            "": "่",  # วรรณยุกต์ไม้เอก (บางกรณีอาจซ้ำ)
            "": "์",  # วรรณยุกต์การันต์
            "": "็",  # วรรณยุกต์ไม้ตรี
            "":"็", # วรรณยุกต์ไตคู้
            "": "๋",  # วรรณยุกต์ไม้จัดตาวา
            "ํ": "ำ",  # สระอำ
            "":"ี", # สระอี
            "":"ั", # ไม้หันอากาศ
            "":"่", # ไม้เอก
            "":"ิ", # สระอิ
            # เพิ่มตามตัวอักษรที่เสียหายในข้อมูลของคุณ
        }
        for wrong, correct in replacements.items():
            text = text.replace(wrong, correct)
        return text