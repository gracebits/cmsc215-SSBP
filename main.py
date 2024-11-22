import threading
import time
import random

# Global variables
waiting_room_capacity = 3  # Number of chairs in the waiting room
waiting_room = []          # Waiting room queue
waiting_room_lock = threading.Lock()
customer_ready = threading.Semaphore(0)  # Semaphore for customers
barber_ready = threading.Event()         # Event for barber sleeping/waking
barber_active = True                      # To end simulation cleanly


def barber():
    while barber_active:
        print("Barber: Waiting for customers...")
        customer_ready.acquire()  # Wait for a customer to signal
        with waiting_room_lock:
            if waiting_room:
                customer_id = waiting_room.pop(0)  # Get the next customer
                print(f"Barber: Cutting hair for Customer {customer_id}.")
        time.sleep(random.uniform(1, 3))  # Simulate cutting hair
        print(f"Barber: Finished cutting hair for Customer {customer_id}.\n")


def customer(customer_id):
    global waiting_room
    with waiting_room_lock:
        if len(waiting_room) < waiting_room_capacity:
            waiting_room.append(customer_id)
            print(f"Customer {customer_id}: Entered the waiting room.")
            customer_ready.release()  # Notify the barber
        else:
            print(f"Customer {customer_id}: Waiting room full. Leaving.\n")
            return
    barber_ready.set()  # Wake the barber if sleeping


def customer_generator():
    customer_id = 1
    while barber_active:
        time.sleep(random.uniform(0.5, 2))  # Random arrival of customers
        threading.Thread(target=customer, args=(customer_id,)).start()
        customer_id += 1


# Main simulation
if __name__ == "__main__":
    # Create barber thread
    barber_thread = threading.Thread(target=barber)
    barber_thread.start()

    # Create customer generator thread
    customer_gen_thread = threading.Thread(target=customer_generator)
    customer_gen_thread.start()

    # Run simulation for a limited time
    try:
        time.sleep(15)  # Run simulation for 15 seconds
    except KeyboardInterrupt:
        print("\nSimulation ended manually.")
    finally:
        barber_active = False  # End barber thread
        customer_ready.release()  # Allow barber to exit gracefully

    barber_thread.join()
    customer_gen_thread.join()
    print("Simulation ended.")
