# นำเข้าโมดูลที่ต้องการ
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM 


# วิธีใช้งาน
# from src.utils.typhoon_2_assistant import Typhoon2Assistant
# assistant = Typhoon2Assistant()
# assistant.ask("ใส่ข้อความที่ต้องการถามที่นี่")

class Typhoon2Assistant:
    def __init__(self,system_content="You are a friendly assistant. Answer the question based only on the following context. If you don't know the answer, then reply, No Context available for this question."):
        self.system_content = system_content
        self.model_id = "scb10x/llama3.2-typhoon2-1b-instruct"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_id, torch_dtype=torch.bfloat16)
        # self.model = AutoModelForCausalLM.from_pretrained(self.model_id, torch_dtype=torch.bfloat16, device_map="auto")

    def ask(self, prompt: str):
        # เตรียมข้อความนำเข้า
        messages = [
            {"role": "system", "content": self.system_content},
            {"role": "user", "content": prompt}
        ]
        # แปลงข้อความเป็น token (คืนค่าเป็น tensor โดยตรง)
        input_ids = self.tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to(self.model.device)
        
        # สร้าง attention_mask จาก input_ids (1 สำหรับ token จริง, 0 สำหรับ padding)
        attention_mask = (input_ids != self.tokenizer.pad_token_id).long().to(self.model.device)
        
        # กำหนดพารามิเตอร์สำหรับการสร้างข้อความ
        terminators = [self.tokenizer.eos_token_id, self.tokenizer.convert_tokens_to_ids("<|eot_id|>")]
        
        # สร้างข้อความตอบกลับ
        outputs = self.model.generate(
            input_ids,
            attention_mask=attention_mask,  # ส่ง attention_mask เข้าไป
            max_new_tokens=512,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.7,
            top_p=0.95,
            pad_token_id=self.tokenizer.pad_token_id  # กำหนด pad_token_id อย่างชัดเจน
        )
        
        # แปลงผลลัพธ์กลับเป็นข้อความ
        response = outputs[0][input_ids.shape[-1]:]
        answer = self.tokenizer.decode(response, skip_special_tokens=True)
        return answer

