import json
import os
import warnings

from openai import OpenAI
from difflib import Differ
from pprint import pprint

class Pasquale:
    
    prompt_types = ("system", "reason", "text")
    
    def __init__(self, prompts_folder="prompts", config_file="config.json"):
        with open(config_file) as in_file:
            config_json = json.load(in_file)
        
        self.client = OpenAI(**config_json['creds'])
        
        self.config = config_json['config']        
        
        self.model_families = set(next(os.walk(prompts_folder))[1])
        
        self.messages = []
        
        self.prompts = {}
        self._setup_prompt_family("base", prompts_folder)
        for family in self.model_families:
            if family == "base":
                pass
            self._setup_prompt_family(family, prompts_folder)
    
    
    def _setup_prompt_family(self, family, prompts_folder):
        if  not os.path.exists(f"{prompts_folder}/{family}") and family == "base":
            raise  FileNotFoundError(f"No prompts for base family found. Aborting...")
        
        prompt = {}
        for language in os.listdir(prompts_folder + "/" + family):
            prompt[language] = self._setup_prompt_language(family, prompts_folder, language)
        self.prompts[family] = prompt


    def _setup_prompt_language(self, family, prompts_folder, language):
        language_prompt = {}
        for p_type in self.prompt_types:
            language_prompt[p_type] = self._setup_prompt_type(family, prompts_folder, language, p_type)
        
        return language_prompt


    def _setup_prompt_type(self, family, prompts_folder, language, p_type):
        file_name = f"{prompts_folder}/{family}/{language}/{p_type}.md"
        try:
            with open(file_name) as in_file:
                return in_file.read()
        except FileNotFoundError as e:
            if family == "base":
                raise  FileNotFoundError(f"Base {p_type} prompt for language {language} missing. Aborting...") from e
            else:
                warnings.warn(f"""No {p_type} prompt for family '{family}' found.
                    Pasquale will use base prompts instead.""")
                return self.prompts['base'][language][p_type]
                    
        return language_prompt
    
    
    def _get_corrections(text1, text2):
        d = Differ()
        result = list(d.compare(text1, text2))
        corrections = []

        added_s = []
        removed_s = []
        
        i = 0
        start_i = -1
        text1_i = 0
        text2_i = 0
        char_start = 0
        char_i = 0
        while i < len(result):
            if result[i][0] == "+":
                if start_i == -1:
                    start_i = text1_i
                    char_start = char_i
                added_s.append(text2[text2_i])
                text2_i += 1
            
            elif result[i][0] == "-":
                if start_i == -1:
                    start_i = text1_i
                    char_start = char_i
                removed_s.append(text1[text1_i])
                
                char_i += len(text1[text1_i])+1
                text1_i += 1
                
            if result[i][0] == " " or i == len(result)-1:
                if start_i != -1:
                    aux_dic = {}
                    aux_dic['added']      = " ".join(added_s) if len(added_s) > 0 else " "
                    aux_dic['removed']    = " ".join(removed_s)
                    aux_dic['start']      = start_i
                    aux_dic['char_start'] = char_start
                    aux_dic['len']        = len(" ".join(removed_s))
                    aux_dic['context1']   = " ".join(text1[max(0, start_i-2) : min(text1_i+2, len(text1))])
                    aux_dic['context2']   = " ".join(text1[max(0, start_i-2) : start_i]
                                                + added_s+text1[text1_i : min(text1_i+2, len(text1))])
                    
                    # if just adds, remove its closests neighbor
                    if aux_dic['len'] == 0:
                        if text1_i < len(text1):
                            aux_dic['added']    = aux_dic['added'] + " " + text1[text1_i]
                            aux_dic['removed']  = text1[text1_i]
                            aux_dic['len']      = len(text1[text1_i])
                        else:
                            aux_dic['added']       = text1[text1_i-1] + " "
                            aux_dic['removed']     = text1[text1_i-1]
                            aux_dic['char_start'] -= len(text1[text1_i-1])
                            aux_dic['len']         = len(text1[text1_i-1])
                    
                    # if just removes, expand bar to include the neighboring spaces
                    if aux_dic['added'] == " ":
                        if text1_i != len(text1):
                            aux_dic['len'] += 1
                        if text1_i != 0:
                            aux_dic['char_start'] -= 1
                        
                    corrections.append(aux_dic)
                    start_i = -1
                    added_s.clear()
                    removed_s.clear()
                
                
                if i != len(result)-1:
                    char_i  += len(text1[text1_i])+1
                    text1_i += 1
                    text2_i += 1
                
            i += 1
            
        return corrections
    
        
    
    def ask_llm_check(
            self,
            text,
            language, 
            model,
            model_family,
            genres="", 
            extra_prompt="", 
            temperature=0.0, 
            max_tokens=8000, 
            thinking=False, 
            persistent=True):
        
        if model_family not in self.model_families:
            warnings.warn(f"No prompts for family '{model_family}' found. Pasquale will use base prompts instead.")
            model_family = "base"
        
        current_prompts = self.prompts[model_family][language]
        
        if len(current_prompts['system']) != 0:
            system_prompt = current_prompts['system'].format(
                genres=genres)
                                
            text = current_prompts['text'].format(
                text=text) + "\n" + extra_prompt
            
            self.messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ]
        else:
            text = current_prompts['text'].format(
                text=text, genres=genres) + "\n" + extra_prompt
            self.messages=[{"role": "user", "content": text}]
        
        completion = self.client.chat.completions.create(
            model = model,
            messages = self.messages,
            max_completion_tokens = max_tokens,
            temperature = temperature)
        
        if persistent:
            self.messages.append(completion.choices[0].message)
        
        
        if thinking:
            return completion.choices[0].message.content.split("</think>\n\n")[1].strip("\n")
        else:
            return completion.choices[0].message.content.strip("\n")
    
    
    def ask_llm_reason(
            self, 
            correction,
            language, 
            model,
            model_family,
            genres="", 
            extra_prompt="", 
            temperature=0.0, 
            max_tokens=8000, 
            thinking=False, 
            persistent=False):
        
        
        if model_family not in self.model_families:
            warnings.warn(f"No prompts for family '{model_family}' found. Pasquale will use base prompts instead.")
            model_family = "base"
        
        current_prompts = self.prompts[model_family][language]
        text = current_prompts['reason'].format(
            removed  = correction['removed'],
            added    = correction['added'],
            context1 = correction['context1'],
            context2 = correction['context2']) + "\n" + extra_prompt
        
        completion = self.client.chat.completions.create(
            model = model,
            messages = self.messages + [{"role": "user", "content": text}],
            max_completion_tokens = max_tokens,
            temperature = temperature)
        
        if persistent:
            self.messages.append({"role": "user", "content": text})
            self.messages.append(completion.choices[0].message)
        
        if thinking:
            return completion.choices[0].message.content.split("</think>\n\n")[1].strip("\n")
        else:
            return completion.choices[0].message.content.strip("\n")
    
    
    def check(
              self,
              text,
              language):
        
        cor_text = self.ask_llm_check(text, language, **self.config)
        corrections = Pasquale._get_corrections(text.split(" "), cor_text.split(" "))
        
        for correction in corrections:
            correction['reason'] = self.ask_llm_reason(correction, language, **self.config)
        
        return corrections


