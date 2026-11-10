from google.genai import types
import aiofiles
import yaml



async def create_multimodel_parts(file_bytes,custom_prompt=None,doc_type=None):
    try:
        doc_parts=types.Part.from_bytes(data=file_bytes,mime_type="application/pdf")
        if not custom_prompt:
            prompt_path = "prompts.yaml"
            async with aiofiles.open(prompt_path, "r") as file:
                file_content = await file.read()
                prompts = yaml.safe_load(file_content)
            prompt_text = prompts.get(doc_type)

    

        else:
            prompt_text = custom_prompt
        prompt = [doc_parts,prompt_text]
        return prompt
    except Exception as e:
        return None


async def run_gemini(file_bytes=None,custom_prompt=None):
    if file_bytes:
        try:
            prompt=await create_multimodel_parts(file_bytes,custom_prompt):
            thinking_budget = -1
            config = types.GenearteContentConfig(
                temperature = 0.0,
                thinking_config = types.ThinkingConfig(thinking_budget=thinking_budget),
                response_mime_type = "application/json"
            )
            response = await client.aio.models.generate_content(
                model=llm,
                content=prompt,
                config = config)

            token_count = response.usage_metadata.total_token_count
            return response.text,token_count
        except Exception as e:
            print(f"LLM failed:{e}")
            return None,None
    else:
        print("No document received by llm")
        return None,None    

          