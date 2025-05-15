# -*- coding: utf-8 -*-
import torch
from app.core.hf_llm_optimized import HuggingFaceLLM

if __name__ == "__main__":
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        print(f"CUDA version: {torch.version.cuda}")
        
    # Test small model with optimization
    print("\nTesting optimized implementation with a small model...")
    model = HuggingFaceLLM(model_name="microsoft/phi-2", max_new_tokens=100)
    
    # Test generation
    prompt = "Tôi muốn hỏi về sự nghiệp của tôi trong tương lai. Đây là điều tôi đang băn khoăn:"
    print(f"\nPrompt: {prompt}")
    print("\nGenerating response...")
    response = model.generate(prompt)
    print(f"\nResponse: {response}")