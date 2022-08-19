import argparse
import os
import uuid
from datetime import datetime

import numpy as np
import torch
from einops import rearrange
from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from loguru import logger
from PIL import Image
from schemas import GenerationRequest
from torchvision.utils import make_grid

from ldm.models.diffusion.ddim import DDIMSampler
from ldm.models.diffusion.ddpm import LatentDiffusion
from ldm.models.diffusion.plms import PLMSSampler


router = APIRouter()


@router.post(
    "/generate",
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Return the JSON item or an image.",
        }
    },
)
def post_generation(request: Request, data: GenerationRequest):
    model: LatentDiffusion = request.app.state.model
    clip_model = request.app.state.clip_model
    preprocess = request.app.state.preprocess
    logger.info(type(clip_model))
    opt = argparse.Namespace(
        prompt=data.prompt,
        outdir="latent-diffusion/outputs",
        ddim_steps=data.steps,
        ddim_eta=0,
        n_iter=1,
        W=data.width,
        H=data.height,
        n_samples=int(data.images),
        scale=data.diversity_scale,
        plms=True,
    )

    if opt.plms:
        opt.ddim_eta = 0
        sampler = PLMSSampler(model)
    else:
        sampler = DDIMSampler(model)

    os.makedirs(opt.outdir, exist_ok=True)
    outpath = opt.outdir

    prompt = opt.prompt

    sample_path = os.path.join(outpath, "samples")
    os.makedirs(sample_path, exist_ok=True)
    base_count = len(os.listdir(sample_path))

    all_samples = list()
    all_samples_images = list()

    with torch.no_grad():
        with torch.cuda.amp.autocast():
            with model.ema_scope():
                uc = None
                if opt.scale > 0:
                    uc = model.get_learned_conditioning(opt.n_samples * [""])
                for n in range(opt.n_iter):
                    c = model.get_learned_conditioning(opt.n_samples * [prompt])
                shape = [4, opt.H // 8, opt.W // 8]
                samples_ddim, _ = sampler.sample(
                    S=opt.ddim_steps,
                    conditioning=c,
                    batch_size=opt.n_samples,
                    shape=shape,
                    verbose=False,
                    unconditional_guidance_scale=opt.scale,
                    unconditional_conditioning=uc,
                    eta=opt.ddim_eta,
                )

                x_samples_ddim = model.decode_first_stage(samples_ddim)
                x_samples_ddim = torch.clamp((x_samples_ddim + 1.0) / 2.0, min=0.0, max=1.0)

                for x_sample in x_samples_ddim:
                    x_sample = 255.0 * rearrange(x_sample.cpu().numpy(), "c h w -> h w c")
                    image_vector = Image.fromarray(x_sample.astype(np.uint8))
                    image_preprocess = preprocess(image_vector).unsqueeze(0)
                    with torch.no_grad():
                        image_features = clip_model.encode_image(image_preprocess)
                    image_features /= image_features.norm(dim=-1, keepdim=True)
                    all_samples_images.append(image_vector)
                    # query = image_features.cpu().detach().numpy().astype("float32")
                    # unsafe = is_unsafe(safety_model, query, 0.5)
                    # if not unsafe:
                    #     all_samples_images.append(image_vector)
                    # else:
                    #     return (
                    #         None,
                    #         None,
                    #         "Sorry, potential NSFW content was detected on your outputs by our NSFW detection model. Try again with different prompts. If you feel your prompt was not supposed to give NSFW outputs, this may be due to a bias in the model. Read more about biases in the Biases Acknowledgment section below.",
                    #     )
                    # Image.fromarray(x_sample.astype(np.uint8)).save(os.path.join(sample_path, f"{base_count:04}.png"))
                    base_count += 1
                all_samples.append(x_samples_ddim)

    # additionally, save as grid
    grid = torch.stack(all_samples, 0)
    grid = rearrange(grid, "n b c h w -> (n b) c h w")
    grid = make_grid(grid, nrow=2)
    # to image
    grid = 255.0 * rearrange(grid, "c h w -> h w c").cpu().numpy()

    now = datetime.utcnow().timestamp()
    task_id = str(uuid.uuid5(uuid.NAMESPACE_OID, str(now)))
    Image.fromarray(grid.astype(np.uint8)).save(os.path.join(outpath, f"{task_id}.png"))
    return FileResponse(os.path.join(outpath, f"{task_id}.png"), media_type="image/png")
