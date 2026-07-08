# Sinhala-Ready-Movie-Art-Generator
This utility is a Python-based automation script designed to be triggered from a WordPress environment to generate professional-grade movie posters.

A server-side image processing engine designed to automate the creation of branded movie art for media-focused web platforms.

## Overview

This utility is a Python-based automation script designed to be triggered from a backend environment (such as PHP) to generate professional-grade movie posters. It utilizes the **PIL (Python Imaging Library)** and **libraqm (HarfBuzz)** to ensure high-quality, native Sinhala text shaping, making it ideal for localized, branded media assets.

## Features

* **Complex Script Support:** Uses `draw_text_si` to handle proper Sinhala character shaping.


* **Automatic Resizing:** Dynamically calculates aspect ratios to overlay posters onto backdrops with consistent padding and borders.


* **Dynamic Branding:** Supports custom logo placement and generates repeating watermark strips at the footer.


* **Integration Ready:** Returns the output file path via standard output for seamless communication with parent web applications.



## Requirements

* **Python 3.x**

* **Pillow (PIL)** with `libraqm` support for complex script rendering.


* **System Dependencies:** HarfBuzz and FriBidi libraries are required for `libraqm` functionality.



## Usage

The script is designed to be executed via the command line:

```bash
python3 generate_movie_art.py \
    --poster   "/path/to/poster.jpg" \
    --backdrop "/path/to/backdrop.jpg" \
    --author   "Author Name" \
    --rating   "8.4" \
    --watermark "BRAND WATERMARK" \
    --logo     "/path/to/logo.png" \
    --output   "/path/to/output.jpg" \
    --font     "/path/to/font.ttf"

```

## Functionality

The script performs the following operations during execution:

* Loads and converts source images to RGB.


* Applies a styled footer bar with meta-information.


* Renders dynamic text fields for ratings and author attribution.


* Saves the processed result as a JPEG with high-quality settings.
