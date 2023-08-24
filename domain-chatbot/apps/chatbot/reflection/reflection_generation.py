
import time
from .reflection_template import ReflectionTemplate
from ..config import singleton_sys_config

class ReflectionGeneration():

    reflection_template: ReflectionTemplate

    def __init__(self) -> None:
        self.reflection_template = ReflectionTemplate()

    def generation(self, role_name: str) -> None:

        timestamp = time.time()
        expr = f'timestamp <= {timestamp}'
        result = singleton_sys_config.memory_storage_driver.pageQuery(
            1, 100, expr)

        result = [item['text'] for item in result]
        prompt = self.reflection_template.format(result)

        reflection_result = singleton_sys_config.memory_storage_driver.chat(prompt=prompt, type=singleton_sys_config.reflection_llm_model_driver_type,
                                                            role_name=role_name, you_name="", query="", short_history="", long_history="")
        reflection_result_arr = self.reflection_template.output_format(
            reflection_result)

        # 批量写入到向量数据库中
        for i in range(len(reflection_result_arr)):
            item = reflection_result_arr[i].strip()
            pk = singleton_sys_config.memory_storage_driver.get_current_entity_id()
            singleton_sys_config.memory_storage_driver.save(pk, item, role_name)
