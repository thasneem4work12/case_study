import random
import statistics
import os
import matplotlib.pyplot as plt

# SIMPLE CALL CENTER SIMULATION 
# -----------------------------------------------------------
# This program simulates a call center with a few agents.
# Customers call randomly, and each call takes some time to complete.
# If all agents are busy, the customer must wait in a queue.
# The goal: See how waiting time changes when we increase the number of agents.
# -----------------------------------------------------------

def simulate_time_stepped(num_agents, arrival_prob_per_dt, service_time_range, sim_time=2000, dt=1):
    """
    Runs the call center simulation for a given number of agents.

    num_agents: how many agents are working
    arrival_prob_per_dt: how likely a new call arrives in each second
    service_time_range: range of seconds each call takes to finish
    sim_time: total time to run the simulation
    dt: time step (1 second per step)

    Returns a dictionary with performance results:
    - avg_wait: average waiting time for calls
    - max_queue: maximum queue length reached
    - throughput: how many calls were served
    - utilization: how busy the agents were (in %)
    - queue_time_series: data for plotting queue changes over time
    """
    queue = []  # store waiting customers 
    agents = [0] * num_agents  # remaining time for each agent (0 = free)
    total_busy_time = [0] * num_agents  # track total time each agent worked
    wait_times = []  # how long each call waited before answered
    queue_length_times = []  # record queue size over time
    served = 0  # number of calls handled

    # Loop through each second of simulation
    for t in range(0, sim_time, dt):

        # Step 1: New call arrives with some probability
        if random.random() < arrival_prob_per_dt:
            queue.append(t)  # save time when the call came

        # Step 2: Update agent busy times
        for i in range(num_agents):
            if agents[i] > 0:  # agent is busy
                agents[i] -= dt  # reduce remaining busy time
                total_busy_time[i] += dt  # count how long they worked
                if agents[i] <= 0:
                    agents[i] = 0  # free now

        # Step 3: Give waiting calls to free agents
        for i in range(num_agents):
            if agents[i] == 0 and queue:  # agent free and people waiting
                arrival_time = queue.pop(0)  # first person in queue
                wait_times.append(t - arrival_time)  # how long they waited
                service_time = random.randint(*service_time_range)  # random call duration
                agents[i] = service_time  # make agent busy for that time
                served += 1  # one more call completed

        # Step 4: Record queue length for graph
        queue_length_times.append((t, len(queue)))

    # Step 5: Calculate summary results
    avg_wait = statistics.mean(wait_times) if wait_times else 0
    max_queue = max((length for _, length in queue_length_times), default=0)
    throughput = served
    utilization = sum(total_busy_time) / (num_agents * sim_time) * 100

    # Return results as a dictionary
    return {
        'avg_wait': avg_wait,
        'max_queue': max_queue,
        'throughput': throughput,
        'queue_time_series': queue_length_times,
        'utilization': utilization,
    }


def run_simple_experiments():
    """Run 3 different cases and compare results."""
    desktop = os.path.expanduser('~/Desktop')  # Save charts on desktop

    # 3 scenarios: 3, 4, and 5 agents
    # All have same call arrival rate (0.5 chance per second)
    scenarios = {
        '3_agents': (3, 0.5, (3, 7)),
        '4_agents': (4, 0.5, (3, 7)),
        '5_agents': (5, 0.5, (3, 7)),
    }

    results = {}

    # Run each scenario one by one
    for name, (agents, arrival_prob, service_range) in scenarios.items():
        out = simulate_time_stepped(agents, arrival_prob, service_range)
        results[name] = out
        print(f"Running {name}...")
        print(f"  avg_wait={out['avg_wait']:.2f}s, max_queue={out['max_queue']}, throughput={out['throughput']}, utilization={out['utilization']:.1f}%")
        print()

    # Compare average waiting times between scenarios
    base = results['3_agents']['avg_wait']
    four = results['4_agents']['avg_wait']
    five = results['5_agents']['avg_wait']

    # Function to calculate improvement percentage
    def pct(old, new):
        return (old - new) / old * 100 if old else 0

    print('Simple comparison:')
    print(f"  3 agents avg wait = {base:.2f}s")
    print(f"  4 agents avg wait = {four:.2f}s ({pct(base, four):.1f}% improvement)")
    print(f"  5 agents avg wait = {five:.2f}s ({pct(base, five):.1f}% improvement)")

    # MAKE GRAPHS (VISUALS)
    names = list(results.keys())

    # Bar graph - Average waiting time
    plt.figure()
    values = [results[n]['avg_wait'] for n in names]
    plt.bar(names, values, color=['#d9534f', '#f0ad4e', '#5cb85c'])
    plt.ylabel('Average Wait (s)')
    plt.title('Average Waiting Time by Scenario')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    avg_path = os.path.join(desktop, 'simple_avg_wait.png')
    plt.savefig(avg_path)
    print(f'Saved {avg_path}')

    # Line graph - Queue size over time
    plt.figure(figsize=(10, 5))
    max_q_overall = 0
    for name in names:
        times, lengths = zip(*results[name]['queue_time_series'])
        plt.step(times, lengths, where='post', label=name)
        max_q_overall = max(max_q_overall, max(lengths))
    plt.xlabel('Time (s)')
    plt.ylabel('Queue length')
    plt.legend()
    plt.ylim(0, max_q_overall + 2)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    queue_path = os.path.join(desktop, 'simple_queue_timeseries.png')
    plt.savefig(queue_path)
    print(f'Saved {queue_path}')

    # Bar graph - Maximum queue length
    plt.figure(figsize=(6, 4))
    max_vals = [results[n]['max_queue'] for n in names]
    bars = plt.bar(names, max_vals, color=['#5cb85c', '#f0ad4e', '#d9534f'])
    plt.ylabel('Max queue length')
    plt.title('Max Queue Length by Scenario')
    for bar, val in zip(bars, max_vals):
        plt.text(bar.get_x() + bar.get_width() / 2, val + 0.1, str(val), ha='center', va='bottom')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    maxq_path = os.path.join(desktop, 'simple_max_queue.png')
    plt.savefig(maxq_path)
    print(f'Saved {maxq_path}')


# Run the program
if __name__ == '__main__':
    random.seed(42)  # keep results repeatable
    run_simple_experiments()