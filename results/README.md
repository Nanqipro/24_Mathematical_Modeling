# 可复核结果

`model-comparison.csv` 由以下命令从 `data/model-outputs/` 中的存储预测结果重算：

```bash
python scripts/evaluate_predictions.py
```

评价时会删除“实际值”或“预测值”为空的行。当前每个模型文件包含 21,781 行，其中 4,351 行可用于成对评价，17,430 行缺少预测值。

这些指标不是重新训练结果，也不是生产性能基准。
