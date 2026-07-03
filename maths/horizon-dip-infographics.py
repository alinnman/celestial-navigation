"""
Horizon dip vs elevation on log-log axes, enhanced with the exact
trigonometric formula alongside the sqrt(H) approximation.

Curves
  1. Exact geometry      D = arccos(R / (R + H))   (equivalently
                         arctan( sqrt(H^2 + 2 R H) / R ), the same function)
  2. No refraction       D = 1.93 * sqrt(H)        (small-angle limit of 1)
  3. With refraction      D = K(H) * sqrt(H), K rising 1.75 -> 1.93

Across all real observer elevations (1 m to ~10 km) curves 1 and 2 agree to
better than 1 percent. The sqrt(H) line keeps climbing as a straight slope-1/2
line forever; the true dip bends over and saturates at a 90 degree ceiling.

D is dip in arcminutes, H is observer elevation in metres.
"""

import numpy as np
import matplotlib.pyplot as plt

# --- Physical constants -------------------------------------------------
EARTH_RADIUS_M = 6.378e6
ARCMIN_PER_RAD = np.degrees(1.0) * 60.0
DIP_CEILING_ARCMIN = 90.0 * 60.0          # dip -> 90 deg as H -> infinity

K_GEOMETRIC = 1.93                         # vacuum coefficient (geometry)
K_OBSERVED = 1.75                          # typical low-elevation, with refraction

PRACTICAL_MAX_M = 1.0e4                     # ~10 km, above any real observer
BEACH_ALTITUDE_M = 2.0e0                    # ~2 m, person standing at the shore
SHIP_ALTITUDE_M = 3.0e1                     # ~30 m, high deck of a large cruise ship
BURJ_ALTITUDE_M = 5.0e2                     # ~500 m, near Burj Khalifa observation deck
CRUISE_ALTITUDE_M = 1.0e4                   # ~10 km, typical airliner cruise
ISS_ALTITUDE_M = 4.0e5                      # ~400 km, for context

HOME_OWNER = "august"

H = np.logspace(0, 7, 600)                 # 1 m to 10000 km


# --- Models -------------------------------------------------------------
def dip_exact_arccos(h):
    """Exact geometric dip, arccos form."""
    return np.arccos(EARTH_RADIUS_M / (EARTH_RADIUS_M + h)) * ARCMIN_PER_RAD


def dip_exact_arctan(h):
    """Exact geometric dip, arctan form. Identical to the arccos form."""
    return np.arctan(np.sqrt(h**2 + 2 * EARTH_RADIUS_M * h) / EARTH_RADIUS_M) * ARCMIN_PER_RAD


def k_with_refraction(h, k_lo=K_OBSERVED, k_hi=K_GEOMETRIC,
                      h_lo=1.0, h_hi=PRACTICAL_MAX_M):
    """Coefficient rising smoothly from k_lo (dense low air) to k_hi (thin high air)."""
    u = (np.log10(h) - np.log10(h_lo)) / (np.log10(h_hi) - np.log10(h_lo))
    u = np.clip(u, 0.0, 1.0)
    smoothstep = u * u * (3.0 - 2.0 * u)
    return k_lo + (k_hi - k_lo) * smoothstep


def burj_silhouette():
    """Vertices of a slender, smoothly tapering spire (Burj Khalifa-like)."""
    right = [
        (0.220, 0.00), (0.205, 0.10), (0.180, 0.22), (0.150, 0.34),
        (0.122, 0.45), (0.098, 0.55), (0.076, 0.64), (0.057, 0.72),
        (0.041, 0.79), (0.028, 0.85), (0.017, 0.90), (0.009, 0.95),
        (0.004, 1.00), (0.000, 1.10),
    ]
    left = [(-x, y) for x, y in reversed(right[:-1])]
    return np.array(right + left)


