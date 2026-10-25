<div align="center">
 
# 👾 pixora-icons 👾
**Taking the legacy of an archived 16-bit icon theme.**

</div>

<div align=center>

![GitHub last commit](https://img.shields.io/github/last-commit/tsora1603/pixora-icons?style=for-the-badge&logo=git&labelColor=101418&color=9ccbfb)
![GitHub Repo stars](https://img.shields.io/github/stars/tsora1603/pixora-icons?style=for-the-badge&logo=github&labelColor=101418&color=b9c8da)
![GitHub repo size](https://img.shields.io/github/repo-size/tsora1603/pixora-icons?style=for-the-badge&logo=gitlfs&labelColor=101418&color=d3bfe6)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/tsora)

</div>

>[!Note]
> pixora-icons is being updated regularly. In case you want an icon to be added, please open a new issue.

---

## What is pixora-icons?

A pixel-style icon theme for Linux desktop systems that aims to be as faithful as possible to the original application icons, while maintaining a unique visual style. Made with a vibrant color palette, your 16-bit retro rice will look as good as possible!

## 🎨 Theme variants

- **Pixora** uses the pack's fixed colors.
- **Pixora Dark** uses the same artwork with a dark-theme fallback.
- **[Pixora Accent](#-pixora-accent-for-kde)** is an optional KDE variant with accent-colored folders.

## 🌠 Preview

![App_launcher](.github/icons-showcase-2.png)

![Icons showcase](.github/icons2.png)

## 🖥️ Installation

>[!Tip]
> If you use Dolphin as your default file manager and have set `QT_QPA_PLATFORMTHEME=qt6ct`, don't forget to have `qt6ct-kde` installed.

### Arch Linux
Using `shelly`:
```bash
shelly install aur pixora-icons-git
```
Using `paru`:
```bash
paru -S pixora-icons-git
```
Using `yay`:
```bash
yay -S pixora-icons-git
```

### Manual installation
#### 1. Clone the repo 
```bash
git clone https://github.com/tsora1603/pixora-icons.git
cd pixora-icons/scripts
```

#### 2. Launch the installation script
This will either: <br>
a. Symlink all three variants into place, allowing for easy updates by running `git pull` in the checkout; <br>
b. Copy all three variants into the icon directory, preserving their internal symlinks for a fully local installation. Update the checkout and re-run the installer to refresh those copies.

```bash
./install.sh
```
> _If install.sh doesn't run, try ```chmod +x install.sh``` and then run it again._

## 🎨 How to Contribute
Want to contribute to the project? Check our [Contributing Guidelines](CONTRIBUTING.md)!

## 🎨 Pixora Accent for KDE

Pixora Accent makes folder bodies follow the user's KDE accent color. Glyphs use darker shades of that color while retaining their shapes and details. These dynamic colors are an exception to the fixed Resurrect 32 palette.

>[!WARNING]
> **Pixora Accent was entirely vibe-coded** because I could not implement KDE's accent-color behavior myself for each icon or code a script that does that on my behalf. **Errors and visual inconsistencies may appear as a result.** If you find a problem, please open an issue with the icon name, a screenshot, your KDE version and your accent color. Thank you.

### Install and enable

Both the [manual installer](#manual-installation) and the repository's [AUR package](#arch-linux) install Pixora, Pixora Dark and Pixora Accent side by side. To use the optional variant:

1. Open **KDE System Settings → Colors & Themes → Icons** and select **Pixora Accent**.
2. Choose an accent color in **Colors & Themes → Colors** and apply it.

The manual installer uses `~/.local/share/icons/`, or `$XDG_DATA_HOME/icons/` when configured. If installing the directories yourself, keep `pixora` and `pixora-accent` next to each other in that location.

### Compatibility and updates

Pixora Accent is intended for KDE Plasma 6 applications using KDE's color-scheme-aware SVG loader. It was tested with Qt 6.8.2 and KIconThemes 6.13.0. Other renderers may display the beige fallback instead of the chosen accent color. No background service or per-color regeneration is required.

If an open application keeps the previous colors, reselect the icon theme or reopen the application to refresh its cached icons. KDE may slightly lighten the accent color for selected icons to improve contrast.

Contributors can regenerate the folder artwork and aliases from the source checkout with `python3 scripts/generate-accent.py` and check them with `python3 scripts/generate-accent.py --check` (Python 3.9 or newer). The generator discovers original folders automatically and stops for review if an artwork has an unsupported structure.

## 👥 CREDITS
- Inspired by **MrDeltaMan**: https://github.com/MrDeltaMan/DeltaPixel-Theme
- Original work by **maxtron95**: https://github.com/maxtron95/tuxonpixels-icon-theme

<br>

---

<a href="https://www.star-history.com/?repos=tsora1603%2Fpixora-icons&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=tsora1603/pixora-icons&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=tsora1603/pixora-icons&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=tsora1603/pixora-icons&type=date&legend=top-left" />
 </picture>
</a>
