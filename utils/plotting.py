import matplotlib.pyplot as plt


def plot_signal(bits, coding_name, signal, t):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(t, signal)
    ax.set_title(f"{coding_name.upper()} Signal")
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")
    ax.set_ylim([-1.5, 1.5])
    ax.grid(True)

    # Add bit labels
    for i, bit in enumerate(bits):
        ax.text(i + 0.5, -1.7, bit, ha='center', va='center')

    ax.set_xticks(range(len(bits) + 1))
    ax.set_xticklabels(range(len(bits) + 1))

    return fig