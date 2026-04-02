import asyncio
from littlehorse.config import LHConfig
from littlehorse.workflow import Workflow, WorkflowThread
from littlehorse import create_workflow_spec

# Load configuration: connects to the LittleHorse server on GKE
config = LHConfig()
config.load({"LHC_API_HOST": "34.74.55.93", "LHC_API_PORT": "2023"})

def order_workflow(wf: WorkflowThread) -> None:
    # Declare a required input variable for the workflow
    # (This will be passed in when a workflow run is triggered)
    order_id = wf.declare_str("order-id").required()

    # Step 1: Validate the order
    # retries=3 tells LittleHorse to automatically retry this task up to 3 times if it fails before marking the workflow as ERROR
    wf.execute("validate-order", order_id, retries=3)

    # Step 2: Process payment
    # (This step only executes if validate-order succeeds)
    wf.execute("process-payment", order_id)

async def main():
    print("Registering order-processing workflow with retries...")
    # Compiles the workflow definition and registers it with LittleHorse
    # LittleHorse then stores this as a WfSpec (Workflow Specification)
    create_workflow_spec(Workflow("order-processing", order_workflow), config)
    print("Workflow registered successfully!")

if __name__ == "__main__":
    asyncio.run(main())