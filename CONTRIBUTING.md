# Contributing Guidelines

Thank you for your interest in contributing to this project!
Pixora-icons welcomes bug reports, pull and feature requests, and suggestions!

## Bug Reports

Before opening an issue: 
- Search existing issues, your problem may have already been mentioned.
- Make sure you're using the latest version.

Please include in your report: 
- Your distro (Ubuntu, Arch, Fedora... Or  any of their derivatives);
- Your DE (GNOME, KDE, XFce...)
- Theme version;
- Steps to reproduce the bug (if applicable);
- Screenshots (if applicable).

## Icon Requests

Please refrain from adding multiple icon requests into the same issue, as this makes the workflow quite chaotic.

## Pull Requests

Pull Requests must follow the **Design Guidelines** described below. <br>
Please keep PRs small and focused:
- One feature per PR;
- One fix per PR;
- No unrelated changes.

---

# pixora-icons Design Guidelines

***These Guidelines are still work-in-progress and are subject to change!***

If you want to make icons for pixora-icons, these guidelines should point you to the right direction. Although they are not that strict, you should still keep them in mind for consistency reasons. <br>
These guidelines apply to every app, be it Discord, Firefox, Steam (branded apps); or Settings, Accessibility, File Manager (non-branded apps).

## Taking References

You're free to use any version you want from any app icon for reference, besides the really old ones if the app has been through many rebrandings. Also try to keep the designs consistent with existing ones!

## Color Palette
pixora-icons uses a specific color palette. You can check it out by clicking [here](https://lospec.com/palette-list/resurrect-32)!
This, together with the vectorizing rule, should be the only rule that is very strict. Please refrain from using any color outside of the 32 ones that Resurrect offers, as this would ruin the general aesthetic of your icon when comparing it with the rest.

Be creative with your designs! If you're not that deep into art, many times you'll think that it's impossible to draw an icon without a specific color, but it is very much possible if you try hard enough. 
You're free to tweak the original icon aesthetic as much as you want, as long as it does not make it unrecognizable. Have fun!

Visual representation of the color palette:

![Color Palette](.github/resurrect-32-32x.png)

## Borders

Every app icon has a border. Its purpose is to keep the icons 'away' from any background color and define their own space on the screen. Since they are all drawn on a 16x16 grid, every color matters, and avoiding background fading is super important. 

A border has three simple criteria:
- It should be colored `#3E3546`;
- It should go around the **entire** icon (so avoid coloring the edges of the grid as much as possible);
- If the icon has any "hollow" (transparent) section, or an internal border (think of a donut shape) it should go there as well.

Here you can see examples of GOOD borders and BAD borders:

![Borders Examples](.github/borders-examples.png)

Why are those borders considered 'bad':

1. The first one has the wrong color (`#625565` instead of `#3E3546`);
2. The second one does not go all the way around, since there's a part of the icon on the edge of the grid. It is actually possible to make this border good — the icon width is 14px;
3. The third one only goes around the external part of the icon, leaving the inside region incomplete.

## Shading

Every icon should have some sort of shading, except monochromatic ones (eg.: GitHub, Monochrome, Hydra Launcher), and rare exceptions, like Nvidia's, where it kind of has some shading originally already, and that is enough. This is to keep visual consistency between the icons.

Shading is (most of the time) done assuming the light source is above the object, so a lighter tone on the top part and a darker one on the bottom part should suffice. It is also quite simplistic, so a single-pixel line should be enough.
This is when the limitations of the 32-color palette shine the most!

Example of shaded vs non-shaded versions of the same icon:

![Shade vs No Shade](.github/shading-example.png)

## Glyphs and General Advice

Keep in mind that pixel art is not about taking the full resolution version of an image and resizing it down; it's actually redrawing it from scratch, where every single pixel matters and actually represents a significant portion of the whole image. You can see this clearly on this project, since we're limited to mere 256 pixels IN TOTAL for every single image. 

When drawing the glyph of any app, try to think which portion of the whole image the last pixel(s) you've drawn actually represents. You'll be surprised of how often you notice that the final result is getting distorted, and you'll know exactly why by applying this thought process.

## Vectorizing

Every app icon should be vectorized. Reason being, I think it's way easier to, in this project's case, make every icon a vector and set the  to `scalable`, than having to make 16, 24, 32, 64px and so on versions of every single icon. The entire vectorizing process is automated by a shell script, so it should be a walk in the park. 

### Tutorial:

>[!Note] 
> Claude AI was used to build the entirety of both `vectorizing.sh` and `svgfit.py` scripts, since I don't know how to code myself. They were tested on my own machine before being pushed to the repo, and are of course available for further inspection. They should work without any issues, since it's just a `.png > .svg` process inside a localized group of directories. Each major step of `vectorizing.sh` can be done manually, and `svgfit.py` only exists to replace Inkscape CLI tools, since they're not compatible with GNU Parallel for multi-processing.

1. **[⚠️ IMPORTANT]** After finishing your design on your favorite 16x16 canvas, export the file to any folder named `16x16`;
2. Make sure to have [imagemagick](https://imagemagick.org/script/download.php#gsc.tab=0), [vtracer](https://github.com/visioncortex/vtracer), [scour](https://deepwiki.com/scour-project/scour/2.1-installation), [python-lxml](https://github.com/lxml/lxml?tab=readme-ov-file), and [parallel](https://www.gnu.org/software/parallel/) installed;
3. Have the provided [vectorizing.sh](/pixora/vectorizing.sh) and [svgfit.py](/pixora/svgfit.py) scripts available ***outside***  the `16x16` folder with your design(s);
4. Execute `vectorizing.sh` via any way you like, e.g. by doing `./vectorizing.sh`;
5. You should now have a folder named `svg` containing all the traced files;
6. Read this tutorial again and make sure you understand each step;
7. Done! :)

---

# License Reminder
By contributing, you agree that your contributions will be licensed under the same license as the project.

