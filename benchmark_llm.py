# -*- coding: utf-8 -*-
"""
Benchmark script to compare performance between original and optimized Hugging Face LLM implementations.
"""

import time
import torch
from app.core.hf_llm import HuggingFaceLLM as StandardLLM
from app.core.hf_llm_optimized import HuggingFaceLLM as OptimizedLLM

def benchmark_model(model_class, model_name, prompt, max_new_tokens=50, runs=3):
    """Benchmark a model implementation"""
    print(f"\nBenchmarking {model_class.__module__}.{model_class.__name__}...")
    
    # Initialize model
    start_time = time.time()
    model = model_class(model_name=model_name, max_new_tokens=max_new_tokens)
    init_time = time.time() - start_time
    print(f"Model initialization time: {init_time:.2f} seconds")
    
    # Warm up (first run is always slower)
    print("Warming up...")
    _ = model.generate(prompt)
    
    # Benchmark generation
    total_time = 0
    for i in range(runs):
        print(f"Run {i+1}/{runs}...")
        torch.cuda.empty_cache()  # Clear GPU memory
        start_time = time.time()
        response = model.generate(prompt)
        run_time = time.time() - start_time
        total_time += run_time
        print(f"  Generated {len(response.split())} words in {run_time:.2f} seconds")
    
    avg_time = total_time / runs
    print(f"Average generation time: {avg_time:.2f} seconds")
    
    # Get memory usage
    if torch.cuda.is_available():
        memory_allocated = torch.cuda.memory_allocated() / 1024**2
        memory_reserved = torch.cuda.memory_reserved() / 1024**2
        print(f"GPU memory allocated: {memory_allocated:.2f} MB")
        print(f"GPU memory reserved: {memory_reserved:.2f} MB")
    
    return {
        "init_time": init_time,
        "avg_gen_time": avg_time,
        "memory_allocated": memory_allocated if torch.cuda.is_available() else 0,
        "memory_reserved": memory_reserved if torch.cuda.is_available() else 0
    }

if __name__ == "__main__":
    # System info
    print("=== System Information ===")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        print(f"CUDA version: {torch.version.cuda}")
    else:
        print("Running on CPU")
    
    # Test parameters
    MODEL_NAME = "microsoft/phi-2"  # Small model for quicker testing
    PROMPT = "Hãy giải thích ý nghĩa của quẻ Kinh Dịch số 1 - Càn (Thuần Dương) và cách áp dụng vào cuộc sống hiện đại:"
    MAX_NEW_TOKENS = 100
    RUNS = 3
    
    print("\n=== Starting Benchmark ===")
    print(f"Model: {MODEL_NAME}")
    print(f"Max new tokens: {MAX_NEW_TOKENS}")
    print(f"Number of runs: {RUNS}")
    
    # Run benchmarks
    standard_results = benchmark_model(StandardLLM, MODEL_NAME, PROMPT, MAX_NEW_TOKENS, RUNS)
    optimized_results = benchmark_model(OptimizedLLM, MODEL_NAME, PROMPT, MAX_NEW_TOKENS, RUNS)
    
    # Compare results
    print("\n=== Benchmark Results ===")
    init_speedup = standard_results["init_time"] / optimized_results["init_time"] if optimized_results["init_time"] > 0 else 0
    gen_speedup = standard_results["avg_gen_time"] / optimized_results["avg_gen_time"] if optimized_results["avg_gen_time"] > 0 else 0
    memory_reduction = (standard_results["memory_allocated"] - optimized_results["memory_allocated"]) / standard_results["memory_allocated"] * 100 if standard_results["memory_allocated"] > 0 else 0
    
    print(f"Initialization speedup: {init_speedup:.2f}x ({'+' if init_speedup > 1 else '-'}{abs(100 - 100/init_speedup):.1f}%)")
    print(f"Generation speedup: {gen_speedup:.2f}x ({'+' if gen_speedup > 1 else '-'}{abs(100 - 100/gen_speedup):.1f}%)")
    print(f"Memory usage change: {memory_reduction:.1f}%")
    
    print("\nNote: Positive percentages indicate improvements in speed or reductions in memory usage.")
    print("      For more accurate results, increase the number of runs and test with larger models.")