def airplane_silhouette():
    """Vertices of a top-view airplane pointing up (classic flight-tracker icon)."""
    right = [
        (0.00, 1.00), (0.045, 0.74), (0.045, 0.60), (0.47, 0.43),
        (0.40, 0.40), (0.05, 0.48), (0.05, 0.18), (0.22, 0.08),
        (0.16, 0.055), (0.05, 0.10), (0.05, 0.00),
    ]
    left = [(-x, y) for x, y in reversed(right[:-1])]
    return np.array(right + left)


def draw_burj(iax):
    """Slender tapering spire."""
    from matplotlib.patches import Polygon
    iax.add_patch(Polygon(burj_silhouette(), closed=True,
                          facecolor="#5b7a99", edgecolor="none"))
    iax.set_xlim(-0.30, 0.30)
    iax.set_ylim(0.0, 1.20)


def draw_airplane(iax):
    """Top-view airliner."""
    from matplotlib.patches import Polygon
    iax.add_patch(Polygon(airplane_silhouette(), closed=True,
                          facecolor="#37474f", edgecolor="none"))
    iax.set_xlim(-0.55, 0.55)
    iax.set_ylim(0.0, 1.05)


def draw_iss(iax):
    """Stylized ISS: central truss, modules, and two pairs of solar arrays."""
    from matplotlib.patches import Rectangle
    panel, truss, module = "#2f5d8a", "#8a8d90", "#d2d4d6"
    arrays = [  # (x, y, w, h): outer then inner pair, above and below the truss
        (-0.50, 0.07, 0.22, 0.25), (-0.50, -0.32, 0.22, 0.25),
        (0.28, 0.07, 0.22, 0.25), (0.28, -0.32, 0.22, 0.25),
        (-0.26, 0.07, 0.16, 0.21), (-0.26, -0.28, 0.16, 0.21),
        (0.10, 0.07, 0.16, 0.21), (0.10, -0.28, 0.16, 0.21),
    ]
    for x, y, w, h in arrays:
        iax.add_patch(Rectangle((x, y), w, h, facecolor=panel,
                                edgecolor="white", lw=0.4))
    iax.add_patch(Rectangle((-0.50, -0.025), 1.00, 0.05,
                            facecolor=truss, edgecolor="none"))
    iax.add_patch(Rectangle((-0.06, -0.10), 0.12, 0.20,
                            facecolor=module, edgecolor="#777", lw=0.4))
    iax.set_xlim(-0.58, 0.58)
    iax.set_ylim(-0.45, 0.45)


def draw_person(iax):
    """Standing person on a sand strip (beach observer)."""
    from matplotlib.patches import Circle, Polygon, Rectangle
    body, sand = "#6d4c33", "#e9d8a6"
    iax.add_patch(Rectangle((-0.30, -0.02), 0.60, 0.07,
                            facecolor=sand, edgecolor="none"))
    iax.add_patch(Circle((0.0, 0.82), 0.12, facecolor=body, edgecolor="none"))
    figure = [
        (-0.09, 0.70), (-0.12, 0.66), (-0.15, 0.42), (-0.10, 0.42),
        (-0.06, 0.62), (-0.08, 0.30), (-0.085, 0.06), (-0.02, 0.06),
        (-0.012, 0.34), (0.012, 0.34), (0.02, 0.06), (0.085, 0.06),
        (0.08, 0.30), (0.06, 0.62), (0.10, 0.42), (0.15, 0.42),
        (0.12, 0.66), (0.09, 0.70),
    ]
    iax.add_patch(Polygon(figure, closed=True, facecolor=body, edgecolor="none"))
    iax.set_xlim(-0.32, 0.32)
    iax.set_ylim(-0.05, 1.00)


