#!/usr/bin/env python3
"""
horizon_dip_sync.py -- Horizon dip vs. elevation, an animated proof aid.

Produces an MP4 in which BOTH panels are driven by a single shared elevation
h(t), so they never disagree about how high the observer is:

  * left  -- a schematic drawn strictly to scale on a unit Earth. Fixing the
             drawn radius R_draw = 1 collapses the geometry to a clean closed
             form that depends only on the dip angle d:

                 eye              = (0, sec d)
                 horizon tangents = (+/- sin d,  cos d)
                 the true-horizon ray drops exactly d below the astronomical
                 horizon.

             (Proof: cos d = R/(R+h), so R+h = sec d with R = 1; the tangent
             point sits at angular distance d from the sub-observer point,
             hence (sin d, cos d). No arctan needed.)

  * right -- the real dip law on log-log axes: the sqrt(h) regime with both the
             1.75 (with refraction) and 1.93 (pure geometry) coefficients, the
             exact arccos(R/(R+h)) curve tracking them at low elevation and then
             bending below them toward the 90-degree asymptote -- i.e. exactly
             where the sqrt(h) approximation stops being valid.

The climb rate is nonlinear: linear in the dip ANGLE (0 -> 60 deg), eased at
both ends, so the schematic sweeps at a steady visual pace while the shared
marker travels the full quantitative curve.

Companion write-up (derivation of the 1.75 / 1.93 coefficients and the Earth
radius from k): the 'maths/horizondip.md' notes, and https://earthform.linnman.net

--------------------------------------------------------------------------------
Author : August Linnman
License : <choose one, e.g. MIT> -- replication and reuse encouraged.
Requires: Python 3.8+, numpy, matplotlib, and ffmpeg on PATH.
Usage  : python horizon_dip_sync.py [--output FILE] [--fps N] [--dpi N]
--------------------------------------------------------------------------------
"""

import argparse
import shutil
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")                         # headless rendering, no display needed
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.patches import Arc, Circle, FancyArrowPatch

# ---------------------------------------------------------------- parameters
R_EARTH   = 6.378e6            # m, EQUATORIAL radius (WGS-84). Mean radius is
                              # 6.371e6 m; the choice shifts k by ~0.05%. The
                              # horizondip.md notes use this same equatorial value.
D_MIN_DEG = 0.032             # ~1 m of elevation -- keeps h > 0 for the log axes
D_MAX_DEG = 60.0              # top of the climb: eye height = R, dip = 60 deg

BLUE, GREY, DARK = "#2196c4", "#9aa0a6", "#222222"
TRUE_C, ASTRO_C  = "#c0392b", "#111111"
GEOM_C, REFR_C   = "#7d3c98", "#2e86c1"

FPS, N_RISE, N_HOLD, DPI = 30, 170, 40, 130    # ~7 s total


# ---------------------------------------------------------------- physics
def dip_rad(h, R=R_EARTH):
    """Geometric horizon dip (radians) for eye height h above sphere radius R."""
    return np.arccos(R / (R + h))


def height_from_dip(d):
    """Inverse: real eye height (m) that produces dip angle d (radians)."""
    return R_EARTH * (1.0 / np.cos(d) - 1.0)


def fmt_h(h):
    return f"{h:,.0f} m" if h < 1000 else f"{h/1000:,.1f} km"


def fmt_dip(d_rad):
    deg = np.degrees(d_rad)
    return f"{deg*60:.1f}\u2032" if deg < 1 else f"{deg:.1f}\u00b0"


def smoothstep(x):
    return x * x * (3 - 2 * x)


def dip_series(n_rise=N_RISE, n_hold=N_HOLD):
    """Per-frame dip angle (degrees): eased climb 0->60 deg, then a hold."""
    ramp = D_MIN_DEG + smoothstep(np.linspace(0, 1, n_rise)) * (D_MAX_DEG - D_MIN_DEG)
    return np.concatenate([ramp, np.full(n_hold, D_MAX_DEG)])


# ---------------------------------------------------------------- drawing helpers
def draw_observer(ax, x, y, s=0.11):
    ln = dict(color=BLUE, lw=2.4, solid_capstyle="round", zorder=6)
    ax.add_patch(Circle((x, y + 0.9 * s), 0.55 * s, color=BLUE, zorder=6))
    ax.plot([x, x], [y + 0.35 * s, y - 0.9 * s], **ln)
    ax.plot([x - 0.7 * s, x + 0.7 * s], [y - 0.1 * s, y - 0.1 * s], **ln)
    ax.plot([x, x - 0.55 * s], [y - 0.9 * s, y - 1.9 * s], **ln)
    ax.plot([x, x + 0.55 * s], [y - 0.9 * s, y - 1.9 * s], **ln)


def arrow(ax, p0, p1, color=DARK, lw=1.6, both=False):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="<|-|>" if both else "-|>",
                                 mutation_scale=13, color=color, lw=lw, zorder=5))


