import asyncio
import base64

from fastapi import FastAPI, Request


app = FastAPI()
# url request example
# curl -X POST http://0.0.0.0:8000/generate -H 'Content-Type: application/json' -d '{"data": ["Hello World",50,32,32,4,15.0]}'


# TODO: implement latent diffusion model to use that in this function
async def run_tti_model(prompt, steps, width, height, images_num, diversity_scale) -> str:
    with open("out.png", "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())
    await asyncio.sleep(7)
    return b64_string


async def make_images(request_data) -> str:
    print(request_data[5])

    prompt, steps, width, height, images_num, diversity_scale = (
        request_data[0],
        request_data[1],
        request_data[2],
        request_data[3],
        request_data[4],
        request_data[5],
    )

    base64_data = await run_tti_model(prompt, steps, width, height, images_num, diversity_scale)
    return base64_data


@app.post("/generate")
async def generate(request: Request) -> dict:
    print("generate")
    json_data = await request.json()
    data = json_data["data"]

    base64_data = await make_images(data)
    return {"base64_data": base64_data}
