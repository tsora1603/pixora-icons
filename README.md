<div align="center">
 
# 👾 pixora-icons 👾
**Taking the legacy of an archived 16-bit icon theme.**

</div>

<div align=center>

![GitHub last commit](https://img.shields.io/github/last-commit/tsora1603/pixora-icons?style=for-the-badge&logo=git&labelColor=101418&color=9ccbfb)
![GitHub Repo stars](https://img.shields.io/github/stars/tsora1603/pixora-icons?style=for-the-badge&logo=github&labelColor=101418&color=b9c8da)
![GitHub repo size](https://img.shields.io/github/repo-size/tsora1603/pixora-icons?style=for-the-badge&logo=gitlfs&labelColor=101418&color=d3bfe6)

</div>

>[!Note]
> pixora-icons is being updated regularly. In case you want an icon to be added, please open a new issue.

---

## What is pixora-icons?

A pixel-style icon theme for Linux desktop systems that aims to be as faithful as possible to the original application icons, while maintaining a unique visual style. Made with a vibrant color palette, your 16-bit retro rice will look as good as possible!

## 🌠 Preview

![App_launcher](.github/icons-showcase-2.png)

![Icons showcase](.github/icons2.png)

## 🖥️ Installation

>[!Tip]
> If you use Dolphin as your default file manager and have set `QT_QPA_PLATFORMTHEME=qt6ct`, don't forget to have `qt6ct-kde` installed.

### Arch Linux
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
a. Symlink the files into place, allowing for easy updates by running `git pull`; <br>
b. Copy-paste the files in the right directories, allowing for a fully local installation.

```bash
./install.sh
```
> _If install.sh doesn't run, try ```chmod +x install.sh``` and then run it again._

## 🎨 How to Contribute
Want to contribute to the project? Check our [Contributing Guidelines](CONTRIBUTING.md)!

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
