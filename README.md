# DeepEval Playground

A minimal [DeepEval](https://github.com/confident-ai/deepeval) POC that runs one `GEval` test with a local Ollama judge model.

This repo is a small example of the `LLM-as-a-judge` pattern:

- define a rubric in plain English
- give the judge an `actual_output` and an `expected_output`
- get a pass/fail result from `pytest`

## What this repo tests

This example evaluates one simple customer-support response:

- User asks: `"What if these shoes don't fit?"`
- Model answer: `"You have 30 days to get a full refund at no extra cost."`
- Expected answer: `"We offer a 30-day full refund at no extra costs."`

The judge checks whether the actual answer is semantically correct based on the expected answer.

This is useful as a POC because it validates:

- DeepEval is wired correctly
- a local Ollama model can act as the judge
- `GEval` can evaluate a response inside a test

It does **not** prove broad evaluation quality. It is only meant to show the basic evaluation flow with as little code as possible.

## What `GEval` is doing here

`GEval` is DeepEval's rubric-based metric.

In this repo, the metric is named `Correctness`, but the real logic is the rubric. The judge is told to:

- treat paraphrases as correct when they preserve the same policy meaning
- ignore minor wording differences
- fail responses that change, omit, contradict, or add a material policy detail

The judge sees:

- `input`
- `actual_output`
- `expected_output`

and returns a score from `0` to `1`. If the score is above the threshold, the test passes.

## When this is useful

Traditional metrics like accuracy, precision, recall, and F1 work well when outputs can be compared directly to labeled answers. For many LLM tasks, that is not enough, because two answers can use different wording while still meaning the same thing. This is where rubric-based evaluation can be useful: instead of exact matching, you ask a judge model to score the quality of the response against a plain-English criterion.

## Project setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Running the evaluation

This project uses [Ollama](https://ollama.com) as the local judge model.

1. Start Ollama:

```bash
ollama serve
```

2. Pull the model once:

```bash
ollama pull qwen2.5:14b
```

`qwen2.5:14b` was chosen as a stronger local judge that should still fit on a machine with roughly 16 GB of GPU RAM.

3. Run the test:

```bash
uv run pytest test_correctness.py -v
```

This gives a simple pass/fail result for the single example.

## Current limitations

- The repo contains only one static test case.
- The result depends heavily on rubric wording.
- The result also depends heavily on judge model quality.
- Judge-based evaluation is useful, but not deterministic or equivalent to ground-truth accuracy.
- Even with a stronger local judge model, borderline cases may still be inconsistent.