def draw_cruiseship(iax):
    """Stylized cruise ship: navy hull, tiered white superstructure, funnel."""
    from matplotlib.patches import Polygon, Rectangle
    hull, decks, funnel, edge = "#1f4e79", "#e8edf1", "#c0392b", "#5a6b7a"
    hull_v = [(-0.46, 0.20), (-0.44, 0.07), (0.30, 0.05),
              (0.50, 0.13), (0.44, 0.20)]
    iax.add_patch(Polygon(hull_v, closed=True, facecolor=hull, edgecolor="none"))
    for x, y, w, h in [(-0.42, 0.20, 0.80, 0.07),
                       (-0.36, 0.27, 0.66, 0.06),
                       (-0.28, 0.33, 0.50, 0.055)]:
        iax.add_patch(Rectangle((x, y), w, h, facecolor=decks,
                                edgecolor=edge, lw=0.4))
    iax.add_patch(Rectangle((0.02, 0.385), 0.12, 0.10,
                            facecolor=funnel, edgecolor="none"))
    iax.set_xlim(-0.55, 0.58)
    iax.set_ylim(0.0, 0.55)


def place_icon(ax, draw_shape, axes_box, data_xy, marker_color, label):
    """Draw an icon in an inset, mark its elevation on the curve, link them."""
    ax.scatter([data_xy[0]], [data_xy[1]], s=55, color=marker_color,
               edgecolor="white", linewidth=1.0, zorder=6)
    ax.annotate("", xy=data_xy, xycoords="data",
                xytext=(axes_box[0] + axes_box[2] / 2, axes_box[1]),
                textcoords="axes fraction",
                arrowprops=dict(arrowstyle="-", color="0.55", lw=1.0))
    iax = ax.inset_axes(axes_box)
    draw_shape(iax)
    iax.set_aspect("equal")
    iax.axis("off")
    iax.set_title(label, fontsize=8.5, color=marker_color, pad=2)


# The two exact forms must agree; assert it rather than trust it.
assert np.allclose(dip_exact_arccos(H), dip_exact_arctan(H)), "exact forms disagree"

dip_exact = dip_exact_arccos(H)
dip_sqrt = K_GEOMETRIC * np.sqrt(H)
dip_refr = k_with_refraction(H) * np.sqrt(H)


# --- Plot ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 7))

# Shade the band of real observer elevations.
ax.axvspan(1, PRACTICAL_MAX_M, color="#fff2cc", zorder=0)

# 90 degree ceiling that the true dip can never exceed.
ax.axhline(DIP_CEILING_ARCMIN, color="0.55", lw=1.3, ls=":", zorder=1)
ax.text(1.3, DIP_CEILING_ARCMIN * 1.06, "physical ceiling: dip -> 90 deg",
        fontsize=10, color="0.4")

# Curves.
ax.plot(H, dip_exact, color="#222222", lw=3.2, zorder=4,
        label="Exact geometry  D = arccos(R/(R+H))")
ax.plot(H, dip_sqrt, color="#1f5fbf", lw=2.2, zorder=3,
        label="No refraction  D = 1.93*sqrt(H)  (small-angle limit)")
ax.plot(H, dip_refr, color="#cc4125", lw=2.0, ls="--", zorder=3,
        label="With refraction  K lowers 1.93 to 1.75")

# Mark the elevation span covered by the Reed's almanac data (shown in the inset).
reed_seg = (H >= 1.5) & (H <= 21.3)
ax.plot(H[reed_seg], dip_exact[reed_seg], color="#8e44ad", lw=6, alpha=0.35,
        zorder=5, solid_capstyle="round")

# The gap between the geometric and refracted curves IS the refraction effect.
ax.fill_between(H, dip_refr, dip_sqrt, color="#ef8a62", alpha=0.9, zorder=2)
ax.annotate("Effect of refraction\n(K 1.93 to 1.75)",
            xy=(6.0, 4.4), xycoords="data",
            xytext=(40, 4.2), textcoords="data",
            fontsize=9.5, color="#b5341b",
            arrowprops=dict(arrowstyle="->", color="#b5341b",
                            connectionstyle="arc3,rad=-0.35"))

