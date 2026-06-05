# Diagram Types

Choose the diagram type before writing the drawing spec.

## Model Architecture

Use for YOLO, Transformer, CNN, encoder-decoder, feature pyramid, detection head, attention, loss, and training/inference models.

Layout:

- Left-to-right for data flow.
- Stack feature scales vertically when showing multi-scale features.
- Use repeated equal-size blocks for repeated layers.
- Use color families by stage: input/data, backbone, neck, head, loss/output.

Common nodes:

- Input, Dataset, Preprocess, Backbone, Neck, Head, Feature Map, Conv, C2f, Attention, Concat, Upsample, Downsample, Loss, Prediction, NMS, Output.

## Method Workflow

Use for data collection, preprocessing, training, inference, evaluation, deployment, or algorithm pipelines.

Layout:

- Top-to-bottom for chronological process.
- Left-to-right for compact paper figures.
- Put feedback loops and optional branches on separate lanes.

## System Architecture

Use for software, service, database, model API, visualization, or edge/cloud systems.

Layout:

- Use layers: client, service, model, storage, external systems.
- Keep data stores visually distinct.
- Label protocols or data formats on connectors only when important.

## Experiment Design

Use for ablation studies, comparison experiments, benchmark flow, or data splits.

Layout:

- Show dataset split first.
- Put comparable experiment branches in parallel columns.
- Merge branches into metrics and conclusions.

## Paper Concept Figure

Use for problem definition, motivation, method advantage, or comparison illustrations.

Layout:

- Prefer a small number of strong visual regions.
- Use annotations sparingly.
- Make the contribution visually clear without long text.

## Pseudo-Code, Sequence, and Interaction

Use for algorithm steps, module calls, or temporal interactions.

Layout:

- Pseudo-code: boxed steps with indentation or swimlanes.
- Sequence: vertical lifelines and horizontal messages.
- Interaction: modules as nodes, calls/data as directed connectors.

## Image Reproduction

Use when the user provides a paper screenshot, sketch, or PPT image.

First classify the target:

- Structure reproduction: preserve modules, arrows, and hierarchy.
- Visual reproduction: match colors, typography, proportions, arrow style, and spacing.
- Publication redraw: improve clarity and consistency while preserving meaning.
