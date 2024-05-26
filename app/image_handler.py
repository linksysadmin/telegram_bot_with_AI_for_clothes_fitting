import logging
from typing import Dict

import replicate

from config import REPLICATE_MODEL

logger = logging.getLogger(__name__)


async def get_url_converted_image(data_images: Dict) -> str:
    try:
        image_url = await replicate.async_run(
            REPLICATE_MODEL,
            input=data_images,
        )
        return image_url
    except replicate.exceptions.ModelError as e:
        logger.error(f"Ошибка модели: {e}")
        return ''
    except replicate.exceptions.ReplicateError:
        logger.error(f"Не передан токен аутентификации")
        return ''
