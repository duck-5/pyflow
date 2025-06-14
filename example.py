import asyncio
from typing import Tuple

from python_flow.core import AsyncPipeline
from python_flow.nodes import (
    AsyncioTimerDataStreamerNode,
    CombineNode,
    MapperNode,
    PrinterNode,
    RangerNode,
    RollingSumNode,
    ValueInRangeForDurationValidatorNode,
)
from python_flow.utils import utils


async def main():
    ranger_0 = RangerNode(label="Ranger_0", step=1)
    ranger_1 = RangerNode(label="Ranger_1", step=2)

    rolling_sum_of_3 = RollingSumNode(label="RollingSumOf3", summed_queue_len=3)
    rolling_sum_of_2 = RollingSumNode(label="RollingSumOf2", summed_queue_len=2)
    combiner = CombineNode(label="Combiner", input_type=Tuple[int])
    printer_0 = PrinterNode(label="Printer_0")
    printer_1 = PrinterNode(label="Printer_1")
    value_in_range_validator = ValueInRangeForDurationValidatorNode(
        label="ValueInRangeForDurationValidator",
        top_limit=300,
        bottom_limit=100,
        duration_seconds=2,
    )
    alert_printer = PrinterNode(label="AlertPrinter")
    timer_0 = AsyncioTimerDataStreamerNode(
        label="Timer0.5",
        loop=asyncio.get_event_loop(),
        timer_interval_seconds=0.5,
        input_type=int,
    )
    timer_1 = AsyncioTimerDataStreamerNode(
        label="Timer1",
        loop=asyncio.get_event_loop(),
        timer_interval_seconds=1,
        input_type=int,
    )

    str_converter = MapperNode(label="StrConverter", callback=str, input_type=str)
    wow_suffix_adder = MapperNode(label="WowSuffixAdder", callback=lambda x: x + "wow", input_type=str)

    pipeline_0 = AsyncPipeline(head=ranger_0, middle_nodes=[rolling_sum_of_3, combiner, printer_0])
    pipeline_1 = AsyncPipeline(
        head=ranger_1,
        middle_nodes=[
            rolling_sum_of_2,
            combiner,
            timer_0,
            str_converter,
            wow_suffix_adder,
            printer_0,
        ],
    )
    pipeline_2 = AsyncPipeline(head=ranger_1, middle_nodes=[rolling_sum_of_2, timer_1, printer_1])
    pipeline_3 = AsyncPipeline(
        head=ranger_1,
        middle_nodes=[
            rolling_sum_of_2,
            timer_1,
            value_in_range_validator,
            alert_printer,
        ],
    )

    pipelines = [pipeline_0, pipeline_1, pipeline_2, pipeline_3]
    utils.initialize_all_pipelines(pipelines)
    utils.render_graphviz_graph(pipelines, label="main_graph")
    await utils.async_start_pipelines(pipelines)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    loop.run_forever()
