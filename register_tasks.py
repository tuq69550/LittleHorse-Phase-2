import asyncio
from littlehorse.config import LHConfig
from littlehorse import create_task_def

# Load configuration - connects to LittleHorse server on GKE
config = LHConfig()
config.load({"LHC_API_HOST": "34.74.55.93", "LHC_API_PORT": "2023"})

# Define placeholder functions that match the expected task signatures
# (These tell LittleHorse what input each task expects (one string: order_id))
async def dummy_validate(order_id: str) -> str:
    return "validated"

async def dummy_payment(order_id: str) -> str:
    return "paid"

async def main():
    print("Registering task definitions with LittleHorse...")
    # Register both TaskDefs with the LittleHorse server
    # (This must be done BEFORE registering the workflow that uses them)
    create_task_def(dummy_validate, "validate-order", config)
    create_task_def(dummy_payment, "process-payment", config)
    print("Task definitions registered successfully!")

if __name__ == "__main__":
    asyncio.run(main())

