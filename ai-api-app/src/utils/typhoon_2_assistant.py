# นำเข้าโมดูลที่ต้องการ
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM 


# วิธีใช้งาน
# from src.utils.typhoon_2_assistant import Typhoon2Assistant
# assistant = Typhoon2Assistant()
# assistant.ask("ใส่ข้อความที่ต้องการถามที่นี่")

class Typhoon2Assistant:
    def __init__(self,
                 system_content="You are a friendly assistant. Answer the question based only on the following context. If you don't know the answer, then reply, No Context available for this question.",
                 model_id="scb10x/llama3.2-typhoon2-1b-instruct",
                 ):
        self.system_content = system_content
        self.model_id = model_id
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

    # def ask_stream(self, prompt: str):
    #     # เตรียมข้อความนำเข้า
    #     messages = [
    #         {"role": "system", "content": self.system_content},
    #         {"role": "user", "content": prompt}
    #     ]
    #     # แปลงข้อความเป็น token (คืนค่าเป็น tensor โดยตรง)
    #     input_ids = self.tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to(self.model.device)
        
    #     # สร้าง attention_mask จาก input_ids (1 สำหรับ token จริง, 0 สำหรับ padding)
    #     attention_mask = (input_ids != self.tokenizer.pad_token_id).long().to(self.model.device)
        
    #     # กำหนดพารามิเตอร์สำหรับการสร้างข้อความ
    #     terminators = [self.tokenizer.eos_token_id, self.tokenizer.convert_tokens_to_ids("<|eot_id|>")]
        
    #     # สร้างข้อความตอบกลับแบบ chunked
    #     outputs = self.model.generate(
    #         input_ids,
    #         attention_mask=attention_mask,  # ส่ง attention_mask เข้าไป
    #         max_new_tokens=512,
    #         eos_token_id=terminators,
    #         do_sample=True,
    #         temperature=0.7,
    #         top_p=0.95,
    #         pad_token_id=self.tokenizer.pad_token_id  # กำหนด pad_token_id อย่างชัดเจน
    #     )
        
    #     # แปลงผลลัพธ์กลับเป็นข้อความแบบ chunked
    #     response = outputs[0][input_ids.shape[-1]:]
    #     answer = self.tokenizer.decode(response, skip_special_tokens=True)
        
    #     # แบ่งข้อความเป็น chunk เล็กๆ และ yield แต่ละ chunk
    #     chunk_size = 20  # ขนาดของ chunk ที่ต้องการ
    #     for i in range(0, len(answer), chunk_size):
    #         yield answer[i:i + chunk_size]
    
    def ask_stream(self, prompt: str):
        # เตรียมข้อความนำเข้า
        messages = [
            {"role": "system", "content": self.system_content},
            {"role": "user", "content": prompt}
        ]
        input_ids = self.tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to(self.model.device)
        attention_mask = (input_ids != self.tokenizer.pad_token_id).long().to(self.model.device)
        
        # กำหนดพารามิเตอร์สำหรับการสร้างข้อความ
        terminators = [self.tokenizer.eos_token_id, self.tokenizer.convert_tokens_to_ids("<|eot_id|>")]
        
        # ใช้ torch.no_grad() เพื่อประหยัดหน่วยความจำ
        with torch.no_grad():
            for token in self.model.generate(
                input_ids,
                attention_mask=attention_mask,
                max_new_tokens=512,
                eos_token_id=terminators,
                do_sample=True,
                temperature=0.7,
                top_p=0.95,
                pad_token_id=self.tokenizer.pad_token_id,
                return_dict_in_generate=False,  # เพื่อให้ได้ token-by-token
                num_return_sequences=1,
            )[0][input_ids.shape[-1]:]:  # เริ่มจาก token ใหม่ที่สร้าง
                # แปลง token เป็นข้อความและ yield ทันที
                chunk = self.tokenizer.decode([token.item()], skip_special_tokens=True)
                if chunk:  # เฉพาะ chunk ที่ไม่ว่างเปล่า
                    yield chunk

