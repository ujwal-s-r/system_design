This folder contains a minimal Flask app and Dockerfile for learning purposes.

How to build and run (PowerShell):

# Build the image
docker build -t first-app .

# Run the container, publishing port 5000
docker run -p 5000:5000 first-app

Then open http://localhost:5000 in your browser.

Notes:
- The Dockerfile copies the `app/` directory contents into `/app` inside the image.
- If you change dependencies, update `requirements.txt` and rebuild the image.
