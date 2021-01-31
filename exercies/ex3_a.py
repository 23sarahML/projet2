import matplotlib.pyplot as plt
import colorsys


def draw_arrows(n: int):
    # Implement drawing of arrows here for an n-by-n grid.

    # Example of an arrow drawn from (0, 0) to (n - 1, n - 1).
    # (Delete this before submitting).

    start_x = 0
    start_y = 0
    end_x = n - 1
    end_y = n - 1

    draw_arrow(start_x, start_y, end_x, end_y)


hue = 0.0


def draw_arrow(
    start_x: float, start_y: float, end_x: float, end_y: float,
):
    global hue

    color = colorsys.hsv_to_rgb(hue, 1, 1)

    hue += 0.125
    if hue >= 1.0:
        hue = 0

    plt.arrow(
        start_x,
        start_y,
        end_x - start_x,
        end_y - start_y,
        head_width=0.2,
        head_length=0.2,
        facecolor=color,
        edgecolor=color,
        overhang=0.4,
        length_includes_head=True,
    )


def draw_grid(n):
    grid_style = dict(color="black", alpha=0.3)

    # draw horizontal grid lines
    for x in range(n + 1):
        plt.plot([x - 0.5, x - 0.5], [-0.5, n - 0.5], **grid_style)

    # draw vertical grid lines
    for y in range(n + 1):
        plt.plot([-0.5, n - 0.5], [y - 0.5, y - 0.5], **grid_style)


def plot_setup(n: int, n_bits: int):
    # set plot size
    plt.figure(figsize=(12, 12))
    plt.axis("equal")

    # set tick labels in binary
    plt.xticks(list(range(n)), [bin(x + (1 << n_bits))[3:] for x in range(n)])
    plt.yticks(list(range(n)), [bin(y + (1 << n_bits))[3:] for y in range(n)])

    # flip plot upside down
    plt.gca().xaxis.tick_top()
    plt.gca().invert_yaxis()


def main():
    for n_bits in [2, 3, 4]:
        n = 1 << n_bits

        plot_setup(n, n_bits)
        draw_grid(n)
        draw_arrows(n)
        plt.savefig(f"z-order-{n}.pdf")
        plt.show()


if __name__ == "__main__":
    main()
