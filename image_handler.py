import asyncio
import logging
import time
from typing import Dict

import replicate


logger = logging.getLogger(__name__)


async def get_url_converted_image(data_images: Dict) -> str:
    try:
        image_url = await replicate.async_run(
            "cuuupid/idm-vton:906425dbca90663ff5427624839572cc56ea7d380343d13e2a4c4b09d3f0c30f",
            input=data_images,
        )
        return image_url
    except replicate.exceptions.ModelError as e:
        logger.error(f"Ошибка модели: {e}")
        return ''
    except replicate.exceptions.ReplicateError:
        logger.error(f"Не передан токен аутентификации")
        return ''