# The thesis of the whole figure: the slope is the diagnostic.
ax.text(6.0e4, 220,
        "Slope 1/2 = a sphere's fingerprint.\n"
        "No flat plane or perspective\n"
        "makes a sqrt(H) dip.",
        fontsize=10.5, va="top", ha="left",
        bbox=dict(boxstyle="round", fc="#eaf2fb", ec="#1f5fbf", alpha=0.95))

# Highlight airline cruise altitude (~10 km), the top of the everyday range.
cruise_exact = dip_exact_arccos(np.array([CRUISE_ALTITUDE_M]))[0]
cruise_sqrt = K_GEOMETRIC * np.sqrt(CRUISE_ALTITUDE_M)
ax.scatter([CRUISE_ALTITUDE_M], [cruise_exact], s=70, color="#2e7d32",
           edgecolor="white", linewidth=1.0, zorder=6)
ax.annotate(f"~10 km (airliner cruise): {cruise_exact:.0f}' = {cruise_exact/60:.1f} deg\n"
            f"sqrt-law within {100*(cruise_sqrt/cruise_exact-1):.1f}%",
            xy=(CRUISE_ALTITUDE_M, cruise_exact), xytext=(2.2e4, 22),
            fontsize=10, color="#2e7d32",
            arrowprops=dict(arrowstyle="->", color="#2e7d32"))

# Silhouette icons: beach ~2 m, cruise ship ~30 m, Burj ~500 m, airliner ~10 km, ISS ~400 km.
beach_exact = dip_exact_arccos(np.array([BEACH_ALTITUDE_M]))[0]
place_icon(ax, draw_person, axes_box=[0.075, 0.165, 0.05, 0.12],
           data_xy=(BEACH_ALTITUDE_M, beach_exact),
           marker_color="#6d4c33",
           label=f"beach ~2 m, {beach_exact:.0f}'")
ship_exact = dip_exact_arccos(np.array([SHIP_ALTITUDE_M]))[0]
place_icon(ax, draw_cruiseship, axes_box=[0.345, 0.205, 0.13, 0.075],
           data_xy=(SHIP_ALTITUDE_M, ship_exact),
           marker_color="#1f4e79",
           label=f"cruise ship deck\n~30 m, {ship_exact:.0f}'")
burj_exact = dip_exact_arccos(np.array([BURJ_ALTITUDE_M]))[0]
place_icon(ax, draw_burj, axes_box=[0.305, 0.43, 0.04, 0.19],
           data_xy=(BURJ_ALTITUDE_M, burj_exact),
           marker_color="#34495e",
           label=f"Burj Khalifa\n~500 m, {burj_exact:.0f}'")
place_icon(ax, draw_airplane, axes_box=[0.455, 0.66, 0.085, 0.09],
           data_xy=(CRUISE_ALTITUDE_M, cruise_exact),
           marker_color="#2e7d32",
           label="airliner ~10 km")

# ISS icon and label, placed next to its own point (no cross-plot arrow).
iss_exact = dip_exact_arccos(np.array([ISS_ALTITUDE_M]))[0]
iss_sqrt = K_GEOMETRIC * np.sqrt(ISS_ALTITUDE_M)
place_icon(ax, draw_iss, axes_box=[0.58, 0.80, 0.14, 0.09],
           data_xy=(ISS_ALTITUDE_M, iss_exact),
           marker_color="#222222",
           label=f"ISS ~400 km\n{iss_exact:.0f}' = {iss_exact/60:.1f} deg, sqrt +{100*(iss_sqrt/iss_exact-1):.0f}%")

# Slope callout for the practical regime.
ax.text(2.7, 2100,
        "Shaded = real observer\n"
        "range (1 m to ~10 km):\n"
        "slope = 1/2; exact and\n"
        "sqrt(H) agree within 1%",
        fontsize=9.5, va="top",
        bbox=dict(boxstyle="round", fc="white", ec="0.6"))

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Observer elevation  H  (metres)", fontsize=12)
ax.set_ylabel("Horizon dip  D  (arcminutes)", fontsize=12)
ax.set_title("Horizon dip vs elevation (log-log)\n"
             "The sqrt(H) law is the small-angle limit of the exact spherical geometry",
             fontsize=13)

