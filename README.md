# I Ching Divination API

An AI-powered API for I Ching divination that provides dynamic and personalized interpretations based on user queries.

## Features

- Random I Ching hexagram generation
- Natural language processing to derive context from user questions
- Personalized divination interpretations based on question context
- RESTful API with FastAPI

## Requirements

- Python 3.9+
- FastAPI
- LangChain
- OpenAI API key

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Update the `.env` file with your OpenAI API key
6. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

## API Usage

### Endpoint: `/api/v1/divination`

**Request**:
```json
{
  "question": "Will my business venture succeed this year?"
}
```

**Response**:
```json
{
  "question": "Will my business venture succeed this year?",
  "hexagram": {
    "number": 14,
    "name": "Dà Yǒu (Great Possession)",
    "image": "Fire in heaven"
  },
  "topic": "Business/Career",
  "interpretation": "The hexagram of Great Possession suggests favorable circumstances for your business venture..."
}
```

## Performance Optimization

The API supports both cloud-based (OpenAI) and local LLM implementations, with several optimizations for local inference:

### Local Model Optimizations

- **GPU Acceleration**: Automatic detection and utilization of CUDA, MPS (Apple Silicon), or CPU.
- **Quantization**: Support for 8-bit and 4-bit quantization to reduce memory usage.
- **Attention Optimizations**: Integration with Flash Attention 2 for faster processing.
- **BetterTransformer**: Enhanced transformer architecture for improved throughput.
- **Adaptive Precision**: FP16 for GPUs to balance speed and accuracy.

### Configuration

Performance optimizations can be controlled via `.env` settings:

```bash
# Enable optimizations
LLM_OPTIMIZE=True

# Optimization settings
HF_USE_BETTER_TRANSFORMER=True
HF_USE_FLASH_ATTENTION=True
HF_USE_8BIT=True
HF_USE_4BIT=False
HF_BATCH_SIZE=1
```

For more details on optimizing local models, see [Local Models Documentation](docs/local_models.md).

## Project Structure

```
.
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   └── divination.py
│   │   └── router.py
│   ├── core/
│   │   ├── config.py
│   │   └── llm.py
│   ├── data/
│   │   └── hexagrams.py
│   ├── models/
│   │   └── schemas.py
│   ├── utils/
│   │   ├── i_ching.py
│   │   └── topic_classifier.py
│   └── main.py
├── .env
├── .gitignore
└── requirements.txt
```

## License

MIT
