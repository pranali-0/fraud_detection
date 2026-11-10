# classification fun
import os
import asyncio
from main.router import ask_llm

MAX_CONCURRENT_LLM_CALLS=10
llm_semaphor=asyncio.Semaphore(MAX_CONCURRENT_LLM_CALLS)
async def _ask_llm_with_semaphor(file_path,doc_type):
    async with llm_semaphor:
        return await ask_llm #call main logic
async def classification(folder_Path):
    files=os.listdir(folder_Path)
    files=[f"{folder_Path}/{file}" for file in files]
    class_dict = {}
    responses=await asyncio.gather(*(_ask_llm_with_semaphor(file,"classification")for file in files))
    doc_types = [response["classification"] for response,_ in responses]
    poi = False
    for file, doc_type in zip(files,doc_types):
        if doc_type == 'poi' and poi:
            doc_type = 'poa'
        if doc_type == 'poi':
            poi = True
        class_dict[file] = doc_type
    return class_

    

