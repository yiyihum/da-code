# DA-Code: Agent Data Science Code Generation Benchmark for Large Language Models

## ⚙️ Quickstart

### Install required packages
```bash
bash requirements.sh
```

### Set LLM API Key
```bash
export AZURE_API_KEY = your_azure_api_key
export AZURE_ENDPOINT = your_azure_endpoint
export OPENAI_API_KEY = your_openai_api_key
export GEMINI_API_KEY = your_genmini_api_key
```

### Run the benchmark
```bash
python run.py
```

### Evaluate the benchmark
```bash
python evaluate.py
```

### Get Full Dataset
We provide 100 examples of the dataset in the source folder. To get the full dataset, follow the instructions below:
* Download the source data from [here]()
* Unzip the dataset to da_code/source
```bash
unzip source.zip -d da_code/source
```
* Download the gold data from [here]()
* Unzip the gold data to da_code/gold
```bash
unzip gold.zip -d da_code/gold
```