ax.grid(True, which="both", ls="-", lw=0.4, color="0.85")
ax.legend(loc="lower right", fontsize=9.5, framealpha=0.95)
ax.set_xlim(1, 1e7)
ax.set_ylim(1.5, 8000)

# Inset: real dip data from Reed's Nautical Almanac (Alt 90 row = pure dip).
# On linear d vs sqrt(H) axes the sqrt law is a straight line through 0; its slope is K.
h_reed = np.array([1.5, 3.0, 4.6, 6.0, 7.6, 9.0, 10.7, 12.0, 13.7, 15.0, 16.8, 18.0, 21.3])
d_reed = np.array([2.2, 3.1, 3.8, 4.4, 4.9, 5.4, 5.8, 6.2, 6.6, 6.9, 7.3, 7.6, 8.2])
k_reed = np.sum(np.sqrt(h_reed) * d_reed) / np.sum(h_reed)

iax = ax.inset_axes([0.055, 0.41, 0.195, 0.205])
x_reed = np.sqrt(h_reed)
xlo, xhi = x_reed.min() - 0.15, x_reed.max() + 0.15
ylo, yhi = d_reed.min() - 0.4, d_reed.max() + 0.4
x_line = np.array([xlo, xhi])
iax.plot(x_line, k_reed * x_line, color="#8e44ad", lw=1.4, zorder=1)
iax.scatter(x_reed, d_reed, s=14, color="#222222", zorder=2)
iax.set_xlim(xlo, xhi)
iax.set_ylim(ylo, yhi)
iax.set_xlabel("sqrt(H)  (m^1/2)", fontsize=7, labelpad=1)
iax.set_ylabel("dip (arcmin)", fontsize=7, labelpad=1)
iax.set_title(f"Reed's almanac dip vs sqrt(H):\nstraight line, K = {k_reed:.2f}",
              fontsize=7.5, pad=2, color="#8e44ad")
iax.tick_params(labelsize=6, length=2)
iax.grid(True, lw=0.3, color="0.85")
iax.set_facecolor("white")
for spine in iax.spines.values():
    spine.set_edgecolor("#8e44ad")

# Range indicator: link the inset's two bottom corners to the two ends of the
# elevation span the almanac data covers on the main curve.
from matplotlib.patches import ConnectionPatch
reed_lo, reed_hi = 1.5, 21.3
d_lo = dip_exact_arccos(np.array([reed_lo]))[0]
d_hi = dip_exact_arccos(np.array([reed_hi]))[0]
ax.scatter([reed_lo, reed_hi], [d_lo, d_hi], s=20, color="#8e44ad",
           edgecolor="white", linewidth=0.6, zorder=6)
for x_axes, x_data, y_data in [(0.055, reed_lo, d_lo), (0.25, reed_hi, d_hi)]:
    ax.add_artist(ConnectionPatch(
        xyA=(x_axes, 0.41), coordsA=ax.transAxes,
        xyB=(x_data, y_data), coordsB=ax.transData,
        color="#8e44ad", lw=0.9, alpha=0.7, zorder=5))

fig.tight_layout()
fig.savefig("/home/"+HOME_OWNER+"/horizon_dip_loglog_exact.png", dpi=200)
fig.savefig("/home/"+HOME_OWNER+"/horizon_dip_loglog_exact.svg")

# Key values for the record.
for h in (1e4, ISS_ALTITUDE_M, 1e6, 1e7):
    print(f"H={h:>9.0f} m   exact={dip_exact_arccos(np.array([h]))[0]:7.1f}'   "
          f"sqrt={K_GEOMETRIC*np.sqrt(h):7.1f}'   "
          f"overshoot={100*(K_GEOMETRIC*np.sqrt(h)/dip_exact_arccos(np.array([h]))[0]-1):5.1f}%")