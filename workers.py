import asyncio
import os
from littlehorse.config import LHConfig
from littlehorse.worker import LHTaskWorker

# Set environment variables so all channels can connect to the correct server
os.environ["LHC_API_HOST"] = "34.74.55.93"
os.environ["LHC_API_PORT"] = "2023"

config = LHConfig()

# Tracking how many times validate_order has been attempted
# (This simulates a real world transient failure scenario)
attempt_count = 0

async def validate_order(order_id: str) -> str:
    """
    Task worker for the validate-order task.
    Deliberately fails on the first two attempts to demonstrate
    LittleHorse's automatic retry behavior.
    On the third attempt, the task succeeds.
    """
    global attempt_count
    attempt_count += 1

    if attempt_count < 3:
        print(f"Attempt {attempt_count}: FAILED for order {order_id}")
        # Raising an exception signals to LittleHorse that the task FAILED
        # LittleHorse will then automatically schedule a retry
        raise Exception(f"Simulated failure on attempt {attempt_count}")

    print(f"Attempt {attempt_count}: SUCCEEDED for order {order_id}")
    return f"Order {order_id} validated successfully"

async def process_payment(order_id: str) -> str:
    """
    Task worker for the process-payment task.
    Only executes after validate-order has succeeded.
    """
    print(f"Processing payment for order {order_id}")
    return f"Payment processed for order {order_id}"

async def main():
    # Create task workers that connect to LittleHorse and listen for tasks
    # (Each worker polls LittleHorse for its specific task type)
    worker1 = LHTaskWorker(validate_order, "validate-order", config)
    worker2 = LHTaskWorker(process_payment, "process-payment", config)

    print("Workers started, listening for tasks...")
    # Run both workers 
    await asyncio.gather(worker1.start(), worker2.start())

if __name__ == "__main__":
    asyncio.run(main())