def draw_schematic(ax, d):
    """Redraw the to-scale schematic (unit Earth) for dip angle d (radians)."""
    ax.clear(); ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-2.0, 2.0); ax.set_ylim(-0.15, 2.55)

    sec, cos, sin = 1 / np.cos(d), np.cos(d), np.sin(d)
    eye = np.array([0.0, sec])                             # eye = (0, sec d)
    pL, pR = np.array([-sin, cos]), np.array([sin, cos])   # tangent points

    ax.add_patch(Circle((0, 0), 1.0, facecolor=GREY, edgecolor="#6b7075", lw=1.2))
    ax.plot([-0.05, 0.05], [1, 1], color=DARK, lw=1.5)     # sub-observer point
    if sec - 1 > 1e-3:                                     # elevation stick
        ax.plot([0, 0], [1, sec], color=DARK, ls=":", lw=1.3)

    draw_observer(ax, *eye)

    arrow(ax, eye, eye + [0, 0.42]); ax.text(0.06, sec + 0.44, "Zenith", fontsize=11)
    arrow(ax, eye, eye - [0, 0.42]); ax.text(0.06, sec - 0.46, "Nadir", fontsize=11, va="top")

    arrow(ax, eye + [-1.8, 0], eye + [1.8, 0], ASTRO_C, both=True)
    ax.text(-1.9, sec + 0.05, "Astronomical Horizon", fontsize=10, color=ASTRO_C)

    for p in (pL, pR):                                     # true-horizon rays
        ext = eye + (p - eye) * 1.16
        ax.plot([eye[0], ext[0]], [eye[1], ext[1]], color=TRUE_C, lw=2.0, zorder=4)
        ax.plot(*p, "o", color=TRUE_C, ms=4.5, zorder=5)
    ax.text(-sin * 1.16 - 0.05, cos - 0.32, "True Horizon", color=TRUE_C, fontsize=10,
            rotation=np.degrees(-d), rotation_mode="anchor", ha="center")

    if np.degrees(d) > 0.4:                                # dip-angle arc
        ax.add_patch(Arc(eye, 0.72, 0.72, theta1=-np.degrees(d), theta2=0,
                         color=TRUE_C, lw=1.6))
        ax.text(0.46, sec - 0.2, f"dip = {fmt_dip(d)}", color=TRUE_C,
                fontsize=11, fontweight="bold", va="center")

    ax.text(0, -0.1, "schematic drawn to scale (unit Earth)", ha="center",
            fontsize=9, style="italic", color="#555")


# ---------------------------------------------------------------- animation
def build_animation():
    """Create the figure and return (fig, anim). No global side effects."""
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.8, 5.7),
                                   gridspec_kw=dict(width_ratios=[1.2, 1.0]))
    suptitle = fig.suptitle("", fontsize=14, fontweight="bold", y=0.975)

    # static right-panel curves (drawn once)
    h_grid = np.logspace(0, 7, 600)                        # 1 m .. 10 000 km
    axR.loglog(h_grid, np.degrees(dip_rad(h_grid)) * 60, color=TRUE_C, lw=2.3,
               label="exact  arccos(R/(R+h))", zorder=4)
    axR.loglog(h_grid, 1.93 * np.sqrt(h_grid), color=GEOM_C, lw=1.5, ls="--",
               label="1.93\u00b7\u221ah  (geometry)")
    axR.loglog(h_grid, 1.75 * np.sqrt(h_grid), color=REFR_C, lw=1.5, ls="--",
               label="1.75\u00b7\u221ah  (refraction)")
    axR.axhline(90 * 60, color="#888", lw=1, ls=":")
    axR.text(1.3, 90 * 60 * 1.04, "90\u00b0  (looking straight down)",
             fontsize=8.5, color="#666", va="bottom")
    axR.set_xlim(1, 1e7); axR.set_ylim(1, 8000)
    axR.set_xlabel("elevation  h   (m)")
    axR.set_ylabel("dip   (arcminutes)")
    axR.set_title("real Earth,  R = 6378 km", fontsize=11)
    axR.grid(which="both", alpha=0.25)
    axR.legend(loc="lower right", fontsize=9)

    # dynamic right-panel artists (updated in place, never recreated)
    (marker,)  = axR.plot([], [], "o", color=TRUE_C, ms=9, zorder=6)
    (dropline,) = axR.plot([], [], color=TRUE_C, lw=1, ls=":", zorder=5)
    readout = axR.text(0.045, 0.94, "", transform=axR.transAxes, va="top",
                       fontsize=10.5, bbox=dict(boxstyle="round", fc="white", ec="#ccc"))

    frames = dip_series()

    def update(i):
        d = np.radians(frames[i])
        h = height_from_dip(d)
        draw_schematic(axL, d)

        dip_am = np.degrees(d) * 60
        marker.set_data([h], [dip_am])
        dropline.set_data([h, h], [1, dip_am])
        readout.set_text(f"h = {fmt_h(h)}\ndip = {fmt_dip(d)}")
        suptitle.set_text(f"Horizon dip grows with elevation      "
                          f"h = {fmt_h(h)}     dip = {fmt_dip(d)}")
        return marker, dropline, readout

    fig.tight_layout(rect=[0, 0, 1, 0.94])
    anim = FuncAnimation(fig, update, frames=len(frames), interval=1000 / FPS)
    return fig, anim


def main(argv=None):
    parser = argparse.ArgumentParser(description="Render the horizon-dip animation to MP4.")
    parser.add_argument("--output", default="horizon_dip_sync.mp4", help="output .mp4 path")
    parser.add_argument("--fps", type=int, default=FPS, help="frames per second")
    parser.add_argument("--dpi", type=int, default=DPI, help="output resolution (dots per inch)")
    args = parser.parse_args(argv)

    if shutil.which("ffmpeg") is None:
        sys.exit("error: ffmpeg not found on PATH. Install it (e.g. 'apt install ffmpeg' "
                 "or 'brew install ffmpeg') and try again.")

    fig, anim = build_animation()
    anim.save(args.output, writer=FFMpegWriter(fps=args.fps, bitrate=2600), dpi=args.dpi)
    plt.close(fig)
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
