import aiofiles
import os 
import yaml
import asyncio
from json_repair import repair_json
import json
from PIL import Image
import io

async def get_file_bytes(file_path,ext):
    async with aiofiles.open(file_path,"rb") as file:
        file_bytes = await file.read()

        if ext.lower().lstrip('.') != 'pdf':
            def sync_conversation():
                image_stream = io.BytesIO(file_bytes)
                img = Image.open(image_stream)
                output_stream = io.BytesIO()
                img.save(output_stream,format='PDF')
                return output_stream.getvalue()
            pdf_bytes = await asyncio.to_thread(sync_conversation)
            return pdf_bytes
        else:
            return file_bytes


async def read_prompt(prompt_type):
    prompt_path = "prompts.yaml"
    async with aiofiles.open(prompt_path, "r") as file:
        file_content = await file.read()
        prompts = yaml.safe_load(file_content)
        prompt_text = prompts.get(prompt_type)
        return prompt_text



def read_files(file_paths=None):
    if file_paths is None:
        file_paths = "data/documents/MT207896578"
    file_list = os.listdir(file_paths)
    return file_list
