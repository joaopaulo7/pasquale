import json
from openai import OpenAI
from difflib import Differ
from pprint import pprint

class Pasquale:
    def __init__(self, prompts_file="prompts/base_prompts.json"):
        with open("creds.json") as in_file:
            cred = json.load(in_file)
        self.client = OpenAI(**cred)
        
        with open(prompts_file) as in_file:
            self.prompts = json.load(in_file)
        
        self.messages = []
    
    
    def get_corrections(text1, text2):
        d = Differ()
        result = list(d.compare(text1, text2))
        corrections = []

        text1_i = 0
        text2_i = 0

        added_s = []
        removed_s = []

        i = 0
        start_i = -1
        char_start = 0
        char_i = 0
        while i < len(result):
            if result[i][0] == '+':
                if start_i == -1:
                    start_i = text1_i
                    char_start = char_i
                added_s.append(text2[text2_i])
                text2_i += 1
            
            elif result[i][0] == '-':
                if start_i == -1:
                    start_i = text1_i
                    char_start = char_i
                removed_s.append(text1[text1_i])
                
                char_i += len(text1[text1_i])+1
                text1_i += 1
                
            if result[i][0] == ' ' or i == len(result)-1:
                if start_i != -1:
                    aux_dic = {}
                    aux_dic['added']    = " ".join(added_s)
                    aux_dic['removed']  = " ".join(removed_s)
                    aux_dic['start']    = start_i
                    aux_dic['char_start'] = char_start
                    aux_dic['len'] = len(" ".join(removed_s))
                    aux_dic['context1'] = " ".join(text1[max(0, start_i-2):min(text1_i+2, len(text1))])
                    aux_dic['context2'] = " ".join(text1[max(0, start_i-2):start_i]+
                                            added_s+text1[text1_i:min(text1_i+2, len(text1))])
                    
                    # if just adds, add to the spacebar before
                    if aux_dic['len'] == 0:
                        aux_dic['char_start'] += -1
                        aux_dic['len'] = 1
                    corrections.append(aux_dic)
                    start_i = -1
                    added_s.clear()
                    removed_s.clear()
                
                
                if i != len(result)-1:
                    char_i += len(text1[text1_i])+1
                    text1_i += 1
                    text2_i += 1
                
            i += 1
            
        return corrections
    
        
    
    def ask_llm_check(self, text, language, genres, model, temperature=0.0, max_tokens=8000, persistent=True):
        system_prompt = self.prompts[language]['system']+"\n\ngenres: "+genres
        text = self.prompts[language]['text']+text
        
        self.messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ]
        
        completion = self.client.chat.completions.create(
            model = model,
            messages = self.messages,
            max_completion_tokens = max_tokens,
            temperature = temperature,
        )
        
        if persistent:
            self.messages.append(completion.choices[0].message)
        
        return completion.choices[0].message.content.strip("\n")
    
    
    def ask_llm_reason(self, correction, language, model, temperature=0.0, max_tokens=8000, persistent=False):
        text  = self.prompts[language]['reason'].format(
                    removed  = correction['removed'],
                    added    = correction['added'],
                    context1 = correction['context1'],
                    context2 = correction['context2'])
        
        completion = self.client.chat.completions.create(
            model = model,
            messages = self.messages+[{"role": "user", "content": text}],
            max_completion_tokens = max_tokens,
            temperature = temperature,
        )
        
        if persistent:
            self.messages.append({"role": "user", "content": text})
            self.messages.append(completion.choices[0].message)
        
        return completion.choices[0].message.content
    
    
    def check(self, text, language, genres, model="gemma3:4b-it-qat", temperature=0.0, max_tokens=7200):
        cor_text = self.ask_llm_check(text, language, genres, model, temperature, max_tokens)
        corrections = Pasquale.get_corrections(text.split(" "), cor_text.split(" "))
        
        for correction in corrections:
            correction['reason'] = self.ask_llm_reason(correction, language, model, temperature, max_tokens)
        
        return corrections

