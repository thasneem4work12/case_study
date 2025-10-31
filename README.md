## Call Center Simulation (Python)

This project simulates a simple call center system using Python.  
It models how customer waiting time and queue length change when the number of agents increases.  
The simulation is built using time-stepped logic (1 second per step) and visualized using **matplotlib**.

---

## Project Goal

To study how staffing levels affect:

-  Average waiting time  
-  Queue length  
-  Throughput (calls served)  
-  Agent utilization  

---

## How It Works

- Each second, there’s a chance a new call arrives (based on probability).  
- Each call takes a random time (3–7 seconds) to complete.  
- If all agents are busy, the call waits in a queue.  
- The simulation tracks how long each customer waits and how busy each agent is.  
- Runs three test scenarios:
  - **3_agents**
  - **4_agents**
  - **5_agents**

---

## Simulation Setup

| Parameter | Description | Example |
|------------|--------------|----------|
| `num_agents` | Number of working agents | 3, 4, 5 |
| `arrival_prob_per_dt` | Chance a new call arrives each second | 0.5 |
| `service_time_range` | Time a call takes (seconds) | (3, 7) |
| `sim_time` | Total simulation duration (seconds) | 2000 |

---

## Output & Visualizations

When the program runs, it:

- Prints simulation results for each case.  
- Saves three charts to your Desktop:
  - `simple_avg_wait.png` → Average Waiting Time by Scenario  
  - `simple_max_queue.png` → Maximum Queue Length by Scenario  
  - `simple_queue_timeseries.png` → Queue Length Over Time  

### Example Output:
Running 3_agents...
avg_wait=0.20s, max_queue=6, throughput=630, utilization=53.3%

Running 4_agents...
avg_wait=0.02s, max_queue=3, throughput=649, utilization=40.6%

Running 5_agents...
avg_wait=0.01s, max_queue=2, throughput=647, utilization=32.2%





