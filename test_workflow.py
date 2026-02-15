# test_workflow.py

from orchestrator import MultiModelOrchestrator

orch = MultiModelOrchestrator()

try:
    pid, model1_df, llm_out, pdf_path = orch.run_pipeline(r"C:\Users\Amogh S\Downloads\sterling-accuris-pathology-sample-report-unlocked.pdf")

    print("Pipeline Execution Successful!")
    print("Patient ID:", pid)
    print("\nModel 1 Output:\n", model1_df)
    print("\nLLM Output:\n", llm_out)
    print("\nGenerated Report:", pdf_path)

except Exception as e:
    print("Pipeline Failed:", str(e))
