import subprocess
import sys
import os

def run_eval():
    print("=== Phase 1: Running Agent Inference over Golden Dataset ===")

    # Run agents-cli eval generate with dataset
    cmd_gen = [
        "agents-cli", "eval", "generate",
        "--dataset", "eval/golden_dataset.json",
        "--output", "artifacts/traces/"
    ]
    print(f"Executing: {' '.join(cmd_gen)}")
    res_gen = subprocess.run(cmd_gen, shell=False)
    if res_gen.returncode != 0:
        print("Error: Inference generation failed.")
        sys.exit(res_gen.returncode)

    print("\n=== Phase 2: Grading Traces with test_cases.yaml ===")
    cmd_grade = [
        "agents-cli", "eval", "grade",
        "--traces", "artifacts/traces/",
        "--config", "eval/test_cases.yaml",
        "--output", "artifacts/grade_results/"
    ]
    print(f"Executing: {' '.join(cmd_grade)}")
    res_grade = subprocess.run(cmd_grade, shell=False)
    if res_grade.returncode != 0:
        print("Error: Grading failed.")
        sys.exit(res_grade.returncode)

    print("\n=== Evaluation complete. Check artifacts/grade_results/ for HTML/JSON reports. ===")

if __name__ == "__main__":
    run_eval()
