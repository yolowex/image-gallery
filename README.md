# Foto Folio - Image and Video Gallery/Editor

Foto Folio is a fully featured Image and Video gallery/editor made with Pygame Community Edition. It allows you to manage your images and videos efficiently and even perform basic editing tasks on your photos. The app runs on Windows and Linux, and it should also work on Mac, although it hasn't been extensively tested on that platform.

## Features

* View and manage images and videos in a user-friendly interface.
* Copy, cut, delete, and rename contents.
* Create new folders to organize your media collection.
* Edit and enhance photos (not videos) with basic editing tools.
* Tag people in a picture to easily organize them by subjects.
* Modify location and caption tags for better organization.
* Play videos (Note: video playback is laggy due to limitations in python threading).
* Play gifs for a more dynamic experience.

## Libraries Used

Foto Folio was built using the following libraries:

* Pygame Community Edition (pygame-ce): A faster and better-maintained fork of the popular Pygame library, used for handling graphics and user input in the app.
* OpenCV (opencv-python): An open-source computer vision and image processing library.
* Pillow: A friendly fork of the Python Imaging Library (PIL), used for image processing tasks.
* Tkinter: Python's standard GUI library for creating the graphical user interface.
* SQLite3: A lightweight and serverless database engine used for storing application data.
* MoviePy: A library for video editing and processing.


## Requirements

Make sure you have the following libraries installed before running Foto Folio:

* pygame-ce
* Pillow
* numpy
* opencv-python
* moviepy
* ffmpeg project (https://ffmpeg.org/)

To install the required libraries, you can use pip:

```shell
pip install requirements.txt
```

Note: If you have the original Pygame library installed, you'll need to uninstall it first before installing pygame-ce:

```shell
pip uninstall pygame
pip install pygame-ce
```

## How to Use
just fork this repository, install the requirements, and run `python main.py`

## Contributing

We welcome contributions from the community to help improve Foto Folio. If you're interested in solving the concurrency problem or adding better color themes, please feel free to contribute to the project. You can submit issues, pull requests, or just reach out to us with your ideas.

Let's make Foto Folio even better together!

## License

This project is licensed under the MIT License - see the LICENSE file for details.


________________________________________

Thank you for showing interest in Foto Folio! 
We hope you enjoy using the app and find it helpful in managing your media collection. 
If you encounter any issues or have any suggestions, don't hesitate to let us know. 
Happy organizing and editing! 😊
