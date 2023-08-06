import flom


def plot(motion, output, fps=0.01, loop=1):
    from flomutils import plot
    import matplotlib.pyplot as plt

    input_motion = flom.load(motion)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    plot.plot_frames(input_motion, ax, loop, fps)

    ax.legend()
    plt.savefig(output)


def add_noise(motion, output, random=0.1):
    from flomutils import noise

    input_motion = flom.load(motion)

    noise.add_noise(input_motion, random)
    input_motion.dump(output)
