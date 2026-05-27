from deepeval.metrics import GEval
from deepeval.models import OllamaModel
from deepeval.test_case import LLMTestCase, SingleTurnParams


def test_correctness():
    correctness_metric = GEval(
        name="Correctness",
        model=OllamaModel(model="qwen2.5:14b"),
        criteria=(
            "Determine whether the actual output is semantically correct based on the expected output. "
            "Treat paraphrases as correct if they preserve the same policy meaning. "
            "Ignore minor wording differences. "
            "Fail only if the actual output changes, omits, contradicts, or adds a material policy detail."
        ),
        evaluation_params=[
            SingleTurnParams.INPUT,
            SingleTurnParams.ACTUAL_OUTPUT,
            SingleTurnParams.EXPECTED_OUTPUT,
        ],
        threshold=0.7,
    )

    test_case = LLMTestCase(
        input="What if these shoes don't fit?",
        actual_output="You have 30 days to get a full refund at no extra cost.",
        expected_output="We offer a 30-day full refund at no extra costs.",
    )

    correctness_metric.measure(test_case)
    print("score:", correctness_metric.score)
    print("reason:", correctness_metric.reason)

    assert correctness_metric.is_successful()
