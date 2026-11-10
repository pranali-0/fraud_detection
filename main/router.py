from main.gemini_llm import run_gemini
from main.utils import read_files,read_prompt,get_file_bytes
import os
from json_repair import repair_json




def router(llm_choice="gemini"):
    match llm_choice:
        case ("gemini"):
            return run_gemini
        case _:
            raise ValueError(f"unknown llm choice {llm_choice}")

    

async def ask_llm(file_path,prompt_type):
    llm=router()
    prompt = await read_prompt(prompt_type)
    ext = os.path.splitext(file_path)[1][1:]
    file_bytes = await get_file_bytes(file_path,ext=ext)
    llm_response,token_used = await llm(file_bytes=file_bytes,custom_prompt=prompt)
    llm_response = repair_json(llm_response,return_objects = True)
    return llm_response,token_used